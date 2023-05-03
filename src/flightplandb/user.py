"""Commands related to registered users."""
from typing import AsyncIterable, Optional

from flightplandb import internal
from flightplandb.datatypes import Plan, User, UserSmall


async def me(key: Optional[str] = None) -> User:
    """Fetches profile information for the currently authenticated user.

    Requires authentication.

    Parameters
    ----------
    key : `str`, optional
        API authentication key.

    Returns
    -------
    User
        The User object of the currently authenticated user

    Raises
    ------
    :class:`~flightplandb.exceptions.UnauthorizedException`
        Authentication failed.
    """

    resp = await internal.get(path="/me", key=key)
    return User(**resp)


async def fetch(username: str, key: Optional[str] = None) -> User:
    """Fetches profile information for any registered user

    Parameters
    ----------
    username : str
        Username of the registered User
    key : `str`, optional
        API authentication key.

    Returns
    -------
    User
        The User object of the user associated with the username

    Raises
    -------
    :class:`~flightplandb.exceptions.NotFoundException`
        No user was found with this username.
    """

    resp = await internal.get(path=f"/user/{username}", key=key)
    return User(**resp)


async def plans(
    username: str, sort: str = "created", limit: int = 100, key: Optional[str] = None
) -> AsyncIterable[Plan]:
    """Fetches flight plans created by a user.

    Parameters
    ----------
    username : str
        Username of the user who created the flight plans
    sort : str
        Sort order to return results in. Valid sort orders are
        created, updated, popularity, and distance
    limit: int
        Maximum number of plans to fetch, defaults to ``100``
    key : `str`, optional
        API authentication key.

    Yields
    -------
    AsyncIterable[Plan]
        An iterator with all the flight plans a user created,
        limited by ``limit``
    """
    async for i in internal.getiter(
        path=f"/user/{username}/plans", sort=sort, limit=limit, key=key
    ):
        yield Plan(**i)


async def likes(
    username: str, sort: str = "created", limit: int = 100, key: Optional[str] = None
) -> AsyncIterable[Plan]:
    """Fetches flight plans liked by a user.

    Parameters
    ----------
    username : str
        Username of the user who liked the flight plans
    sort : str
        Sort order to return results in. Valid sort orders are
        created, updated, popularity, and distance
    limit : int
        Maximum number of plans to fetch, defaults to ``100``
    key : `str`, optional
        API authentication key.

    Yields
    -------
    AsyncIterable[Plan]
        An iterable with all the flight plans a user liked,
        limited by ``limit``
    """

    async for i in internal.getiter(
        path=f"/user/{username}/likes", sort=sort, limit=limit, key=key
    ):
        yield Plan(**i)


async def search(
    username: str, limit=100, key: Optional[str] = None
) -> AsyncIterable[UserSmall]:
    """Searches for users by username. For more detailed info on a
    specific user, use :meth:`fetch`

    Parameters
    ----------
    username : str
        Username to search user database for
    limit : type
        Maximum number of users to fetch, defaults to ``100``
    key : `str`, optional
        API authentication key.

    Yields
    -------
    AsyncIterable[UserSmall]
        An iterable with a list of users approximately matching
        ``username``, limited by ``limit``. UserSmall is used instead of
        User, because less info is returned.
    """

    async for i in internal.getiter(
        path="/search/users", limit=limit, params={"q": username}, key=key
    ):
        yield UserSmall(**i)
