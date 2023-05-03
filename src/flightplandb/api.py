"""These functions return information about the API."""
from typing import Optional

from flightplandb import internal
from flightplandb.datatypes import StatusResponse


async def header_value(header_key: str, key: Optional[str] = None) -> str:
    """Gets header value for key. Do not call directly.

    Parameters
    ----------
    header_key : str
        One of the HTTP header keys
    key : `str`, optional
        API authentication key.

    Returns
    -------
    str
        The value corresponding to the passed key
    """

    # Make 1 request to fetch headers
    headers = await internal.get_headers(key=key)
    return headers[header_key]


async def version(key: Optional[str] = None) -> int:
    """API version that returned the response.

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    -------
    int
        API version
    """

    return int(await header_value(header_key="X-API-Version", key=key))


async def units(key: Optional[str] = None) -> str:
    """The units system used for numeric values.
    https://flightplandatabase.com/dev/api#units

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    -------
    str
        AVIATION, METRIC or SI
    """

    return await header_value(header_key="X-Units", key=key)


async def limit_cap(key: Optional[str] = None) -> int:
    """The number of requests allowed per day, operated on an hourly rolling
    basis. i.e requests used between 19:00 and 20:00 will become available
    again at 19:00 the following day. API key authenticated requests get a
    higher daily rate limit and can be raised if a compelling
    use case is presented. See :ref:`request-limits` for more details.

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    -------
    int
        number of allowed requests per day
    """

    return int(await header_value(header_key="X-Limit-Cap", key=key))


async def limit_used(key: Optional[str] = None) -> int:
    """The number of requests used in the current period
    by the presented API key or IP address.
    See :ref:`request-limits` for more details.

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    -------
    int
        number of requests used in period
    """

    return int(await header_value(header_key="X-Limit-Used", key=key))


async def ping(key: Optional[str] = None) -> StatusResponse:
    """Checks API status to see if it is up

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    -------
    StatusResponse
        OK 200 means the service is up and running.
    """

    resp = await internal.get(path="", key=key)
    return StatusResponse(**resp)


async def revoke(key: str) -> StatusResponse:
    """Revoke the API key in use in the event it is compromised.
    See :ref:`authentication` for more details.

    Requires authentication.

    Parameters
    ----------
    key : str
        API authentication key.

    Returns
    -------
    StatusResponse
        If the HTTP response code is 200 and the status message is "OK",
        then the key has been revoked and any further requests will be
        rejected.
        Any other status code or message indicates an error has
        occurred and the errors array will give further details.
    """

    resp = await internal.get(path="/auth/revoke", key=key)
    return StatusResponse(**resp)
