#!/usr/bin/env python

from typing import Generator, List, Dict, Union, Optional
from dataclasses import asdict

from urllib.parse import urljoin
import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict

from flightplandb.datatypes import (
    StatusResponse,
    PlanQuery, Plan, GenerateQuery,
    User, Tag,
    Airport, Track, Navaid,
    Weather
)


# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoclass
class FlightPlanDB:

    """Base functions called by other parts of the API.
    All of the functions in here are for internal use only, except for
    ping(), revoke() and the properties.
    """

    def __init__(
            self, key: str,
            url_base: str = "https://api.flightplandatabase.com"):
        """To get an API key, visit your account settings page.
        Your account will need a verified email address to add an API key.
        https://flightplandatabase.com/settings

        :param key: api token
        :type key: str
        :param url_base:
            The host of the API endpoint URL,
            defaults to "https://api.flightplandatabase.com"
        :type url_base: str, optional
        """
        self.key: str = key
        self._header: CaseInsensitiveDict[str] = CaseInsensitiveDict()
        self.url_base = url_base

    def request(self, method: str,
                path: str, return_format="dict",
                ignore_statuses: Optional[List] = None,
                params: Optional[Dict] = None,
                *args, **kwargs) -> Union[Dict, bytes]:
        """General HTTP requests function for non-paginated results.

        :param method: An HTTP request type. One of GET, POST, PATCH, or DELETE
        :type method: str
        :param path: The endpoint's path to which the request is being made
        :type path: str
        :param return_format: The API response format, defaults to "dict"
        :type return_format: str, optional
        :param ignore_statuses:
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        :type ignore_statuses: Optional[List], optional
        :param params: Any other HTTP request parameters, defaults to None
        :type params: Optional[Dict], optional
        :raises ValueError: Invalid return_format option
        :raises HTTPError: Invalid HTTP status in response
        :return: A dict if return_format is dict, otherwise bytes
        :rtype: Union[Dict, bytes]
        """
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

        if not ignore_statuses:
            ignore_statuses = []
        if not params:
            params = {}

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
    def get(self, path: str, return_format="dict",
            ignore_statuses: Optional[List] = None,
            params: Optional[Dict] = None,
            *args, **kwargs):
        """Calls request() for get requests.

        :param path: The endpoint's path to which the request is being made
        :type path: str
        :param return_format: The API response format, defaults to "dict"
        :type return_format: str, optional
        :param ignore_statuses:
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        :type ignore_statuses: Optional[List], optional
        :param params: Any other HTTP request parameters, defaults to None
        :type params: Optional[Dict], optional
        :raises: [description]
        :return: [description]
        :rtype: [type]
        """
        # I HATE not being able to set empty lists as default arguments
        if not ignore_statuses:
            ignore_statuses = []
        if not params:
            params = {}

        resp = self.request("get", path,
                            return_format,
                            ignore_statuses,
                            params,
                            *args, **kwargs)
        return resp

    def post(self, path: str, return_format="dict",
             ignore_statuses: Optional[List] = None,
             params: Optional[Dict] = None,
             *args, **kwargs):
        """Calls request() for post requests.

        :param path: The endpoint's path to which the request is being made
        :type path: str
        :param return_format: The API response format, defaults to "dict"
        :type return_format: str, optional
        :param ignore_statuses:
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        :type ignore_statuses: Optional[List], optional
        :param params: Any other HTTP request parameters, defaults to None
        :type params: Optional[Dict], optional
        :raises: [description]
        :return: [description]
        :rtype: [type]
        """
        if not ignore_statuses:
            ignore_statuses = []
        if not params:
            params = {}

        resp = self.request("post",
                            path,
                            return_format,
                            ignore_statuses,
                            params,
                            *args, **kwargs)
        return resp

    def patch(self, path: str, return_format="dict",
              ignore_statuses: Optional[List] = None,
              params: Optional[Dict] = None,
              *args, **kwargs):
        """Calls request() for patch requests.

        :param path: The endpoint's path to which the request is being made
        :type path: str
        :param return_format: The API response format, defaults to "dict"
        :type return_format: str, optional
        :param ignore_statuses:
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        :type ignore_statuses: Optional[List], optional
        :param params: Any other HTTP request parameters, defaults to None
        :type params: Optional[Dict], optional
        :raises: [description]
        :return: [description]
        :rtype: [type]
        """
        if not ignore_statuses:
            ignore_statuses = []
        if not params:
            params = {}

        resp = self.request("patch",
                            path,
                            return_format,
                            ignore_statuses,
                            params,
                            *args, **kwargs)
        return resp

    def delete(self, path: str, return_format="dict",
               ignore_statuses: Optional[List] = None,
               params: Optional[Dict] = None,
               *args, **kwargs):
        """Calls request() for delete requests.

        :param path: The endpoint's path to which the request is being made
        :type path: str
        :param return_format: The API response format, defaults to "dict"
        :type return_format: str, optional
        :param ignore_statuses:
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        :type ignore_statuses: Optional[List], optional
        :param params: Any other HTTP request parameters, defaults to None
        :type params: Optional[Dict], optional
        :raises: [description]
        :return: [description]
        :rtype: [type]
        """
        if not ignore_statuses:
            ignore_statuses = []
        if not params:
            params = {}

        resp = self.request("delete",
                            path,
                            return_format,
                            ignore_statuses,
                            params,
                            *args, **kwargs)
        return resp

    def getiter(self, path: str,
                limit=100,
                ignore_statuses: Optional[List] = None,
                params: Optional[Dict] = None,
                *args, **kwargs) -> Generator[Dict, None, None]:
        """Get requests function for paginated results.

        :param path:
            The endpoint's path to which the request is being made
        :type path: str
        :param limit:
            Maximum number of results to return, defaults to 100
        :type limit: int, optional
        :param ignore_statuses:
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        :type ignore_statuses: Optional[List], optional
        :param params:
            Any other HTTP request parameters, defaults to None
        :type params: Optional[Dict], optional
        :raises: [description]
        :yield: [description]
        :rtype: Generator[Dict, None, None]
        """
        if not ignore_statuses:
            ignore_statuses = []
        if not params:
            params = {}

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
            for i in r_fpdb.json():
                # ...and return every dictionary in there...
                yield i
                num_results += 1
                # ...unless the result limit has been reached
                if num_results == limit:
                    return

    def _header_value(self, header_key: str) -> str:
        """Gets header value for key

        :param header_key: One of the HTTP header keys
        :type header_key: str
        :return: The value corresponding to the passed key
        :rtype: str
        """
        if header_key not in self._header:
            self.ping()  # Make at least one request
        return self._header[header_key]

    @property
    def api_version(self) -> int:
        """API version that returned the response

        :return: API version
        :rtype: int
        """
        return int(self._header_value("X-API-Version"))

    @property
    def units(self) -> str:
        """The units system used for numeric values.
        https://flightplandatabase.com/dev/api#units

        :return: AVIATION, METRIC or SI
        :rtype: str
        """
        return self._header_value("X-Units")

    @property
    def limit_cap(self) -> int:
        """The number of requests allowed per day, operated on an hourly rolling
        basis. i.e Requests used between 19:00 and 20:00 will become available
        again at 19:00 the following day. API key authenticated requests get a
        higher daily rate limit and can be raised if a compelling
        use case is presented.

        :return: number of allowed requests per day
        :rtype: int
        """
        return int(self._header_value("X-Limit-Cap"))

    @property
    def limit_used(self) -> int:
        """The number of requests used in the current period
        by the presented API key or IP address

        :return: number of requests used in period
        :rtype: int
        """
        return int(self._header_value("X-Limit-Used"))

    def ping(self) -> StatusResponse:
        """Checks API status to see if it is up

        :return: OK 200 means the service is up and running.
        :rtype: StatusResponse

        """
        resp = self.get("")
        return StatusResponse(**resp)

    def revoke(self) -> StatusResponse:
        """Revoke the API key in use in the event it is compromised.

        :return:
            If the HTTP response code is 200 and the status message is "OK",
            then the key has been revoked and any further requests will be
            rejected.
            Any other status code or message indicates an error has
            occurred and the errors array will give further details.
        :rtype: StatusResponse

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

    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def fetch(self, id_: int,
              return_format: str = "dict") -> Union[Plan, bytes]:
        """Fetches a flight plan and its associated attributes by ID.
        Returns it in specified format.

        :param id_: Description of parameter `id_`.
        :type id_: int
        :param return_format: Description of parameter `return_format`.
        :type return_format: str
        :return: Description of returned object.
        :rtype: Union[Plan, bytes]

        """
        request = self._fp.get(f"/plan/{id_}", return_format=return_format)
        if return_format == "dict":
            return Plan(**request)

        return request  # if the format is not a dict

    def create(self, plan: Plan, return_format: str = "dict") -> Plan:
        """Creates a new flight plan.

        :param plan: Description of parameter `plan`.
        :type plan: Plan
        :param return_format: Description of parameter `return_format`.
        :type return_format: str
        :return: Description of returned object.
        :rtype: Plan

        """
        return Plan(**self._fp.post("/plan",
                    return_format=return_format,
                    json=asdict(plan)))

    def edit(self, plan: Plan) -> Plan:
        """Edits a flight plan linked to your account.

        :param plan: Description of parameter `plan`.
        :type plan: Plan
        :return: Description of returned object.
        :rtype: Plan

        """
        return Plan(**self._fp.patch(f"/plan/{plan.id}", json=asdict(plan)))

    def delete(self, id_: int) -> StatusResponse:
        """Deletes a flight plan that is linked to your account.

        :param id_: Description of parameter `id_`.
        :type id_: int
        :return: Description of returned object.
        :rtype: StatusResponse

        """
        return StatusResponse(**self._fp.delete(f"/plan/{id_}"))

    def search(self, plan_query: PlanQuery,
               limit: int = 100) -> Generator[Plan, None, None]:
        """Searches for flight plans.
        A number of search parameters are available.
        They will be combined to form a search request.

        :param plan_query: Description of parameter `plan_query`.
        :type plan_query: PlanQuery
        :param limit: Description of parameter `limit`.
        :type limit: int
        :return: Description of returned object.
        :rtype: Generator[Plan, None, None]

        """
        for i in self._fp.getiter("/search/plans",
                                  params=plan_query.as_dict(),
                                  limit=limit):
            yield Plan(**i)

    def has_liked(self, id_: int) -> bool:
        """Fetches your like status for a flight plan.

        :param id_: Description of parameter `id_`.
        :type id_: int
        :return: Description of returned object.
        :rtype: bool

        """
        sr = StatusResponse(
            **self._fp.get(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def like(self, id_: int) -> StatusResponse:
        """Likes a flight plan.

        :param id_: Description of parameter `id_`.
        :type id_: int
        :return: Description of returned object.
        :rtype: StatusResponse

        """
        return StatusResponse(**self._fp.post(f"/plan/{id_}/like"))

    def unlike(self, id_: int) -> bool:
        """Removes a flight plan like.

        :param id_: Description of parameter `id_`.
        :type id_: int
        :return: Description of returned object.
        :rtype: bool

        """
        sr = StatusResponse(
            **self._fp.delete(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def generate(self, gen_query: GenerateQuery) -> Plan:
        """Creates a new flight plan using the route generator.

        :param gen_query: Description of parameter `gen_query`.
        :type gen_query: GenerateQuery
        :return: Description of returned object.
        :rtype: Plan

        """
        return Plan(
            **self._fp.patch(
                "/auto/generate", json=asdict(gen_query)))

    def decode(self, route: str) -> Plan:
        """Creates a new flight plan using the route decoder.

        :param route: Description of parameter `route`.
        :type route: str
        :return: Description of returned object.
        :rtype: Plan

        """
        return Plan(**self._fp.post(
            "/auto/decode", json={"route": route}))


class UserAPI:

    """
    Commands related to registered users
    """

    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    @property
    def me(self) -> User:
        """Fetches profile information for the currently authenticated user.

        :return: Description of returned object.
        :rtype: User

        """
        return User(**self._fp.get("/me"))

    def key_revoke(self) -> StatusResponse:
        """Use this endpoint to manually revoke an API key if it is compromised.
        If the HTTP response code is 200 and the status message is "OK",
        then the key has been revoked; any further requests will be rejected.
        Any other status code or message indicates an error has occurred.
        In that case, the errors array will give further details.

        :return: Description of returned object.
        :rtype: StatusResponse

        """
        return StatusResponse(**self._fp.get("/auth/revoke"))

    def fetch(self, username: str) -> User:
        """Fetches profile information for any registered user

        :param username: Description of parameter `username`.
        :type username: str
        :return: Description of returned object.
        :rtype: User

        """
        return User(**self._fp.get(f"user/{username}"))

    def plans(self, username: str,
              limit: int = 100) -> Generator[Plan, None, None]:
        """Fetches flight plans created by a user.

        :param username: Description of parameter `username`.
        :type username: str
        :param limit: Description of parameter `limit`.
        :type limit: int
        :return: Description of returned object.
        :rtype: Generator[Plan, None, None]

        """
        # TODO: params
        #   sort The order of the returned plans
        for i in self._fp.getiter(f"/user/{username}/plans",
                                  limit=limit):
            yield Plan(**i)

    def likes(self, username: str,
              limit: int = 100) -> Generator[Plan, None, None]:
        """Fetches flight plans created by a user.

        :param username: Description of parameter `username`.
        :type username: str
        :param limit: Description of parameter `limit`.
        :type limit: int
        :return: Description of returned object.
        :rtype: Generator[Plan, None, None]

        """
        # TODO: params
        #   sort The order of the returned plans
        for i in self._fp.getiter(f"/user/{username}/likes",
                                  limit=limit):
            yield Plan(**i)

    def search(self, username: str, limit=100) -> Generator[User, None, None]:
        """Searches for users by username.

        :param username: Description of parameter `username`.
        :type username: str
        :param limit: Description of parameter `limit`.
        :type limit: type
        :return: Description of returned object.
        :rtype: Generator[User, None, None]

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
        self._fp = flightplandb

    def fetch(self) -> List[Tag]:
        """Fetches current popular tags from all flight plans.
        Only tags with sufficient popularity are included

        :return: Description of returned object.
        :rtype: List[Tag]

        """
        return list(map(lambda t: Tag(**t), self._fp.get("/tags")))


