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
    :meth:`ping()`, :meth:`revoke()` and the properties.

    Parameters
    ----------
    key : str
        API token
    url_base : str
        The host of the API endpoint URL,
        defaults to https://api.flightplandatabase.com
    """

    def __init__(
            self, key: str,
            url_base: str = "https://api.flightplandatabase.com"):
        self.key: str = key
        self._header: CaseInsensitiveDict[str] = CaseInsensitiveDict()
        self.url_base = url_base

    def request(self, method: str,
                path: str, return_format="dict",
                ignore_statuses: Optional[List] = None,
                params: Optional[Dict] = None,
                *args, **kwargs) -> Union[Dict, bytes]:
        """General HTTP requests function for non-paginated results.

        Parameters
        ----------
        method : str
            An HTTP request type. One of GET, POST, PATCH, or DELETE
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"dict"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dict`` if ``return_format`` is ``"dict"``, otherwise ``bytes``

        Raises
        ------
        ValueError
            Invalid return_format option
        HTTPError
            Invalid HTTP status in response
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
            *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`request()` for get requests.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"dict"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dict`` if ``return_format`` is ``"dict"``, otherwise ``bytes``
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
             *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`request()` for post requests.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"dict"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dict`` if ``return_format`` is ``"dict"``, otherwise ``bytes``
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
              *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`request()` for patch requests.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"dict"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dict`` if ``return_format`` is ``"dict"``, otherwise ``bytes``
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
               *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`request()` for delete requests.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"dict"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dict`` if ``return_format`` is ``"dict"``, otherwise ``bytes``
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
        """Get :meth:`request()` for paginated results.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        limit : int, optional
            Maximum number of results to return, defaults to 100
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Generator[Dict, None, None]
            A generator of dicts. Return format cannot be specified.
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

        Parameters
        ----------
        header_key : str
            One of the HTTP header keys

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
        """API version that returned the response

        Returns
        -------
        int
            API version
        """
        return int(self._header_value("X-API-Version"))

    @property
    def units(self) -> str:
        """The units system used for numeric values.
        https://flightplandatabase.com/dev/api#units

        Returns
        -------
        str
            AVIATION, METRIC or SI
        """
        return self._header_value("X-Units")

    @property
    def limit_cap(self) -> int:
        """The number of requests allowed per day, operated on an hourly rolling
        basis. i.e requests used between 19:00 and 20:00 will become available
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
        """The number of requests used in the current period
        by the presented API key or IP address

        Returns
        -------
        int
            number of requests used in period
        """
        return int(self._header_value("X-Limit-Used"))

    def ping(self) -> StatusResponse:
        """Checks API status to see if it is up

        Returns
        -------
        StatusResponse
            OK 200 means the service is up and running.
        """
        resp = self.get("")
        return StatusResponse(**resp)

    def revoke(self) -> StatusResponse:
        """Revoke the API key in use in the event it is compromised.

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
        """Alias for :class:`PlanAPI()`"""
        return PlanAPI(self)

    @property
    def user(self):
        """Alias for :class:`UserAPI()`"""
        return UserAPI(self)

    @property
    def tags(self):
        """Alias for :class:`TagsAPI()`"""
        return TagsAPI(self)

    @property
    def nav(self):
        """Alias for :class:`NavAPI()`"""
        return NavAPI(self)

    @property
    def weather(self):
        """Alias for :class:`WeatherAPI()`"""
        return WeatherAPI(self)


class PlanAPI():

    """Flightplan-related commands"""

    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def fetch(self, id_: int,
              return_format: str = "dict") -> Union[Plan, None, bytes]:
        """Fetches a flight plan and its associated attributes by ID.
        Returns it in specified format.

        Parameters
        ----------
        id\_ : int
            The ID of the flight plan to fetch
        return_format : str
            The API response format, defaults to ``"dict"``

        Returns
        -------
        Union[Plan, None, bytes]
            :class:`~flightplandb.datatypes.Plan` by default or if ``"dict"``
            is specified as the ``return_format``.

            ``bytes`` if a different format than ``"dict"`` was specified.

            ``None`` if the plan with that id was not found.
        """
        try:
            request = self._fp.get(f"/plan/{id_}", return_format=return_format)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                raise e

        if return_format == "dict":
            return Plan(**request)

        return request  # if the format is not a dict

    def create(self, plan: Plan,
               return_format: str = "dict") -> Union[Plan, bytes]:
        """Creates a new flight plan.

        Parameters
        ----------
        plan : Plan
            The Plan object to register on the website
        return_format : str
            The API response format, defaults to ``"dict"``

        Returns
        -------
        Union[Plan, bytes]
            :class:`~flightplandb.datatypes.Plan` by default or if ``"dict"``
            is specified as the ``return_format``.

            ``bytes`` if a different format than ``"dict"`` was specified.
        """
        request = self._fp.post(f"/plan/", return_format=return_format)

        if return_format == "dict":
            return Plan(**request)

        return request

    def edit(self, plan: Plan,
             return_format: str = "dict") -> Union[Plan, bytes]:
        """Edits a flight plan linked to your account.

        Parameters
        ----------
        plan : Plan
            The new Plan object to replace the old one associated with that ID
        return_format : str
            The API response format, defaults to ``"dict"``

        Returns
        -------
        Union[Plan, bytes]
            :class:`~flightplandb.datatypes.Plan` by default or if ``"dict"``
            is specified as the ``return_format``.

            ``bytes`` if a different format than ``"dict"`` was specified.
        """
        request = self._fp.patch(f"/plan/{plan.id}", json=asdict(plan))

        if return_format == "dict":
            return Plan(**request)

        return request

    def delete(self, id_: int) -> StatusResponse:
        """Deletes a flight plan that is linked to your account.

        Parameters
        ----------
        id\_ : int
            The ID of the flight plan to delete

        Returns
        -------
        StatusResponse
            OK 200 means a successful delete
        """
        return StatusResponse(**self._fp.delete(f"/plan/{id_}"))

    def search(self, plan_query: PlanQuery,
               limit: int = 100) -> Generator[Plan, None, None]:
        """Searches for flight plans.
        A number of search parameters are available.
        They will be combined to form a search request.

        Parameters
        ----------
        plan_query : PlanQuery
            A dataclass containing multiple options for plan searches
        limit : int
            Maximum number of plans to return, defaults to 100

        Yields
        -------
        Generator[Plan, None, None]
            A generator containing :class:`~flightplandb.datatypes.Plan`
            objects.
            Each plan's :py:obj:`~flightplandb.datatypes.Plan.route`
            will be set to ``None`` unless otherwise specified in the
            :py:obj:`~flightplandb.datatypes.PlanQuery.includeRoute` parameter
            of the :class:`~flightplandb.datatypes.PlanQuery` used to request it
        """
        for i in self._fp.getiter("/search/plans",
                                  params=plan_query.as_dict(),
                                  limit=limit):
            yield Plan(**i)

    def has_liked(self, id_: int) -> bool:
        """Fetches your like status for a flight plan.

        Parameters
        ----------
        id\_ : int
            ID of the flightplan to be checked

        Returns
        -------
        bool
            ``True``/``False`` to indicate that the plan was liked / not liked
        """
        sr = StatusResponse(
            **self._fp.get(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def like(self, id_: int) -> StatusResponse:
        """Likes a flight plan.

        Parameters
        ----------
        id\_ : int
            ID of the flightplan to be liked

        Returns
        -------
        StatusResponse
            201 means the plan was successfully liked.
            200 means the plan was already liked.
        """
        return StatusResponse(**self._fp.post(f"/plan/{id_}/like"))

    def unlike(self, id_: int) -> bool:
        """Removes a flight plan like.

        Parameters
        ----------
        id\_ : int
            ID of the flightplan to be unliked

        Returns
        -------
        bool
            ``True`` for a successful unlike, ``False`` indicates a failure
        """
        sr = StatusResponse(
            **self._fp.delete(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def generate(self, gen_query: GenerateQuery,
                 return_format: str = "dict") -> Union[Plan, bytes]:
        """Creates a new flight plan using the route generator.

        Parameters
        ----------
        gen_query : GenerateQuery
            A dataclass with options for flight plan generation
        return_format : str
            The API response format, defaults to ``"dict"``

        Returns
        -------
        Union[Plan, bytes]
            Plan by default or if ``"dict"`` is specified as
            the ``return_format``.

            Bytes if a different format than ``"dict"`` was specified
        """
        return Plan(
            **self._fp.post(
                "/auto/generate", json=asdict(gen_query)))

    def decode(self, route: str) -> Plan:
        """Creates a new flight plan using the route decoder.

        Parameters
        ----------
        route : str
            The route to decode. Use a comma or space separated string of
            waypoints, beginning and ending with valid airport ICAOs
            (e.g. KSAN BROWS TRM LRAIN KDEN). Airways are supported if they
            are preceded and followed by valid waypoints on the airway
            (e.g. 06TRA UL851 BEGAR). SID and STAR procedures are not
            currently supported and will be skipped, along with any
            other unmatched waypoints.

        Returns
        -------
        Plan
            The registered flight plan created on flight plan database,
            corresponding to the decoded route
        """
        return Plan(**self._fp.post(
            "/auto/decode", json={"route": route}))


class UserAPI:

    """Commands related to registered users"""

    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    @property
    def me(self) -> User:
        """Fetches profile information for the currently authenticated user.

        Returns
        -------
        User
            The User object of the currently authenticated user
        """
        return User(**self._fp.get("/me"))

    def key_revoke(self) -> StatusResponse:
        """Use this endpoint to manually revoke an API key if it is compromised.
        If the HTTP response code is ``200`` and the status message is ``"OK"``,
        then the key has been revoked; any further requests will be rejected.
        Any other status code or message indicates an error has occurred.
        In that case, the errors array will give further details.

        Returns
        -------
        StatusResponse
            200 OK for a successful key revoke
        """
        return StatusResponse(**self._fp.get("/auth/revoke"))

    def fetch(self, username: str) -> User:
        """Fetches profile information for any registered user

        Parameters
        ----------
        username : str
            Username of the registered User

        Returns
        -------
        User
            The User object of the user associated with the username
        """
        return User(**self._fp.get(f"user/{username}"))

    def plans(self, username: str,
              limit: int = 100) -> Generator[Plan, None, None]:
        """Fetches flight plans created by a user.

        Parameters
        ----------
        username : str
            Username of the user who created the flight plans
        limit: int
            Maximum number of plans to fetch, defaults to ``100``

        Yields
        -------
        Generator[Plan, None, None]
            A generator with all the flight plans a user created,
            limited by ``limit``
        """
        # TODO: params
        #   sort The order of the returned plans
        for i in self._fp.getiter(f"/user/{username}/plans",
                                  limit=limit):
            yield Plan(**i)

    def likes(self, username: str,
              limit: int = 100) -> Generator[Plan, None, None]:
        """Fetches flight plans liked by a user.

        Parameters
        ----------
        username : str
            Username of the user who liked the flight plans
        limit : int
            Maximum number of plans to fetch, defaults to ``100``

        Yields
        -------
        Generator[Plan, None, None]
            A generator with all the flight plans a user liked,
            limited by ``limit``
        """
        # TODO: params
        #   sort The order of the returned plans
        for i in self._fp.getiter(f"/user/{username}/likes",
                                  limit=limit):
            yield Plan(**i)

    def search(self, username: str, limit=100) -> Generator[User, None, None]:
        """Searches for users by username. For more detailed info on a
        specific user, use :meth:`fetch`

        Parameters
        ----------
        username : str
            Username to search user database for
        limit : type
            Maximum number of users to fetch, defaults to ``100``

        Yields
        -------
        Generator[User, None, None]
            A generator with a list of users approximately matching
            ``username``, limited by ``limit``
        """
        for i in self._fp.getiter("/search/users",
                                  limit=limit,
                                  params={"q": username}):
            yield User(**i)


class TagsAPI:

    """Related to flight plans"""

    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def fetch(self) -> List[Tag]:
        """Fetches current popular tags from all flight plans.
        Only tags with sufficient popularity are included
        """
        return list(map(lambda t: Tag(**t), self._fp.get("/tags")))


class NavAPI:

    """Commands related to navigation aids and airports"""

    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def airport(self, icao) -> Airport:
        """Fetches information about an airport.

        Parameters
        ----------
        icao : type
            The airport ICAO to fetch information for

        Returns
        -------
        Airport
            An oversized dataclass with more information than you'd
            need in 500 years.
        """
        return Airport(**self._fp.get(f"/nav/airport/{icao}"))

    def nats(self) -> List[Track]:
        """Fetches current North Atlantic Tracks.

        Returns
        -------
        List[Track]
            List of NATs
        """
        return list(
            map(lambda n: Track(**n), self._fp.get("/nav/NATS")))

    def pacots(self) -> List[Track]:
        """Fetches current Pacific Organized Track System tracks.

        Returns
        -------
        List[Track]
            List of PACOTs
        """
        return list(
            map(lambda t: Track(**t), self._fp.get("/nav/PACOTS")))

    def search(self, query: str,
               type_: str = None) -> Generator[Navaid, None, None]:
        """Searches navaids using a query.

        Parameters
        ----------
        query : str
            The search query. Searches the navaid identifier and navaid name
        type_ : str
            Navaid type.
            Must be either ``None`` (default value, returns all types) or one
            of :py:obj:`~flightplandb.datatypes.Navaid.validtypes`

        Yields
        -------
        Generator[Navaid, None, None]
            A generator of navaids with either a name or ident
            matching the ``query``
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

    """Weather. I mean, how much is there to say?"""

    def __init__(self, flightplandb: FlightPlanDB):
        self._fp = flightplandb

    def fetch(self, icao: str) -> Weather:
        """
        Fetches current weather conditions at an airport

        Parameters
        ----------
        icao : str
            ICAO code of the airport for which the weather will be fetched

        Returns
        -------
        Weather
            METAR and TAF for an airport
        """
        return Weather(**self._fp.get(f"/weather/{icao}"))
