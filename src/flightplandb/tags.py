"""Contains the command for fetching flight plan tags."""
from typing import List, Optional
from flightplandb.datatypes import Tag
from flightplandb import internal


def fetch(key: Optional[str] = None) -> List[Tag]:
    """Fetches current popular tags from all flight plans.
    Only tags with sufficient popularity are included.

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    ----------
    List[Tag]
        A list of the current popular tags.
    """

    return list(map(lambda t: Tag(**t), internal.get(path="/tags", key=key)))
