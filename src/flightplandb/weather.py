"""Weather. I mean, how much is there to say?"""
from typing import Optional

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

    return Weather(**(await internal.get(path=f"/weather/{icao}", key=key)))
