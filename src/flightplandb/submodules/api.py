from typing import Optional
from flightplandb import internal
from flightplandb.datatypes import StatusResponse


def _header_value(header_key: str, key: Optional[str] = None) -> str:
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

    headers = internal._get_headers(key=key)  # Make one request to fetch headers
    return headers[header_key]


def version(key: Optional[str] = None) -> int:
    """API version that returned the response

    Returns
    -------
    int
        API version
    """

    return int(_header_value("X-API-Version", key=key))


def units(key: Optional[str] = None) -> str:
    """The units system used for numeric values.
    https://flightplandatabase.com/dev/api#units

    Returns
    -------
    str
        AVIATION, METRIC or SI
    """

    return _header_value("X-Units", key=key)


def limit_cap(key: Optional[str] = None) -> int:
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

    return int(_header_value("X-Limit-Cap", key=key))


def limit_used(key: Optional[str] = None) -> int:
    """The number of requests used in the current period
    by the presented API key or IP address

    Returns
    -------
    int
        number of requests used in period
    """

    return int(_header_value("X-Limit-Used", key=key))


def ping(key: Optional[str] = None) -> StatusResponse:
    """Checks API status to see if it is up

    Returns
    -------
    StatusResponse
        OK 200 means the service is up and running.
    """

    resp = internal._get(path="", key=key)
    return StatusResponse(**resp)


def revoke(key: Optional[str] = None) -> StatusResponse:
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

    resp = internal._get(path="/auth/revoke", key=key)
    return StatusResponse(**resp)
