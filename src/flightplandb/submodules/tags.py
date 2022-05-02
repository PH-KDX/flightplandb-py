from typing import List, Optional
from flightplandb.datatypes import Tag
from flightplandb.internal import FlightPlanDB


class TagsAPI(FlightPlanDB):

    """
    Related to flight plans.
    Accessed via :meth:`~flightplandb.flightplandb.FlightPlanDB.tags`.
    """

    def fetch(self, key: Optional[str] = None) -> List[Tag]:
        """Fetches current popular tags from all flight plans.
        Only tags with sufficient popularity are included.

        Returns
        ----------
        List[Tag]
            A list of the current popular tags.
        """

        return list(map(lambda t: Tag(**t), self._get(path="/tags", key=key)))
