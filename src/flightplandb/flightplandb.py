#!/usr/bin/env python
"""Summary

Attributes
----------
format_return_types : TYPE
    Description
"""

from functools import partial
from typing import Generator, List, Dict, Union
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

    """Summary

    Attributes
    ----------
    url_base : TYPE
        Description
    """

    def __init__(
            self, key: str,
            url_base: str = "https://api.flightplandatabase.com"):
        """
        To get an API key, visit your account settings page.
        Your account will need a verified email address to add an API key.
        https://flightplandatabase.com/settings

        Parameters
        ----------
        key : str
            api token
        url_base : str, optional
            Description
        """
        self.key: str = key
        self._header: CaseInsensitiveDict[str] = CaseInsensitiveDict()
        self.url_base = url_base

    # general HTTP request function for non-paginated results
    def request(self, method: str,
                path: str, ignore_statuses=[],
                return_format="dict",
                params={}, *args, **kwargs) -> Union[Dict, bytes]:
        """
        General HTTP requests function. Only for internal use.

        Parameters
        ----------
        method : str
            An HTTP request type. One of GET, POST, PATCH, or DELETE
        path : str
            The endpoint's path to which the request is being made
        ignore_statuses : list, optional
            Statuses (together with 200 OK) which don't raise an HTTPError
        return_format : str, optional
            The API response format; defaults to Python dict
        params : dict, optional
            Any other HTTP request parameters. God knows what; go read the code
        *args
            etc
        **kwargs
            etc...

        Returns
        -------
        Union[Dict, bytes]
            Returns a dict if return_format is dict, otherwise returns bytes

        Raises
        ------
        ValueError
            Invalid return_format option

        HTTPError
            Invalid HTTP status in response
        """
        # convert the API content return_format to an HTTP Accept type
        try:
            return_format_encoded = format_return_types[return_format]
        # unless it's not a valid return_format
        except KeyError:
            raise ValueError(
                f"'{return_format}' is not a valid data return type option")

        # then add it to the request headers
        params["Accept"] = return_format_encoded

        resp = requests.request(method, urljoin(self.url_base, path),
                                auth=HTTPBasicAuth(self.key, None),
                                *args, **kwargs)

        if resp.status_code not in ignore_statuses:
            resp.raise_for_status()

        self._header = resp.headers

        if return_format == "dict":
            return resp.json()

        return resp.text  # if the format is not a dict

    # and here go the specific non-paginated HTTP calls
    def get(self, path: str, ignore_statuses=[],
            return_format="dict", params={},
            *args, **kwargs):
        """Summary

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        ignore_statuses : list, optional
            Statuses (together with 200 OK) which don't raise an HTTPError
        return_format : str, optional
            Description
        params : dict, optional
            Description
        *args
            Description
        **kwargs
            Description

        Returns
        -------
        TYPE
            Description
        """
        resp = self.request("get", path,
                            ignore_statuses=[],
                            return_format="dict",
                            params={},
                            *args, **kwargs)
        return resp

    def post(self, path: str, ignore_statuses=[],
             return_format="dict", params={},
             *args, **kwargs):
        """Summary

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        ignore_statuses : list, optional
            Statuses (together with 200 OK) which don't raise an HTTPError
        return_format : str, optional
            Description
        params : dict, optional
            Description
        *args
            Description
        **kwargs
            Description

        Returns
        -------
        TYPE
            Description
        """
        resp = self.request("post",
                            path,
                            ignore_statuses=[],
                            return_format="dict",
                            params={},
                            *args, **kwargs)
        return resp

    def patch(self, path: str, ignore_statuses=[],
              return_format="dict", params={},
              *args, **kwargs):
        """Summary

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        ignore_statuses : list, optional
            Description
        return_format : str, optional
            Description
        params : dict, optional
            Description
        *args
            Description
        **kwargs
            Description

        Returns
        -------
        TYPE
            Description
        """
        resp = self.request("patch",
                            path,
                            ignore_statuses=[],
                            return_format="dict",
                            params={},
                            *args, **kwargs)
        return resp

    def delete(self, path: str, ignore_statuses=[],
               return_format="dict", params={},
               *args, **kwargs):
        """Summary

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        ignore_statuses : list, optional
            Statuses (together with 200 OK) which don't raise an HTTPError
        return_format : str, optional
            Description
        params : dict, optional
            Description
        *args
            Description
        **kwargs
            Description

        Returns
        -------
        TYPE
            Description
        """
        resp = self.request("delete",
                            path,
                            ignore_statuses=[],
                            return_format="dict",
                            params={},
                            *args, **kwargs)
        return resp

    # For paginated results, no return format allowed
    def getiter(self, path: str,
                ignore_statuses=[],
                limit=100,
                params={},
                *args, **kwargs) -> Generator[Dict, None, None]:
        """Summary

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        ignore_statuses : list, optional
            Statuses (together with 200 OK) which don't raise an HTTPError
        limit : int, optional
            Maximum number of results to return
        params : None, optional
            Description
        *args
            Description
        **kwargs
            Description

        Returns
        -------
        Generator[Dict, None, None]
            Description
        """
        url = urljoin(self.url_base, path)
        auth = HTTPBasicAuth(self.key, None)

        session = requests.Session()
        # initially no results have been fetched yet
        num_results = 0

        r_fpdb = session.get(url, params=params, auth=auth, *args, **kwargs)

        # I detest responses which "may" be paginated
        # therefore I choose to pretend that all pages are paginated
        # if it is unpaginated I say it is paginated with 1 page
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

    def _header_value(self, header_key: str) -> str:
        """
        Parameters
        ----------
        header_key : str
            One of the header keys

        Returns
        -------
        str
            The value corresponding to the passed key
        """
        if header_key not in self._header:
            self.ping()  # Make at least one request
        return self._header[header_key]

    @property
    def api_version(self) -> int:
        """
        Returns
        -------
        int
            API version that returned the response
        """
        return int(self._header_value("X-API-Version"))

    @property
    def units(self) -> str:
        """
        The units system used for numeric values.
        https://flightplandatabase.com/dev/api#units

        Returns
        -------
        str
            AVIATION, METRIC or SI
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

        Returns
        -------
        int
            number of allowed requests per day
        """
        return int(self._header_value("X-Limit-Cap"))

    @property
    def limit_used(self) -> int:
        """
        The number of requests used in the current period
        by the presented API key or IP address

        Returns
        -------
        int
            number of requests used in period
        """
        return int(self._header_value("X-Limit-Used"))

    def ping(self) -> StatusResponse:
        """
        Checks API status to see if it is up

        Returns
        -------
        StatusResponse
            OK 200 means the service is up and running.
        """
        resp = self.get("")
        return StatusResponse(**resp)

    def revoke(self) -> StatusResponse:
        """
        Revoke the API key in use in the event it is compromised.

        Returns
        -------
        StatusResponse
            If the HTTP response code is 200 and the status message is "OK",
            then the key has been revoked and any further requests will be
            rejected.
            Any other status code or message indicates an error has
            occurred and the errors array will give further details.
        """
        resp = self.get("/auth/revoke")
        self._header = resp.headers
        return StatusResponse(**resp.json())

    # Sub APIs
    @property
    def plan(self):
        """
        Alias for PlanAPI()
        """
        return PlanAPI(self)

    @property
    def user(self):
        """
        Alias for UserAPI()
        """
        return UserAPI(self)

    @property
    def tags(self):
        """
        Alias for TagsAPI()
        """
        return TagsAPI(self)

    @property
    def nav(self):
        """
        Alias for NavAPI()
        """
        return NavAPI(self)

    @property
    def weather(self):
        """
        Alias for WeatherAPI()
        """
        return WeatherAPI(self)


