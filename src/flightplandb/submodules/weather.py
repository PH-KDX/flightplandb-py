from flightplandb.datatypes import Weather
from typing import Optional
from flightplandb.flightplandb import FlightPlanDB


class WeatherAPI(FlightPlanDB):

    """Weather. I mean, how much is there to say?

    Accessed via :meth:`~flightplandb.flightplandb.FlightPlanDB.weather`.
    """

    def fetch(self, icao: str, key: Optional[str] = None) -> Weather:
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

        return Weather(**self._get(path=f"/weather/{icao}", key=key))
