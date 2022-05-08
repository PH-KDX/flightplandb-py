"""Commands related to navigation aids and airports."""
from typing import Generator, List, Optional
from flightplandb.datatypes import Airport, Track, SearchNavaid
from flightplandb import internal


def airport(icao: str, key: Optional[str] = None) -> Airport:
    """Fetches information about an airport.

    Parameters
    ----------
    icao : str
        The airport ICAO to fetch information for
    key : `str`, optional
        API authentication key.

    Returns
    -------
    Union[Airport, None]
        :class:`~flightplandb.datatypes.Airport` if the airport was found.

    Raises
    ------
    :class:`~flightplandb.exceptions.BadRequestException`
        No airport with the specified ICAO code was found.
    """

    resp = internal.get(path=f"/nav/airport/{icao}", key=key)
    return Airport(**resp)


def nats(key: Optional[str] = None) -> List[Track]:
    """Fetches current North Atlantic Tracks.

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    -------
    List[Track]
        List of NATs
    """

    return list(
        map(lambda n: Track(**n), internal.get(path="/nav/NATS", key=key)))


def pacots(key: Optional[str] = None) -> List[Track]:
    """Fetches current Pacific Organized Track System tracks.

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    -------
    List[Track]
        List of PACOTs
    """

    return list(
        map(lambda t: Track(**t), internal.get(path="/nav/PACOTS", key=key)))


def search(
        query: str,
        type_: Optional[str] = None, key: Optional[str] = None
        ) -> Generator[SearchNavaid, None, None]:
    r"""Searches navaids using a query.

    Parameters
    ----------
    query : str
        The search query. Searches the navaid identifier and navaid name
    type\_ : `str`, optional
        Navaid type.
        Must be either ``None`` (default value, returns all types) or one
        of :py:obj:`~flightplandb.datatypes.SearchNavaid.validtypes`
    key : `str`, optional
        API authentication key.

    Yields
    -------
    Generator[SearchNavaid, None, None]
        A generator of navaids with either a name or ident
        matching the ``query``
    """

    params = {"q": query}
    if type_:
        if type_ in SearchNavaid.validtypes:
            params["types"] = type_
        else:
            raise ValueError(f"{type_} is not a valid Navaid type")
    for i in internal.getiter(path="/search/nav", params=params, key=key):
        yield SearchNavaid(**i)