class PlanAPI():

    """
    Flightplan-related commands
    """

    # TODO: params
    #   allow flight plan return format to be specified by user
    def __init__(self, flightplandb: FlightPlanDB):
        """Summary

        Parameters
        ----------
        flightplandb : FlightPlanDB
            Description
        """
        self._fp = flightplandb

    def fetch(self, id_: int,
              return_format: str = "dict") -> Union[Plan, bytes]:
        """
        Fetches a flight plan and its associated attributes by ID.
        Returns it in specified format.

        Parameters
        ----------
        id_ : int
            Description
        return_format : str, optional
            Description

        Returns
        -------
        Union[Plan, bytes]
            Description
        """
        request = self._fp.get(f"/plan/{id_}", return_format=return_format)
        if return_format == "dict":
            return Plan(**request)

        return request  # if the format is not a dict

    def create(self, plan: Plan, return_format: str = "dict") -> Plan:
        """
        Creates a new flight plan.

        Parameters
        ----------
        plan : Plan
            Description
        return_format : str, optional
            Description

        Returns
        -------
        Plan
            Description
        """
        return Plan(**self._fp.post("/plan", json=asdict(plan)))

    def edit(self, plan: Plan) -> Plan:
        """
        Edits a flight plan linked to your account.

        Parameters
        ----------
        plan : Plan
            Description

        Returns
        -------
        Plan
            Description
        """
        return Plan(**self._fp.patch(f"/plan/{plan.id}", json=asdict(plan)))

    def delete(self, id_: int) -> StatusResponse:
        """
        Deletes a flight plan that is linked to your account.

        Parameters
        ----------
        id_ : int
            Description

        Returns
        -------
        StatusResponse
            Description
        """
        return StatusResponse(**self._fp.delete(f"/plan/{id_}"))

    def search(self, plan_query: PlanQuery,
               limit: int = 100) -> Generator[Plan, None, None]:
        """
        Searches for flight plans.
        A number of search parameters are available.
        They will be combined to form a search request.

        Parameters
        ----------
        plan_query : PlanQuery
            Description
        limit : int, optional
            Description

        Yields
        ------
        Generator[Plan, None, None]
            Description
        """
        for i in self._fp.getiter("/search/plans",
                                  params=plan_query.as_dict(),
                                  limit=limit):
            yield Plan(**i)

    def has_liked(self, id_: int) -> bool:
        """
        Fetches your like status for a flight plan.

        Parameters
        ----------
        id_ : int
            Description

        Returns
        -------
        bool
            Description
        """
        sr = StatusResponse(
            **self._fp.get(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def like(self, id_: int) -> StatusResponse:
        """
        Likes a flight plan.

        Parameters
        ----------
        id_ : int
            Description

        Returns
        -------
        StatusResponse
            Description
        """
        return StatusResponse(**self._fp.post(f"/plan/{id_}/like"))

    def unlike(self, id_: int) -> bool:
        """
        Removes a flight plan like.

        Parameters
        ----------
        id_ : int
            Description

        Returns
        -------
        bool
            Description
        """
        sr = StatusResponse(
            **self._fp.delete(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def generate(self, gen_query: GenerateQuery) -> Plan:
        """
        Creates a new flight plan using the route generator.

        Parameters
        ----------
        gen_query : GenerateQuery
            Description

        Returns
        -------
        Plan
            Description
        """
        return Plan(
            **self._fp.patch(
                "/auto/generate", json=asdict(gen_query)))

    def decode(self, route: str) -> Plan:
        """
        Creates a new flight plan using the route decoder.

        Parameters
        ----------
        route : str
            Description

        Returns
        -------
        Plan
            Description
        """
        return Plan(**self._fp.post(
            "/auto/decode", json={"route": route}))


class UserAPI:

    """
    Commands related to registered users
    """

    def __init__(self, flightplandb: FlightPlanDB):
        """Summary

        Parameters
        ----------
        flightplandb : FlightPlanDB
            Description
        """
        self._fp = flightplandb

    @property
    def me(self) -> User:
        """
        Fetches profile information for the currently authenticated user.

        Returns
        -------
        User
            Description
        """
        return User(**self._fp.get("/me"))

    def key_revoke(self) -> StatusResponse:
        """
        Use this endpoint to manually revoke an API key if it is compromised.
        If the HTTP response code is 200 and the status message is "OK",
        then the key has been revoked; any further requests will be rejected.
        Any other status code or message indicates an error has occurred.
        In that case, the errors array will give further details.

        Returns
        -------
        StatusResponse
            Description
        """
        return StatusResponse(**self._fp.get("/auth/revoke"))

    def fetch(self, username: str) -> User:
        """
        Fetches profile information for any registered user

        Parameters
        ----------
        username : str
            Description

        Returns
        -------
        User
            Description
        """
        return User(**self._fp.get(f"user/{username}"))

    def plans(self, username: str,
              limit: int = 100) -> Generator[Plan, None, None]:
        """
        Fetches flight plans created by a user.

        Parameters
        ----------
        username : str
            Description
        limit : int, optional
            Description

        Yields
        ------
        Generator[Plan, None, None]
            Description
        """
        # TODO: params
        #   page The page of results to fetch
        #   limit [20] The number of plans to return per page (max 100)
        #   sort The order of the returned plans
        for i in self._fp.getiter(f"/user/{username}/plans",
                                  limit=limit):
            yield Plan(**i)

    def likes(self, username: str,
              limit: int = 100) -> Generator[Plan, None, None]:
        """
        Fetches flight plans created by a user.

        Parameters
        ----------
        username : str
            Description
        limit : int, optional
            Description

        Yields
        ------
        Generator[Plan, None, None]
            Description
        """
        # TODO: params
        #   page The page of results to fetch
        #   limit [20] The number of plans to return per page (max 100)
        #   sort The order of the returned plans
        for i in self._fp.getiter(f"/user/{username}/likes",
                                  limit=limit):
            yield Plan(**i)

    def search(self, username: str) -> Generator[User, None, None]:
        """
        Searches for users by username.

        Parameters
        ----------
        username : str
            Description

        Yields
        ------
        Generator[User, None, None]
            Description
        """
        for i in self._fp.getiter("/search/users",
                                  limit=limit,
                                  params={"q": username}):
            yield User(**i)


class TagsAPI:

    """
    Related to flight plans
    """

    def __init__(self, flightplandb: FlightPlanDB):
        """Summary

        Parameters
        ----------
        flightplandb : FlightPlanDB
            Description
        """
        self._fp = flightplandb

    def fetch(self) -> List[Tag]:
        """
        Fetches current popular tags from all flight plans.
        Only tags with sufficient popularity are included

        Returns
        -------
        List[Tag]
            Description
        """
        return list(map(lambda t: Tag(**t), self._fp.get("/tags")))


class NavAPI:

    """
    Commands related to navigation aids and airports
    """

    def __init__(self, flightplandb: FlightPlanDB):
        """Summary

        Parameters
        ----------
        flightplandb : FlightPlanDB
            Description
        """
        self._fp = flightplandb

    def airport(self, icao) -> Airport:
        """
        Fetches information about an airport.

        Parameters
        ----------
        icao : TYPE
            Description

        Returns
        -------
        Airport
            Description
        """
        return Airport(**self._fp.get(f"/nav/airport/{icao}"))

    def nats(self) -> List[Track]:
        """
        Fetches current North Atlantic Tracks.

        Returns
        -------
        List[Track]
            Description
        """
        return list(
            map(lambda n: Track(**n), self._fp.get("/nav/NATS")))

    def pacots(self) -> List[Track]:
        """
        Fetches current Pacific Organized Track System tracks.

        Returns
        -------
        List[Track]
            Description
        """
        return list(
            map(lambda t: Track(**t), self._fp.get("/nav/PACOTS")))

    def search(self, q: str,
               type_: str = None) -> Generator[Navaid, None, None]:
        """
        Searches navaids using a query.

        Parameters
        ----------
        q : str
            Description
        type_ : str, optional
            Description

        Yields
        ------
        Generator[Navaid, None, None]
            Description

        Raises
        ------
        ValueError
            Description
        ValueError
        Description
        """
        params = {"q": q}
        if type_:
            if type_ in Navaid.validtypes:
                params["types"] = type_
            else:
                raise ValueError(f"{type_} is not a valid Navaid type")
        for i in self._fp.getiter("/search/nav", params=params):
            yield Navaid(**i)


class WeatherAPI:

    """
    Weather. I mean, how much is there to say?
    """

    def __init__(self, flightplandb: FlightPlanDB):
        """Summary

        Parameters
        ----------
        flightplandb : FlightPlanDB
            Description
        """
        self._fp = flightplandb

    def fetch(self, icao: str) -> Weather:
        """
        Fetches current weather conditions at an airport

        Parameters
        ----------
        icao : str
            Description

        Returns
        -------
        Weather
            Description
        """
        return Weather(**self._fp.get(f"/weather/{icao}"))


def test_run():
    """Summary
    """
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
