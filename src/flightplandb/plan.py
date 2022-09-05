"""Flightplan-related commands."""
from typing import AsyncIterable, Union, Optional
from flightplandb.datatypes import (
    StatusResponse, PlanQuery,
    Plan, GenerateQuery
)
from flightplandb import internal


async def fetch(
    id_: int,
    return_format: str = "native",
    key: Optional[str] = None
) -> Union[Plan, None, bytes]:
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
        The API response format, defaults to ``"native"``.
        Must be one of the keys in the :ref:`permitted-return-types`.
    key : `str`, optional
        API authentication key.

    Returns
    -------
    Union[Plan, None, bytes]
        :class:`~flightplandb.datatypes.Plan` by default or if ``"native"``
        is specified as the ``return_format``.

        ``bytes`` if a different format than ``"native"`` was specified.

    Raises
    ------
    :class:`~flightplandb.exceptions.NotFoundException`
        No plan with the specified id was found.
    """

    request = await internal.get(
        path=f"/plan/{id_}",
        return_format=return_format,
        key=key
    )

    if return_format == "native":
        return Plan(**request)

    return request  # if the format is not a dict


async def create(
    plan: Plan,
    return_format: str = "native",
    key: Optional[str] = None
) -> Union[Plan, bytes]:
    """Creates a new flight plan.

    Requires authentication.

    Parameters
    ----------
    plan : Plan
        The Plan object to register on the website
    return_format : str
        The API response format, defaults to ``"native"``.
        Must be one of the keys in the :ref:`permitted-return-types`.
    key : `str`, optional
        API authentication key.

    Returns
    -------
    Plan
        The registered flight plan created on flight plan database

    Raises
    ------
    :class:`~flightplandb.exceptions.BadRequestException`
        The plan submitted had incorrect arguments or was
        otherwise unusable.
    """

    request = await internal.post(
        path="/plan/",
        return_format=return_format,
        json_data=plan.to_api_dict(),
        key=key)

    if return_format == "native":
        return Plan(**request)

    return request


async def edit(
    plan: Plan,
    return_format: str = "native",
    key: Optional[str] = None
) -> Union[Plan, bytes]:
    """Edits a flight plan linked to your account.

    Requires authentication.

    Parameters
    ----------
    plan : Plan
        The new Plan object to replace the old one associated with that ID
    return_format : str
        The API response format, defaults to ``"native"``.
        Must be one of the keys in the :ref:`permitted-return-types`.
    key : `str`, optional
        API authentication key.

    Returns
    -------
    Plan
        The registered flight plan created on flight plan database,
        corresponding to the route after being edited

    Raises
    ------
    :class:`~flightplandb.exceptions.BadRequestException`
        The plan submitted had incorrect arguments
        or was otherwise unusable.
    :class:`~flightplandb.exceptions.NotFoundException`
        No plan with the specified id was found.
    """

    plan_data = plan.to_api_dict()
    request = await internal.patch(
        path=f"/plan/{plan_data['id']}",
        return_format=return_format,
        json_data=plan_data,
        key=key)

    if return_format == "native":
        return Plan(**request)

    return request


async def delete(
    id_: int,
    key: Optional[str] = None
) -> StatusResponse:
    r"""Deletes a flight plan that is linked to your account.

    Requires authentication.

    Parameters
    ----------
    id\_ : int
        The ID of the flight plan to delete
    key : `str`, optional
        API authentication key.

    Returns
    -------
    StatusResponse
        OK 200 means a successful delete

    Raises
    ------
    :class:`~flightplandb.exceptions.NotFoundException`
        No plan with the specified id was found.
    """

    resp = await internal.delete(path=f"/plan/{id_}", key=key)
    return StatusResponse(**resp)


async def search(
    plan_query: PlanQuery,
    sort: str = "created",
    include_route: bool = False,
    limit: int = 100,
    key: Optional[str] = None
) -> AsyncIterable[Plan]:
    """Searches for flight plans.
    A number of search parameters are available.
    They will be combined to form a search request.

    Requires authentication if route is included in results

    Parameters
    ----------
    plan_query : PlanQuery
        A dataclass containing multiple options for plan searches
    sort : str
        Sort order to return results in. Valid sort orders are
        created, updated, popularity, and distance
    limit : int
        Maximum number of plans to return, defaults to 100
    include_route : bool
        Include route in response, defaults to False
    key : `str`, optional
        API authentication key.

    Yields
    -------
    AsyncIterable[Plan]
        An iterable containing :class:`~flightplandb.datatypes.Plan`
        objects.
    """

    request_json = plan_query.to_api_dict()
    request_json["includeRoute"] = include_route

    async for i in internal.getiter(
        path="/search/plans",
        sort=sort,
        params=request_json,
        limit=limit,
        key=key
    ):
        yield Plan(**i)


async def has_liked(
    id_: int,
    key: Optional[str] = None
) -> bool:
    r"""Fetches your like status for a flight plan.

    Requires authentication.

    Parameters
    ----------
    id\_ : int
        ID of the flightplan to be checked
    key : `str`, optional
        API authentication key.

    Returns
    -------
    bool
        ``True``/``False`` to indicate that the plan was liked / not liked
    """

    resp = await internal.get(
        path=f"/plan/{id_}/like",
        ignore_statuses=[404],
        key=key
    )
    status_response = StatusResponse(**resp)
    return status_response.message != "Not Found"


async def like(
    id_: int,
    key: Optional[str] = None
) -> StatusResponse:
    r"""Likes a flight plan.

    Requires authentication.

    Parameters
    ----------
    id\_ : int
        ID of the flightplan to be liked
    key : `str`, optional
        API authentication key.

    Returns
    -------
    StatusResponse
        ``message=Created`` means the plan was successfully liked.
        ``message=OK`` means the plan was already liked.

    Raises
    ------
    :class:`~flightplandb.exceptions.NotFoundException`
        No plan with the specified id was found.
    """

    resp = await internal.post(path=f"/plan/{id_}/like", key=key)
    return StatusResponse(**resp)


async def unlike(
    id_: int,
    key: Optional[str] = None
) -> bool:
    r"""Removes a flight plan like.

    Requires authentication.

    Parameters
    ----------
    id\_ : int
        ID of the flightplan to be unliked
    key : `str`, optional
        API authentication key.

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

    await internal.delete(path=f"/plan/{id_}/like", key=key)
    return True


async def generate(
    gen_query: GenerateQuery,
    include_route: bool = False,
    key: Optional[str] = None
) -> Union[Plan, bytes]:
    """Creates a new flight plan using the route generator.

    Requires authentication.

    Parameters
    ----------
    gen_query : GenerateQuery
        A dataclass with options for flight plan generation
    include_route : bool
        Include route in response, defaults to False
    key : `str`, optional
        API authentication key.

    Returns
    -------
    Plan
        The registered flight plan created on flight plan database,
        corresponding to the generated route
    include_route : bool, optional
        Include route in response, defaults to false
    """

    request_json = gen_query.to_api_dict()

    # due to an API bug this must be a string instead of a boolean
    request_json["includeRoute"] = "true" if include_route else "false"

    resp = await internal.post(
        path="/auto/generate",
        json_data=request_json,
        key=key
    )
    return Plan(**resp)


async def decode(
    route: str,
    key: Optional[str] = None
) -> Plan:
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
    key : `str`, optional
        API authentication key.

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

    resp = await internal.post(
        path="/auto/decode", json_data={"route": route}, key=key)
    return Plan(**resp)
