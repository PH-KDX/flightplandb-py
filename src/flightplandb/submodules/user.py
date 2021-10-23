from typing import Generator, Optional
from flightplandb.datatypes import Plan, User, UserSmall
from flightplandb.flightplandb import FlightPlanDB


class UserAPI(FlightPlanDB):

    """Commands related to registered users.
    Accessed via :meth:`~flightplandb.flightplandb.FlightPlanDB.user`.
    """

    def me(self, key: Optional[str] = None) -> User:
        """Fetches profile information for the currently authenticated user.

        Requires authentication.

        Returns
        -------
        User
            The User object of the currently authenticated user

        Raises
        ------
        :class:`~flightplandb.exceptions.UnauthorizedException`
            Authentication failed.
        """

        return User(**self._get(path="/me", key=key))

    def fetch(self, username: str, key: Optional[str] = None) -> User:
        """Fetches profile information for any registered user

        Parameters
        ----------
        username : str
            Username of the registered User

        Returns
        -------
        User
            The User object of the user associated with the username

        Raises
        -------
        :class:`~flightplandb.exceptions.NotFoundException`
            No user was found with this username.
        """

        return User(**self._get(path=f"/user/{username}", key=key))

    def plans(self, username: str, sort: str = "created",
              limit: int = 100,
              key: Optional[str] = None) -> Generator[Plan, None, None]:
        """Fetches flight plans created by a user.

        Parameters
        ----------
        username : str
            Username of the user who created the flight plans
        sort : str, optional
            Sort order to return results in. Valid sort orders are
            created, updated, popularity, and distance
        limit: int
            Maximum number of plans to fetch, defaults to ``100``

        Yields
        -------
        Generator[Plan, None, None]
            A generator with all the flight plans a user created,
            limited by ``limit``
        """
        for i in self._getiter(path=f"/user/{username}/plans",
                               sort=sort,
                               limit=limit,
                               key=key):
            yield Plan(**i)

    def likes(self, username: str, sort: str = "created",
              limit: int = 100,
              key: Optional[str] = None) -> Generator[Plan, None, None]:
        """Fetches flight plans liked by a user.

        Parameters
        ----------
        username : str
            Username of the user who liked the flight plans
        sort : str, optional
            Sort order to return results in. Valid sort orders are
            created, updated, popularity, and distance
        limit : int
            Maximum number of plans to fetch, defaults to ``100``

        Yields
        -------
        Generator[Plan, None, None]
            A generator with all the flight plans a user liked,
            limited by ``limit``
        """

        for i in self._getiter(path=f"/user/{username}/likes",
                               sort=sort,
                               limit=limit,
                               key=key):
            yield Plan(**i)

    def search(self, username: str,
               limit=100,
               key: Optional[str] = None) -> Generator[UserSmall, None, None]:
        """Searches for users by username. For more detailed info on a
        specific user, use :meth:`fetch`

        Parameters
        ----------
        username : str
            Username to search user database for
        limit : type
            Maximum number of users to fetch, defaults to ``100``

        Yields
        -------
        Generator[UserSmall, None, None]
            A generator with a list of users approximately matching
            ``username``, limited by ``limit``. UserSmall is used instead of
            User, because less info is returned.
        """

        for i in self._getiter(path="/search/users",
                               limit=limit,
                               params={"q": username},
                               key=key):
            yield UserSmall(**i)
