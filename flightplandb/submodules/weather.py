from flightplandb.datatypes import Weather


class WeatherAPI:

    """Weather. I mean, how much is there to say?

    Accessed via :meth:`~flightplandb.flightplandb.FlightPlanDB.weather`.
    """

    def __init__(self, flightplandb):
        self._fp = flightplandb

    def fetch(self, icao: str) -> Weather:
        """
        Fetches current weather conditions at an airport

        Parameters
        ----------
        icao : str
            ICAO code of the airport for which the weather will be fetched

        Returns
        -------
        Weather
            METAR and TAF for an airport

        Raises
        ------
        :class:`~flightplandb.exceptions.NotFoundException`
            No airport with the specified ICAO code was found.
        """

        return Weather(**self._fp._get(f"/weather/{icao}"))
