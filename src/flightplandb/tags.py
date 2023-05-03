"""Contains the command for fetching flight plan tags."""
from typing import List, Optional

from flightplandb import internal
from flightplandb.datatypes import Tag


async def fetch(key: Optional[str] = None) -> List[Tag]:
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

    return list(map(lambda t: Tag(**t), await internal.get(path="/tags", key=key)))
