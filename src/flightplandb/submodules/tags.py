from typing import List
from flightplandb.datatypes import Tag


class TagsAPI:

    """
    Related to flight plans.
    Accessed via :meth:`~flightplandb.flightplandb.FlightPlanDB.tags`.
    """

    def __init__(self, flightplandb):
        self._fp = flightplandb

    def fetch(self) -> List[Tag]:
        """Fetches current popular tags from all flight plans.
        Only tags with sufficient popularity are included.

        Returns
        ----------
        List[Tag]
            A list of the current popular tags.
        """

        return list(map(lambda t: Tag(**t), self._fp._get("/tags")))
