#!/usr/bin/env python

from functools import partial
from typing import Generator, List, Union
from dataclasses import asdict

import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from urllib.parse import urljoin

from flightplandb.datatypes import (
    StatusResponse,
    PlanQuery, Plan, GenerateQuery,
    User, Tag,
    Airport, Track, Navaid,
    Weather
)


format_return_types = {
            # if a dict is requested, the JSON will later be converted to that
            "dict": "application/json",
            # otherwise, pure JSON will be returned
            "json": "application/json",
            "xml": "application/xml",
            "csv": "text/csv",
            "pdf": "application/pdf",
            "kml": "application/vnd.fpd.export.v1.kml+xml",
            "xplane": "application/vnd.fpd.export.v1.xplane",
            "xplane11": "application/vnd.fpd.export.v1.xplane11",
            "fs9": "application/vnd.fpd.export.v1.fs9",
            "fsx": "application/vnd.fpd.export.v1.fsx",
            "squawkbox": "application/vnd.fpd.export.v1.squawkbox",
            "xfmc": "application/vnd.fpd.export.v1.xfmc",
            "pmdg": "application/vnd.fpd.export.v1.pmdg",
            "airbusx": "application/vnd.fpd.export.v1.airbusx",
            "qualitywings": "application/vnd.fpd.export.v1.qualitywings",
            "ifly747": "application/vnd.fpd.export.v1.ifly747",
            "flightgear": "application/vnd.fpd.export.v1.flightgear",
            "tfdi717": "application/vnd.fpd.export.v1.tfdi717",
            "infiniteflight": "application/vnd.fpd.export.v1.infiniteflight"
            }


class FlightPlanDB:
    def __init__(
            self, key: str,
            url_base: str = "https://api.flightplandatabase.com"):
        """
        To get an API key, visit your account settings page.
        Your account will need a verified email address to add an API key.
        https://flightplandatabase.com/settings

        Args:
            key (str): api token
        """
        self.key: str = key
        self._header: CaseInsensitiveDict[str] = CaseInsensitiveDict()
        self.url_base = url_base

    # general HTTP request function for non-paginated results
    def request(self, method: str,
                path, ignore_statuses=[],
                return_format="dict",
                params={}, *args, **kwargs):

        # convert the API content return format to an HTTP Accept type
        try:
            return_format_encoded = format_return_types[return_format]
        except KeyError:
            raise ValueError(
                f"'{return_format}' is not a valid data return type option")

        # then add it to the request headers
        params["Accept"] = return_format_encoded

        resp = requests.request(
            method,
            urljoin(self.url_base, path),
            auth=HTTPBasicAuth(self.key, None),
            *args, **kwargs)

        if resp.status_code not in ignore_statuses:
            resp.raise_for_status()

        self._header = resp.headers

        if return_format == "dict":
            return resp.json()

        return resp.text  # if the format is not a dict

    # and here go the specific non-paginated HTTP calls
    def get(self, path, ignore_statuses=[],
            return_format="dict", *args, **kwargs):
        resp = self.request("get",
                            path,
                            ignore_statuses=[],
                            return_format="dict",
                            *args, **kwargs)
        return resp

    def post(self, path, ignore_statuses=[],
             return_format="dict", *args, **kwargs):
        resp = self.request("post",
                            path,
                            ignore_statuses=[],
                            return_format="dict",
                            *args, **kwargs)
        return resp

    def patch(self, path, ignore_statuses=[],
              return_format="dict", *args, **kwargs):
        resp = self.request("patch",
                            path,
                            ignore_statuses=[],
                            return_format="dict",
                            *args, **kwargs)
        return resp

    def delete(self, path, ignore_statuses=[],
               return_format="dict", *args, **kwargs):
        resp = self.request("delete",
                            path,
                            ignore_statuses=[],
                            return_format="dict",
                            *args, **kwargs)
        return resp

    # For paginated results, no return format allowed
    def getiter(self, path,
                ignore_statuses=[],
                limit=100,
                params=None,
                *args, **kwargs):
        url = urljoin(self.url_base, path)
        auth = HTTPBasicAuth(self.key, None)

        session = requests.Session()
        # initially no results have been fetched yet
        num_results = 0

        r_fpdb = session.get(url, params=params, auth=auth, *args, **kwargs)

        # I detest responses which "may" be paginated
        # therefore I choose to pretend they are paginated anyway, with 1 page
        if 'X-Page-Count' in r_fpdb.headers:
            num_pages = int(r_fpdb.headers['X-Page-Count'])
        else:
            num_pages = 1

        # while page <= num_pages...
        for page in range(0, num_pages):
            params['page'] = page
            r_fpdb = session.get(url,
                                 params=params,
                                 auth=auth,
                                 *args, **kwargs)
            # ...keep cycling through pages...
            for e in r_fpdb.json():
                # ...and return every dictionary in there...
                yield e
                num_results += 1
                # ...unless the result limit has been reached
                if num_results == limit:
                    return

    def _header_value(self, header_key):
        if header_key not in self._header:
            self.ping()  # Make at least one request
        return self._header[header_key]

    @property
    def api_version(self) -> int:
        """
        Returns:
            int: API version that returned the response
        """
        return int(self._header_value("X-API-Version"))

    @property
    def units(self) -> str:
        """The units system used for numeric values.
        https://flightplandatabase.com/dev/api#units

        Returns:
            String: AVIATION, METRIC or SI
        """
        return self._header_value("X-Units")

    @property
    def limit_cap(self) -> int:
        """
        The number of requests allowed per day, operated on an hourly rolling
        basis. i.e Requests used between 19:00 and 20:00 will become available
        again at 19:00 the following day. API key authenticated requests get a
        higher daily rate limit and can be raised if a compelling
        use case is presented.
        Returns:
            int: number of allowed requests per day
        """
        return int(self._header_value("X-Limit-Cap"))

    @property
    def limit_used(self) -> int:
        """
        The number of requests used in the current period
        by the presented API key or IP address

        Returns:
            int: number of requests used in period
        """
        return int(self._header_value("X-Limit-Used"))

    def ping(self) -> StatusResponse:
        """Checks API status to see if it is up"""
        resp = self.get("")
        return StatusResponse(**resp)

    def revoke(self) -> StatusResponse:
        """
        Revoke the API key in use in the event it is compromised.

        If the HTTP response code is 200 and the status message is "OK", then
        the key has been revoked and any further requests will be rejected.
        Any other status code or message indicates an error
        has occurred and the errors array will give further details.
        """
        resp = self.get("/auth/revoke")
        self._header = resp.headers
        return StatusResponse(**resp.json())

    # Sub APIs
    @property
    def plan(self):
        return PlanAPI(self)

    @property
    def user(self):
        return UserAPI(self)

    @property
    def tags(self):
        return TagsAPI(self)

    @property
    def nav(self):
        return NavAPI(self)

    @property
    def weather(self):
        return WeatherAPI(self)


