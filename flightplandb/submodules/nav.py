from typing import Generator, List, Union
from flightplandb.datatypes import Airport, Track, SearchNavaid


class NavAPI:

    """
    Commands related to navigation aids and airports.
    Accessed via :meth:`~flightplandb.flightplandb.FlightPlanDB.nav`.
    """

    def __init__(self, flightplandb):
        self._fp = flightplandb

    def airport(self, icao) -> Union[Airport, None]:
        """Fetches information about an airport.

        Parameters
        ----------
        icao : type
            The airport ICAO to fetch information for

        Returns
        -------
        Union[Airport, None]

            :class:`~flightplandb.datatypes.Airport` if the airport was found.
            ``None`` if it was not.

        """

        resp = self._fp._get(f"/nav/airport/{icao}", ignore_statuses=[404])
        if "message" in resp and resp["message"] == "Not Found":
            response = None
        else:
            response = Airport(**resp)
        return response

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
            if type_ in SearchNavaid.validtypes:
                params["types"] = type_
            else:
                raise ValueError(f"{type_} is not a valid Navaid type")
        for i in self._fp._getiter("/search/nav", params=params):
            yield SearchNavaid(**i)
