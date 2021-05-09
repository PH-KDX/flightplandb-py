from typing import Generator, Union
from flightplandb.datatypes import (
    StatusResponse, PlanQuery,
    Plan, GenerateQuery
)


class PlanAPI():

    """
    Flightplan-related commands.
    Accessed via :meth:`~flightplandb.flightplandb.FlightPlanDB.plan`.
    """

    def __init__(self, flightplandb):
        self._fp = flightplandb

    def fetch(self, id_: int,
              return_format: str = "dict") -> Union[Plan, None, bytes]:
        # Underscore for id_ must be escaped as id\_ so sphinx shows the _.
        # However, this would raise W605. To fix this, a raw string is used.
        r"""
        Fetches a flight plan and its associated attributes by ID.
        Returns it in specified format.

        Parameters
        ----------
        id\_ : int
            The ID of the flight plan to fetch
        return_format : str
            The API response format, defaults to ``"dict"``

        Returns
        -------
        Union[Plan, None, bytes]
            :class:`~flightplandb.datatypes.Plan` by default or if ``"dict"``
            is specified as the ``return_format``.

            ``bytes`` if a different format than ``"dict"`` was specified.

        Raises
        ------
        :class:`~flightplandb.exceptions.NotFoundException`
            No plan with the specified id was found.
        """

        request = self._fp._get(
            f"/plan/{id_}",
            return_format=return_format
        )

        if return_format == "dict":
            return Plan(**request)

        return request  # if the format is not a dict

    def create(self, plan: Plan,
               return_format: str = "dict") -> Union[Plan, bytes]:
        """Creates a new flight plan.

        Requires authentication.

        Parameters
        ----------
        plan : Plan
            The Plan object to register on the website
        return_format : str
            The API response format, defaults to ``"dict"``

        Returns
        -------
        Union[Plan, bytes]
            :class:`~flightplandb.datatypes.Plan` by default or if ``"dict"``
            is specified as the ``return_format``.

            ``bytes`` if a different format than ``"dict"`` was specified.

        Raises
        ------
        :class:`~flightplandb.exceptions.BadRequestException`
            The plan submitted had incorrect arguments
            or was otherwise unusable.
        """

        request = self._fp._post(
            "/plan/", return_format=return_format, json=plan._to_api_dict())

        if return_format == "dict":
            return Plan(**request)

        return request

    def edit(self, plan: Plan,
             return_format: str = "dict") -> Union[Plan, bytes]:
        """Edits a flight plan linked to your account.

        Requires authentication.

        Parameters
        ----------
        plan : Plan
            The new Plan object to replace the old one associated with that ID
        return_format : str
            The API response format, defaults to ``"dict"``

        Returns
        -------
        Union[Plan, bytes]
            :class:`~flightplandb.datatypes.Plan` by default or if ``"dict"``
            is specified as the ``return_format``.

            ``bytes`` if a different format than ``"dict"`` was specified.

        Raises
        ------
        :class:`~flightplandb.exceptions.BadRequestException`
            The plan submitted had incorrect arguments
            or was otherwise unusable.
        :class:`~flightplandb.exceptions.NotFoundException`
            No plan with the specified id was found.
        """

        plan_data = plan._to_api_dict()
        request = self._fp._patch(f"/plan/{plan_data['id']}", json=plan_data)

        if return_format == "dict":
            return Plan(**request)

        return request

    def delete(self, id_: int) -> StatusResponse:
        r"""Deletes a flight plan that is linked to your account.

        Requires authentication.

        Parameters
        ----------
        id\_ : int
            The ID of the flight plan to delete

        Returns
        -------
        StatusResponse
            OK 200 means a successful delete

        Raises
        ------
        :class:`~flightplandb.exceptions.NotFoundException`
            No plan with the specified id was found.
        """

        resp = self._fp._delete(f"/plan/{id_}")
        return(StatusResponse(**resp))

    def search(self, plan_query: PlanQuery, sort: str = "created",
               limit: int = 100) -> Generator[Plan, None, None]:
        """Searches for flight plans.
        A number of search parameters are available.
        They will be combined to form a search request.

        Requires authentication if route is included in results

        Parameters
        ----------
        plan_query : PlanQuery
            A dataclass containing multiple options for plan searches
        sort : str, optional
            Sort order to return results in. Valid sort orders are
            created, updated, popularity, and distance
        limit : int
            Maximum number of plans to return, defaults to 100

        Yields
        -------
        Generator[Plan, None, None]
            A generator containing :class:`~flightplandb.datatypes.Plan`
            objects.
            Each plan's :py:obj:`~flightplandb.datatypes.Plan.route`
            will be set to ``None`` unless otherwise specified in the
            :py:obj:`~flightplandb.datatypes.PlanQuery.includeRoute` parameter
            of the :class:`~flightplandb.datatypes.PlanQuery` used
            to request it
        """

        for i in self._fp._getiter("/search/plans",
                                   sort=sort,
                                   params=plan_query._to_api_dict(),
                                   limit=limit):
            yield Plan(**i)

    def has_liked(self, id_: int) -> bool:
        r"""Fetches your like status for a flight plan.

        Requires authentication.

        Parameters
        ----------
        id\_ : int
            ID of the flightplan to be checked

        Returns
        -------
        bool
            ``True``/``False`` to indicate that the plan was liked / not liked
        """

        sr = StatusResponse(
            **self._fp._get(f"/plan/{id_}/like", ignore_statuses=[404]))
        return sr.message != "Not Found"

    def like(self, id_: int) -> StatusResponse:
        r"""Likes a flight plan.

        Requires authentication.

        Parameters
        ----------
        id\_ : int
            ID of the flightplan to be liked

        Returns
        -------
        StatusResponse
            ``message=Created`` means the plan was successfully liked.
            ``message=OK`` means the plan was already liked.

        Raises
        ------
        :class:`~flightplandb.exceptions.InternalServerException`
            No plan with the specified id was found.
            (yeah, I don't know why it isn't ``NotFoundException`` either;
            ask the guy who made the API)
        """

        return StatusResponse(**self._fp._post(f"/plan/{id_}/like"))

    def unlike(self, id_: int) -> bool:
        r"""Removes a flight plan like.

        Requires authentication.

        Parameters
        ----------
        id\_ : int
            ID of the flightplan to be unliked

        Returns
        -------
        bool
            ``True`` for a successful unlike

        Raises
        ------
        :class:`~flightplandb.exceptions.NotFoundException`
            No plan with the specified id was found,
            or the plan was found but wasn't liked.
        """

        self._fp._delete(f"/plan/{id_}/like")
        return True

    def generate(self, gen_query: GenerateQuery,
                 return_format: str = "dict") -> Union[Plan, bytes]:
        """Creates a new flight plan using the route generator.

        Requires authentication.

        Parameters
        ----------
        gen_query : GenerateQuery
            A dataclass with options for flight plan generation
        return_format : str
            The API response format, defaults to ``"dict"``

        Returns
        -------
        Union[Plan, bytes]
            Plan by default or if ``"dict"`` is specified as
            the ``return_format``.

            Bytes if a different format than ``"dict"`` was specified
        """

        return Plan(
            **self._fp._post(
                "/auto/generate", json=gen_query._to_api_dict()))

    def decode(self, route: str) -> Plan:
        """Creates a new flight plan using the route decoder.

        Requires authentication.

        Parameters
        ----------
        route : str
            The route to decode. Use a comma or space separated string of
            waypoints, beginning and ending with valid airport ICAOs
            (e.g. KSAN BROWS TRM LRAIN KDEN). Airways are supported if they
            are preceded and followed by valid waypoints on the airway
            (e.g. 06TRA UL851 BEGAR). SID and STAR procedures are not
            currently supported and will be skipped, along with any
            other unmatched waypoints.

        Returns
        -------
        Plan
            The registered flight plan created on flight plan database,
            corresponding to the decoded route

        Raises
        ------
        :class:`~flightplandb.exceptions.BadRequestException`
            The encoded plan submitted had incorrect
            arguments or was otherwise unusable.
        """

        return Plan(**self._fp._post(
            "/auto/decode", json={"route": route}))
