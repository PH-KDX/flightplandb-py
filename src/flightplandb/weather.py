"""Weather. I mean, how much is there to say?"""
from typing import Dict, Optional

from flightplandb import internal
from flightplandb.datatypes import Weather


async def fetch(icao: str, key: Optional[str] = None) -> Weather:
    """
    Fetches current weather conditions at an airport

    Parameters
    ----------
    icao : str
        ICAO code of the airport for which the weather will be fetched
    key : `str`, optional
        API authentication key.

    Returns
    -------
    Weather
        METAR and TAF for an airport

    Raises
    ------
    :class:`~flightplandb.exceptions.NotFoundException`
        No airport with the specified ICAO code was found.
    """

    weather_response = await internal.get(path=f"/weather/{icao}", key=key)
    if isinstance(weather_response, Dict):
        return Weather(**weather_response)
    else:
        raise ValueError(
            "Could not convert response to a Weather datatype; "
            "it is not a valid mapping"
        )
