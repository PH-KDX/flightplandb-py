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



# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoclass
# https://github.com/python/cpython/blob/main/Lib/random.py#L792
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

    def __init__(self):
        self._header: CaseInsensitiveDict[str] = CaseInsensitiveDict()
        self.url_base: str = "https://api.flightplandatabase.com"

    def _request(self, method: str,
                 path: str, return_format="native",
                 ignore_statuses: Optional[List] = None,
                 params: Optional[Dict] = None,
                 key: Optional[str] = None,
                 *args, **kwargs) -> Union[Dict, bytes]:
        """General HTTP requests function for non-paginated results.

        Parameters
        ----------
        method : str
            An HTTP request type. One of GET, POST, PATCH, or DELETE
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"native"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        key : Optional[str]
            API token, defaults to None (which makes it unauthenticated)
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dataclass`` if ``return_format`` is ``"native"``,
            otherwise ``bytes``

        Raises
        ------
        ValueError
            Invalid return_format option
        HTTPError
            Invalid HTTP status in response
        """

        format_return_types = {
            # if a dict is requested, the JSON will later be converted to that
            "native": "application/vnd.fpd.v1+json",
            # otherwise, pure JSON will be returned
            "json": "application/vnd.fpd.v1+json",
            "xml": "application/vnd.fpd.v1+xml",
            "csv": "text/vnd.fpd.export.v1.csv+csv",
            "pdf": "application/vnd.fpd.export.v1.pdf",
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
                                auth=HTTPBasicAuth(key, None),
                                headers=params, *args, **kwargs)

        status_handler(resp.status_code, ignore_statuses)

        self._header = resp.headers

        if return_format == "native":
            return resp.json()

        return resp.text  # if the format is not a dict

    # and here go the specific non-paginated HTTP calls
    def _get(self, path: str, return_format="native",
             ignore_statuses: Optional[List] = None,
             params: Optional[Dict] = None,
             key: Optional[str] = None,
             *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`_request()` for get requests.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"native"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        key : Optional[str]
            API token, defaults to None (which makes it unauthenticated)
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dataclass`` if ``return_format`` is ``"native"``,
            otherwise ``bytes``
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
                             key,
                             *args, **kwargs)
        return resp

    def _post(self, path: str, return_format="native",
              ignore_statuses: Optional[List] = None,
              params: Optional[Dict] = None,
              key: Optional[str] = None,
              *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`_request()` for post requests.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"native"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        key : Optional[str]
            API token, defaults to None (which makes it unauthenticated)
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dataclass`` if ``return_format`` is ``"native"``,
            otherwise ``bytes``
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
                             key,
                             *args, **kwargs)
        return resp

    def _patch(self, path: str, return_format="native",
               ignore_statuses: Optional[List] = None,
               params: Optional[Dict] = None,
               key: Optional[str] = None,
               *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`_request()` for patch requests.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"native"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        key : Optional[str]
            API token, defaults to None (which makes it unauthenticated)
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dataclass`` if ``return_format`` is ``"native"``,
            otherwise ``bytes``
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
                             key,
                             *args, **kwargs)
        return resp

    def _delete(self, path: str, return_format="native",
                ignore_statuses: Optional[List] = None,
                params: Optional[Dict] = None,
                key: Optional[str] = None,
                *args, **kwargs) -> Union[Dict, bytes]:
        """Calls :meth:`_request()` for delete requests.

        Parameters
        ----------
        path : str
            The endpoint's path to which the request is being made
        return_format : str, optional
            The API response format, defaults to ``"native"``
        ignore_statuses : Optional[List], optional
            Statuses (together with 200 OK) which don't
            raise an HTTPError, defaults to None
        params : Optional[Dict], optional
            Any other HTTP request parameters, defaults to None
        key : Optional[str]
            API token, defaults to None (which makes it unauthenticated)
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Union[Dict, bytes]
            A ``dataclass`` if ``return_format`` is ``"native"``,
            otherwise ``bytes``
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
                             key,
                             *args, **kwargs)
        return resp

    def _getiter(self, path: str,
                 limit: int = 100,
                 sort: str = "created",
                 ignore_statuses: Optional[List] = None,
                 params: Optional[Dict] = None,
                 key: Optional[str] = None,
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
        key : Optional[str]
            API token, defaults to None (which makes it unauthenticated)
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
        auth = HTTPBasicAuth(key, None)

        session = requests.Session()
        # initially no results have been fetched yet
        num_results = 0

        r_fpdb = session.get(url, params=params, auth=auth, *args, **kwargs)
        status_handler(r_fpdb.status_code, ignore_statuses)

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
            status_handler(r_fpdb.status_code, ignore_statuses)
            # ...keep cycling through pages...
            for i in r_fpdb.json():
                # ...and return every dictionary in there...
                yield i
                num_results += 1
                # ...unless the result limit has been reached
                if num_results == limit:
                    return