class PlanAPI():
    # TODO: params
    #   allow flight plan return format to be specified by user
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def fetch(self, id_: int,
              return_format: str = "dict") -> Union[Plan, bytes]:
        """
        Fetches a flight plan and its associated attributes by ID.
        Returns it in specified format.
        """
        request = self._fp.get(f"/plan/{id_}", return_format=return_format)
        if return_format == "dict":
            return Plan(**request)

        return request  # if the format is not a dict

    def create(self, plan: Plan, return_format: str = "dict") -> Plan:
        return Plan(**self._fp.post("/plan", json=asdict(plan)))

    def edit(self, plan: Plan) -> Plan:
        return Plan(**self._fp.patch(f"/plan/{plan.id}", json=asdict(plan)))

    def delete(self, id_: int) -> StatusResponse:
        return StatusResponse(**self._fp.delete(f"/plan/{id_}"))

    def search(self, plan_query: PlanQuery,
               limit: int = 100) -> Generator[Plan, None, None]:
        for i in self._fp.getiter("/search/plans",
                                  params=plan_query.as_dict(),
                                  limit=limit):
            yield Plan(**i)

    def has_liked(self, id_: int) -> bool:
        sr = StatusResponse(
            **self._fp.get(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def like(self, id_: int) -> StatusResponse:
        return StatusResponse(**self._fp.post(f"/plan/{id_}/like"))

    def unlike(self, id_: int) -> bool:
        sr = StatusResponse(
            **self._fp.delete(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def generate(self, gen_query: GenerateQuery) -> Plan:
        return Plan(
            **self._fp.patch(
                "/auto/generate", json=asdict(gen_query)))

    def decode(self, route: str) -> Plan:
        return Plan(**self._fp.post(
            "/auto/decode", json={"route": route}))


class UserAPI:
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    @property
    def me(self) -> User:
        return User(**self._fp.get("/me"))

    def fetch(self, username: str) -> User:
        return User(**self._fp.get(f"user/{username}"))

    def plans(self, username: str,
              limit: int = 100) -> Generator[Plan, None, None]:
        # TODO: params
        #   page The page of results to fetch
        #   limit [20] The number of plans to return per page (max 100)
        #   sort The order of the returned plans
        for i in self._fp.getiter(f"/user/{username}/plans",
                                  limit=limit):
            yield Plan(**i)

    def likes(self, username: str,
              limit: int = 100) -> Generator[Plan, None, None]:
        # TODO: params
        #   page The page of results to fetch
        #   limit [20] The number of plans to return per page (max 100)
        #   sort The order of the returned plans
        for i in self._fp.getiter(f"/user/{username}/likes",
                                  limit=limit):
            yield Plan(**i)

    def search(self, username: str) -> Generator[User, None, None]:
        for i in self._fp.getiter("/search/users",
                                  limit=limit,
                                  params={"q": username}):
            yield User(**i)


class TagsAPI:
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def fetch(self) -> List[Tag]:
        return list(map(lambda t: Tag(**t), self._fp.get("/tags")))


class NavAPI:
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def airport(self, icao) -> Airport:
        return Airport(**self._fp.get(f"/nav/airport/{icao}"))

    def nats(self) -> List[Track]:
        return list(
            map(lambda n: Track(**n), self._fp.get("/nav/NATS")))

    def pacots(self) -> List[Track]:
        return list(
            map(lambda t: Track(**t), self._fp.get("/nav/PACOTS")))

    def search(self, q: str,
               type_: str = None) -> Generator[Navaid, None, None]:
        params = {"q": q}
        if type_:
            if type_ in Navaid.validtypes:
                params["types"] = type_
            else:
                raise ValueError(f"{type_} is not a valid Navaid type")
        for i in self._fp.getiter("/search/nav", params=params):
            yield Navaid(**i)


class WeatherAPI:
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def fetch(self, icao: str) -> Weather:
        return Weather(**self._fp.get(f"/weather/{icao}"))


def test_run():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    token = os.environ["KEY"]
    api = FlightPlanDB(token)

    print(api.ping())
    print(api.limit_used)

    plan_id = 98
    plan = api.plan(plan_id)
    plan_dict = asdict(plan)
    print(plan_dict)

    # print(api.get())
