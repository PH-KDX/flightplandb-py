"""Contains the command for fetching flight plan tags."""
from typing import List, Optional
from flightplandb.datatypes import Tag
from flightplandb.internal import _get


def fetch(key: Optional[str] = None) -> List[Tag]:
    """Fetches current popular tags from all flight plans.
    Only tags with sufficient popularity are included.

    Returns
    ----------
    List[Tag]
        A list of the current popular tags.
    """

    return list(map(lambda t: Tag(**t), _get(path="/tags", key=key)))
