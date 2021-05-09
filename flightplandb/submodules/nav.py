from typing import Generator, List, Union
from flightplandb.datatypes import Airport, Track, SearchNavaid


class NavAPI:

    """
    Commands related to navigation aids and airports.
    Accessed via :meth:`~flightplandb.flightplandb.FlightPlanDB.nav`.
    """

    def __init__(self, flightplandb):
        self._fp = flightplandb

    def airport(self, icao: str) -> Union[Airport]:
        """Fetches information about an airport.

        Parameters
        ----------
        icao : str
            The airport ICAO to fetch information for

        Returns
        -------
        Union[Airport, None]
            :class:`~flightplandb.datatypes.Airport` if the airport was found.

        Raises
        ------
        :class:`~flightplandb.exceptions.BadRequestException`
            No airport with the specified ICAO code was found.
        """

        resp = self._fp._get(f"/nav/airport/{icao}")
        return Airport(**resp)

    def nats(self) -> List[Track]:
        """Fetches current North Atlantic Tracks.

        Returns
        -------
        List[Track]
            List of NATs
        """

        return list(
            map(lambda n: Track(**n), self._fp._get("/nav/NATS")))

    def pacots(self) -> List[Track]:
        """Fetches current Pacific Organized Track System tracks.

        Returns
        -------
        List[Track]
            List of PACOTs
        """

        return list(
            map(lambda t: Track(**t), self._fp._get("/nav/PACOTS")))

    def search(self, query: str,
               type_: str = None) -> Generator[SearchNavaid, None, None]:
        r"""Searches navaids using a query.

        Parameters
        ----------
        query : str
            The search query. Searches the navaid identifier and navaid name
        type\_ : str
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
            if type_ in SearchNavaid.validtypes:
                params["types"] = type_
            else:
                raise ValueError(f"{type_} is not a valid Navaid type")
        for i in self._fp._getiter("/search/nav", params=params):
            yield SearchNavaid(**i)
