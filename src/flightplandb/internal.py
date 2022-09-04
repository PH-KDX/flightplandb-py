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

"""This file mostly contains internal functions called by the API,
so you're unlikely to ever use them."""

from typing import AsyncIterable, List, Dict, Union, Optional

from base64 import b64encode
from urllib.parse import urljoin
import json
import aiohttp

from multidict import CIMultiDict

from flightplandb.exceptions import status_handler


# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoclass
# https://github.com/python/cpython/blob/main/Lib/random.py#L792

url_base: str = "https://api.flightplandatabase.com"


def _auth_str(key):
    """Returns a API auth string."""

    if isinstance(key, str):
        key = key.encode("latin1")
    else:
        raise ValueError("API key must be a string!")

    authstr = "Basic " + (
        b64encode(key + b":").strip().decode()
    )

    return authstr


async def request(
    method: str,
    path: str,
    return_format="native",
    ignore_statuses: Optional[List] = None,
    params: Optional[Dict] = None,
    json_data: Optional[Dict] = None,
    key: Optional[str] = None
) -> Union[Dict, bytes]:
    """General HTTP requests function for non-paginated results.

    Parameters
    ----------
    method : str
        An HTTP request type. One of GET, POST, PATCH, or DELETE
    path : str
        The endpoint's path to which the request is being made
    return_format : `str`, optional
        The API response format, defaults to ``"native"``
    ignore_statuses : `List`, optional
        Statuses (together with 200 OK) which don't
        raise an HTTPError, defaults to None
    params : `Dict`, optional
        Any other HTTP request parameters, defaults to None
    json_data : `Dict`, optional
        Custom JSON data to be formatted into the request body
    key : str
        API token, defaults to None (which makes it unauthenticated)

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
    for _key, _value in params.items():
        if _value in (True, False):
            params[_key] = json.dumps(_value)

    # convert the API content return_format to an HTTP Accept type
    try:
        return_format_encoded = format_return_types[return_format]
    # unless it's not a valid return_format
    except KeyError as exc:
        raise ValueError(
            f"'{return_format}' is not a valid data return type option"
            ) from exc

    # then add it to the request headers
    params["Accept"] = return_format_encoded

    # set auth in headers if key is provided
    if key is not None:
        params["Authorization"] = _auth_str(key=key)

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=method,
            url=urljoin(url_base, path),
            headers=params,
            json=json_data
        ) as resp:

            status_handler(resp.status, ignore_statuses)

            header = resp.headers

            if return_format == "native":
                return header, await resp.json()
            else:
                return header, await resp.text()  # if the format is not a dict


# and here go the specific non-paginated HTTP calls
async def get_headers(
    key: Optional[str] = None
) -> CIMultiDict:
    """Calls :meth:`request()` for request headers.

    Parameters
    ----------
    key : `str`, optional
        API token, defaults to None (which makes it unauthenticated)

    Returns
    -------
    CaseInsensitiveDict
        A dict of headers, but the keys are case-insensitive.
    """
    headers, _ = await request(
        method="get",
        path="",
        key=key
    )
    return headers


async def get(
    path: str,
    return_format="native",
    ignore_statuses: Optional[List] = None,
    params: Optional[Dict] = None,
    key: Optional[str] = None
) -> Union[Dict, bytes]:
    """Calls :meth:`request()` for get requests.

    Parameters
    ----------
    path : str
        The endpoint's path to which the request is being made
    return_format : `str`, optional
        The API response format, defaults to ``"native"``
    ignore_statuses : `List`, optional
        Statuses (together with 200 OK) which don't
        raise an HTTPError, defaults to None
    params : `Dict`, optional
        Any other HTTP request parameters, defaults to None
    key : `str`, optional
        API token, defaults to None (which makes it unauthenticated)

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

    _, resp = await request(
        method="get",
        path=path,
        return_format=return_format,
        ignore_statuses=ignore_statuses,
        params=params,
        key=key
    )
    return resp


