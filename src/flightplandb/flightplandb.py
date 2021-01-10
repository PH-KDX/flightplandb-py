#!/usr/bin/env python

from functools import partial
from typing import List
from dataclasses import asdict

import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from urllib.parse import urljoin

from flightplandb.datatypes import (
    StatusResponse, Pagination,
    PlanQuery, Plan, GenerateQuery,
    User, Tag,
    Airport, Track, Navaid,
    Weather, Response
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

# Set a "format" argument.
# This must be converted to the equivalent format string (perhaps in datatypes.py?)
# It must be added as a header.

# Same goes for pagination. However, this does not need to be defined in datatypes.

    def __call__(self,
                 method: str,
                 path,
                 ignore_statuses=[],
                 return_format="dict",
                 params={},
                 *args,
                 **kwargs):
        try:
            return_format_encoded = format_return_types[return_format]
        except KeyError:
            raise ValueError(
                f"'{return_format}' is not a valid data return type option")

        params["Accept"] = return_format_encoded

        resp = requests.request(
            method,
            urljoin(self.url_base, path),
            auth=HTTPBasicAuth(self.key, None),
            params=params,
            *args, **kwargs)

        if resp.status_code not in ignore_statuses:
            resp.raise_for_status()
        self._header = resp.headers

        # return resp.json()
        resp_formatted = Response(
                content=resp.json() if return_format == "dict" else resp.text,
                api_version=resp.headers["X-API-Version"],
                units=resp.headers["X-Units"],
                limit_cap=resp.headers["X-Limit-Cap"],
                limit_used=resp.headers["X-Limit-Used"],
                pagination=None)

        if "X-Page-Current" in resp.headers:
            resp_formatted.pagination = Pagination(
                    page_count=resp.headers["X-Page-Count"],
                    page=resp.headers["X-Page-Current"],
                    limit=resp.headers["X-Page-PerPage"],
                    sort=resp.headers["X-Sort"])

        return resp_formatted

    def __getattr__(self, attr):
        """
        The API only supports the following HTTP verbs
        """
        if attr not in ["get", "post", "patch", "delete"]:
            raise AttributeError(
                f"'{self.__class__.__name__}' has no attribute '{attr}'")

        return partial(self, attr)

    def ping(self) -> StatusResponse:
        """Checks API status to see if it is up"""
        resp = self.get("")
        resp.content = StatusResponse(**resp.content)
        return(resp)

    def revoke(self) -> StatusResponse:
        """
        Revoke the API key in use in the event that it is compromised.

        If the HTTP response code is 200 and the status message is "OK", then
        the key has been revoked and any further requests will be rejected.
        Any other status code or message indicates an error
        has occurred and the errors array will give further details.
        """
        resp = self.get("/auth/revoke")
        resp.content = StatusResponse(**resp.content)
        return(resp)

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

    def __call__(self, id_: int) -> Plan:
        """
        Fetches a flight plan and its associated attributes by ID.
        Returns it in specified format.
        """
        resp = self._fp.get(f"/plan/{id_}")
        resp.content = Plan(**resp.content)
        return(resp)

    def create(self, plan: Plan) -> Plan:
        resp = self._fp.post("/plan", json=asdict(plan))
        resp.content = Plan(**resp.content)
        return(resp)

    def edit(self, plan: Plan) -> Plan:
        resp = self._fp.post("/plan", json=asdict(plan))
        resp.content = Plan(**resp.content)
        return(resp)

    def delete(self, id_: int) -> StatusResponse:
        resp = self._fp.post("/plan", json=asdict(plan))
        resp.content = StatusResponse(**resp.content)
        return(resp)

    def search(self, plan_query: PlanQuery) -> List[Plan]:
        resp = self._fp.get("/search/plans", params=plan_query.as_dict())
        resp.content = list(
            map(
                lambda u: Plan(**u),
                resp.content))
        return resp

    def has_liked(self, id_: int) -> bool:
        resp = self._fp.get(f"/plan/{id_}/like", ignore_statuses=[404])
        # resp.content is still a dict at this point
        resp.content = (resp.content["message"] != "Not Found")
        return resp

    def like(self, id_: int) -> StatusResponse:
        resp = self._fp.post(f"/plan/{id_}/like")
        resp.content = StatusResponse(**resp.content)
        return resp

    def unlike(self, id_: int) -> bool:
        resp = self._fp.get(f"/plan/{id_}/like", ignore_statuses=[404])
        # resp.content is still a dict at this point
        resp.content = (resp.content["message"] != "Not Found")
        return resp

    def generate(self, gen_query: GenerateQuery) -> Plan:
        resp = self._fp.patch("/auto/generate", json=asdict(gen_query))
        resp.content = Plan(**resp.content)
        return resp

    def decode(self, route: str) -> Plan:
        resp = self._fp.post("/auto/decode", json={"route": route})
        resp.content = Plan(**resp.content)
        return resp


class UserAPI:
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    @property
    def me(self) -> User:
        resp = self._fp.get("/me")
        resp.content = User(**resp.content)
        return resp

    def __call__(self, username: str) -> User:
        resp = self._fp.get(f"/user/{username}")
        resp.content = User(**resp.content)
        return resp

    def plans(self, username: str) -> List[Plan]:
        # TODO: params
        #   page The page of results to fetch
        #   limit [20] The number of plans to return per page (max 100)
        #   sort The order of the returned plans
        resp = self._fp.get(f"/user/{username}/plans")
        resp.content = list(
            map(
                lambda u: Plan(**u),
                resp.content))
        return resp

    def likes(self, username: str) -> List[Plan]:
        # TODO: params
        #   page The page of results to fetch
        #   limit [20] The number of plans to return per page (max 100)
        #   sort The order of the returned plans
        resp = self._fp.get(f"/user/{username}/likes")
        resp.content = list(
            map(
                lambda u: Plan(**u),
                resp.content))
        return resp

    def search(self, username: str) -> List[User]:
        resp = self._fp.get("/search/users", params={"q": username})
        resp.content = list(
            map(
                lambda u: User(**u),
                resp.content))
        return resp


class TagsAPI:
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def __call__(self) -> List[Tag]:
        resp = self._fp.get("/tags")
        resp.content = list(map(lambda t: Tag(**t), resp.content))
        return resp


class NavAPI:
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def airport(self, icao) -> Airport:
        resp = self._fp.get(f"/nav/airport/{icao}")
        resp.content = Airport(**resp.content)
        return resp

    def nats(self) -> List[Track]:
        resp = self._fp.get("/nav/NATS")
        resp.content = list(map(lambda n: Track(**n), resp.content))
        return resp

    def pacots(self) -> List[Track]:
        resp = self._fp.get("/nav/PACOTS")
        resp.content = list(map(lambda n: Track(**n), resp.content))
        return resp

    def search(self, q: str, types: str = None) -> List[Navaid]:
        params = {"q": q}
        if types:
            params["types"] = types
        return list(map(
            lambda n: Navaid(**n),
            self._fp.get("/search/nav", params=params)))


class WeatherAPI:
    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def __call__(self, icao: str) -> Weather:
        resp = self._fp.get(f"/weather/{icao}")
        resp.content = Weather(**resp.content)
        return resp


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