class NavAPI:

    """
    Commands related to navigation aids and airports
    """

    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def airport(self, icao) -> Airport:
        """Fetches information about an airport.

        :param icao: Description of parameter `icao`.
        :type icao: type
        :return: Description of returned object.
        :rtype: Airport

        """
        return Airport(**self._fp.get(f"/nav/airport/{icao}"))

    def nats(self) -> List[Track]:
        """Fetches current North Atlantic Tracks.

        :return: Description of returned object.
        :rtype: List[Track]

        """
        return list(
            map(lambda n: Track(**n), self._fp.get("/nav/NATS")))

    def pacots(self) -> List[Track]:
        """Fetches current Pacific Organized Track System tracks.

        :return: Description of returned object.
        :rtype: List[Track]

        """
        return list(
            map(lambda t: Track(**t), self._fp.get("/nav/PACOTS")))

    def search(self, query: str,
               type_: str = None) -> Generator[Navaid, None, None]:
        """Searches navaids using a query.

        :param query: Description of parameter `query`.
        :type query: str
        :param type_: Description of parameter `type_`.
        :type type_: str
        :return: Description of returned object.
        :rtype: Generator[Navaid, None, None]

        """
        params = {"q": query}
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
        self._fp = flightplandb

    def fetch(self, icao: str) -> Weather:
        """Fetches current weather conditions at an airport

        :param icao: Description of parameter `icao`.
        :type icao: str
        :return: Description of returned object.
        :rtype: Weather

        """
        return Weather(**self._fp.get(f"/weather/{icao}"))