async def post(
    path: str,
    return_format="native",
    ignore_statuses: Optional[List] = None,
    params: Optional[Dict] = None,
    json_data: Optional[Dict] = None,
    key: Optional[str] = None
) -> Union[Dict, bytes]:
    """Calls :meth:`request()` for post requests.

    Parameters
    ----------
    path : str
        The endpoint's path to which the request is being made
    return_format : `str`, optional
        The API response format, defaults to ``"native"``
    ignore_statuses : `List`, optional
        Statuses (together with 200 OK) which don't
        raise an HTTPError, defaults to None
    params : `Dict`, optional
        Any other HTTP request parameters, defaults to None
    json_data : `Dict`, optional
        Custom JSON data to be formatted into the request body
    key : `str`, optional
        API token, defaults to None (which makes it unauthenticated)

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

    _, resp = await request(
        method="post",
        path=path,
        return_format=return_format,
        ignore_statuses=ignore_statuses,
        params=params,
        json_data=json_data,
        key=key
    )
    return resp


async def patch(
    path: str,
    return_format="native",
    ignore_statuses: Optional[List] = None,
    params: Optional[Dict] = None,
    json_data: Optional[Dict] = None,
    key: Optional[str] = None
) -> Union[Dict, bytes]:
    """Calls :meth:`request()` for patch requests.

    Parameters
    ----------
    path : str
        The endpoint's path to which the request is being made
    return_format : `str`, optional
        The API response format, defaults to ``"native"``
    ignore_statuses : `List`, optional
        Statuses (together with 200 OK) which don't
        raise an HTTPError, defaults to None
    params : `Dict`, optional
        Any other HTTP request parameters, defaults to None
    json_data : `Dict`, optional
        Custom JSON data to be formatted into the request body
    key : `str`, optional
        API token, defaults to None (which makes it unauthenticated)

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

    _, resp = await request(
        method="patch",
        path=path,
        return_format=return_format,
        ignore_statuses=ignore_statuses,
        params=params,
        key=key,
        json_data=json_data
    )
    return resp


async def delete(
    path: str,
    return_format="native",
    ignore_statuses: Optional[List] = None,
    params: Optional[Dict] = None,
    key: Optional[str] = None
) -> Union[Dict, bytes]:
    """Calls :meth:`request()` for delete requests.

    Parameters
    ----------
    path : str
        The endpoint's path to which the request is being made
    return_format : `str`, optional
        The API response format, defaults to ``"native"``
    ignore_statuses : `List`, optional
        Statuses (together with 200 OK) which don't
        raise an HTTPError, defaults to None
    params : `Dict`, optional
        Any other HTTP request parameters, defaults to None
    key : `str`, optional
        API token, defaults to None (which makes it unauthenticated)

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

    _, resp = await request(
        method="delete",
        path=path,
        return_format=return_format,
        ignore_statuses=ignore_statuses,
        params=params,
        key=key
    )
    return resp


async def getiter(
    path: str,
    limit: int = 100,
    sort: str = "created",
    ignore_statuses: Optional[List] = None,
    params: Optional[Dict] = None,
    key: Optional[str] = None
) -> AsyncIterable[Dict]:
    """Get :meth:`request()` for paginated results.

    Parameters
    ----------
    path : str
        The endpoint's path to which the request is being made
    limit : int, optional
        Maximum number of results to return, defaults to 100
    sort : `str`, optional
        Sort order to return results in. Valid sort orders are
        created, updated, popularity, and distance
    ignore_statuses : `List`, optional
        Statuses (together with 200 OK) which don't
        raise an HTTPError, defaults to None
    params : `Dict`, optional
        Any other HTTP request parameters, defaults to None
    key : `str`, optional
        API token, defaults to None (which makes it unauthenticated)

    Returns
    -------
    AsyncIterable[Dict]
        An iterable of dicts. Return format cannot be specified.
    """

    if not ignore_statuses:
        ignore_statuses = []
    if not params:
        params = {}

    # the API only takes "true" or "false", not True or False
    for key, value in params.items():
        if value in (True, False):
            params[key] = json.dumps(value)

    valid_sort_orders = ["created", "updated", "popularity", "distance"]
    if sort not in valid_sort_orders:
        raise ValueError(
            f"sort argument must be one of {', '.join(valid_sort_orders)}")
    else:
        params["sort"] = sort

    url = urljoin(url_base, path)

    # set auth in headers if key is provided
    if key is not None:
        params["Authorization"] = _auth_str(key=key)

    # initially no results have been fetched yet
    num_results = 0

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
            params=params,
        ) as r_fpdb:
            status_handler(r_fpdb.status, ignore_statuses)

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
            async with session.get(
                url=url,
                params=params
            ) as r_fpdb:
                status_handler(r_fpdb.status, ignore_statuses)
                # ...keep cycling through pages...
                for i in await r_fpdb.json():
                    # ...and return every dictionary in there...
                    yield i
                    num_results += 1
                    # ...unless the result limit has been reached
                    if num_results == limit:
                        return
