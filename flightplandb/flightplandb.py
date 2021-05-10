#!/usr/bin/env python

# Copyright 2021 PH-KDX
# This file is part of FlightplanDB-py.

# FlightplanDB-py is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FlightplanDB-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with FlightplanDB-py.  If not, see <https://www.gnu.org/licenses/>.

from typing import Generator, List, Dict, Union, Optional

from urllib.parse import urljoin
import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict

import json
from flightplandb.exceptions import status_handler

from flightplandb.datatypes import StatusResponse

from flightplandb.submodules.plan import PlanAPI
from flightplandb.submodules.user import UserAPI
from flightplandb.submodules.tags import TagsAPI
from flightplandb.submodules.nav import NavAPI
from flightplandb.submodules.weather import WeatherAPI


# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoclass
class FlightPlanDB:

    """This class mostly contains internal functions called by the API.
    However, the internal functions are hidden, so unless you look at
    the source code, you're unlikely to see them.

    Submodules are accessed via the alias properties at the end; for instance,
    ``flightplandb.plan.fetch()``

    Parameters
    ----------
    key : Optional[str]
        API token, defaults to None (which makes it unauthenticated)
    url_base : str
        The host of the API endpoint URL,
        defaults to https://api.flightplandatabase.com
    """

    def __init__(
        self, key: Optional[str] = None,
        url_base: str = "https://api.flightplandatabase.com"
    ):
        self.key: str = key
        self._header: CaseInsensitiveDict[str] = CaseInsensitiveDict()
        self.url_base = url_base

    def _request(self, method: str,
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

        # the API only takes "true" or "false", not True or False
        for k, v in params.items():
            if v in (True, False):
                params[k] = json.dumps(v)

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

        status_handler(resp.status_code, ignore_statuses)

        self._header = resp.headers

        if return_format == "dict":
            return resp.json()

        return resp.text  # if the format is not a dict

    # and here go the specific non-paginated HTTP calls
    def _get(self, path: str, return_format="dict",
             ignore_statuses: Optional[List] = None,
             params: Optional[Dict] = None,
             *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`_request()` for get requests.

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

        resp = self._request("get", path,
                             return_format,
                             ignore_statuses,
                             params,
                             *args, **kwargs)
        return resp

    def _post(self, path: str, return_format="dict",
              ignore_statuses: Optional[List] = None,
              params: Optional[Dict] = None,
              *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`_request()` for post requests.

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

        resp = self._request("post",
                             path,
                             return_format,
                             ignore_statuses,
                             params,
                             *args, **kwargs)
        return resp

    def _patch(self, path: str, return_format="dict",
               ignore_statuses: Optional[List] = None,
               params: Optional[Dict] = None,
               *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`_request()` for patch requests.

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

        resp = self._request("patch",
                             path,
                             return_format,
                             ignore_statuses,
                             params,
                             *args, **kwargs)
        return resp

    def _delete(self, path: str, return_format="dict",
                ignore_statuses: Optional[List] = None,
                params: Optional[Dict] = None,
                *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`_request()` for delete requests.

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

        resp = self._request("delete",
                             path,
                             return_format,
                             ignore_statuses,
                             params,
                             *args, **kwargs)
        return resp

    def _getiter(self, path: str,
                 limit: int = 100,
                 sort: str = "created",
                 ignore_statuses: Optional[List] = None,
                 params: Optional[Dict] = None,
                 *args, **kwargs) -> Generator[Dict, None, None]:
        """Get :meth:`_request()` for paginated results.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        limit : int, optional
            Maximum number of results to return, defaults to 100
        sort : str, optional
            Sort order to return results in. Valid sort orders are
            created, updated, popularity, and distance
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

        # the API only takes "true" or "false", not True or False
        for k, v in params.items():
            if v in (True, False):
                params[k] = json.dumps(v)

        valid_sort_orders = ["created", "updated", "popularity", "distance"]
        if sort not in valid_sort_orders:
            raise ValueError(
                f"sort argument must be one of {', '.join(valid_sort_orders)}")
        else:
            params["sort"] = sort

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
    def version(self) -> int:
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

        resp = self._get("")
        return StatusResponse(**resp)

    def revoke(self) -> StatusResponse:
        """Revoke the API key in use in the event it is compromised.

        Requires authentication.

        Returns
        -------
        StatusResponse
            If the HTTP response code is 200 and the status message is "OK",
            then the key has been revoked and any further requests will be
            rejected.
            Any other status code or message indicates an error has
            occurred and the errors array will give further details.
        """

        resp = self._get("/auth/revoke")
        self._header = resp.headers
        return StatusResponse(**resp.json())

    # Sub APIs
    @property
    def nav(self):
        """Alias for :class:`~flightplandb.submodules.nav.NavAPI()`"""
        return NavAPI(self)

    @property
    def plan(self):
        """Alias for :class:`~flightplandb.submodules.plan.PlanAPI()`"""
        return PlanAPI(self)

    @property
    def tags(self):
        """Alias for :class:`~flightplandb.submodules.tags.TagsAPI()`"""
        return TagsAPI(self)

    @property
    def user(self):
        """Alias for :class:`~flightplandb.submodules.user.UserAPI()`"""
        return UserAPI(self)

    @property
    def weather(self):
        """Alias for :class:`~flightplandb.submodules.weather.WeatherAPI()`"""
        return WeatherAPI(self)
