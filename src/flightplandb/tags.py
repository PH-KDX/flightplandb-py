"""Contains the command for fetching flight plan tags."""
from typing import Dict, List, Optional

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

    tags_list = []
    for tag in await internal.get(path="/tags", key=key):
        if isinstance(tag, Dict):
            tags_list.append(Tag(**tag))
        else:
            raise ValueError(
                f"could not convert {tag} to a Tag datatype; it is not a valid mapping"
            )
    return tags_list
