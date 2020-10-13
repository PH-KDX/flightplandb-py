#!/usr/bin/env python3

from typing import List, Union, Any, Optional
from dataclasses import dataclass, fields
from dateutil.parser import isoparse
from datetime import datetime
from enum import Enum


@dataclass
class StatusResponse():
    message: str
    errors: Union[List[str], None]


@dataclass
class User():
    # Unique user identifier number
    id: int
    # Username
    username: str
    # User provided location information.
    location: Optional[Union[str, None]] = None
    # Gravatar hash based on user's account email address.
    gravatarHash: Optional[str] = None


@dataclass
class Application():
    # Unique application identifier number
    id: int
    # Application name
    name: Optional[Union[str, None]] = None
    # Application URL
    url: Optional[Union[str, None]] = None


class RouteNodeType(Enum):
    UKN = "Unknown"
    APT = "Airport"
    NDB = "Non-directional beacon (NDB)"
    VOR = "VHF omni-directional range (VOR)"
    FIX = "Navigational fix"
    DME = "Distance measuring equipment"
    LATLON = "Latitude/Longitude point"

    def __deepcopy__(self, memo):
        return self.name


ViaType = Enum('ViaType', 'SID STAR AWY-HI AWY-LO NAT PACOT')
ViaType.__deepcopy__ = lambda self, memo: self.name  # type: ignore

# class ViaType(_ViaType):
#     def __deepcopy__(self, memo):
#         return self.name


@dataclass
class Via():
    ident: str
    type: ViaType

    def __post_init__(self):
        self.type = ViaType[self.type]


@dataclass
class RouteNode():
    # Node navaid identifier
    ident: str
    # Node type.
    type: RouteNodeType
    # Node latitude in decimal degrees
    lat: float
    # Node longitude in decimal degrees
    lon: float
    # Suggested altitude at node
    alt: float
    # Node name.
    name: Union[str, None]
    # Route to node.
    via: Union[Via, None]

    def __post_init__(self):
        self.type = RouteNodeType[self.type]
        self.via = Via(**self.via) if self.via else self.via


@dataclass
class Route():
    # An array of route nodes. A route must have at least 2 nodes
    nodes: List[RouteNode]

    def __post_init__(self):
        self.nodes = list(map(lambda x: RouteNode(**x), self.nodes))


@dataclass
class Plan():
    # Unique plan identifier number
    id: int
    # ICAO code of the departure airport
    fromICAO: Union[str, None]
    # ICAO code of the destination airport
    toICAO: Union[str, None]
    # Name of the departure airport
    fromName: Union[str, None]
    # Name of the destination airport
    toName: Union[str, None]
    # Flight number of the flight plan
    flightNumber: Optional[Union[str, None]] = None
    # Total distance of the flight plan route
    distance: Optional[float] = None
    # Maximum altitude of the flight plan route
    maxAltitude: Optional[float] = None
    # Number of nodes in the flight plan route
    waypoints: Optional[int] = None
    # Number of times the flight plan has been liked
    likes: Optional[int] = None
    # Number of times the flight plan has been downloaded
    downloads: Optional[int] = None
    # Relative popularity of the plan based on downloads and likes
    popularity: Optional[int] = None
    # Extra information about the flight plan
    notes: Optional[str] = None
    # Encoded polyline of the route, which can be used for quickly drawing maps
    encodedPolyline: Optional[str] = None
    # UTC Date and time of flight plan creation
    createdAt: Optional[datetime] = None
    # UTC Date and time of the last flight plan edit
    updatedAt: Optional[datetime] = None
    # Array of flight plan tags
    tags: Optional[List[str]] = None
    # User associated with the item. Null if no user linked
    user: Optional[Union[User, None]] = None
    # Application associated with the item. Null if no application linked
    application: Optional[Union[Application, None]] = None
    # The flight plan route.
    route: Optional[Route] = None

    # TODO: unknown keyword from server response
    cycle: Optional[Any] = None

    def __post_init__(self):
        self.createdAt = isoparse(self.createdAt)
        self.updatedAt = isoparse(self.updatedAt)

        self.user = User(**self.user) if self.user else self.user
        if self.application:
            self.application = Application(**self.application)
        self.route = Route(**self.route)


@dataclass
class PlanQuery():
    # Simple search query.
    # Search departure ICAO & name, destination ICAO & name,
    # username, tags and the flight number
    q: Optional[str] = None
    # From search query. Search departure ICAO & name
    From: Optional[str] = None
    # To search query. Search departure ICAO & name
    to: Optional[str] = None
    # Matches departure airport ICAO
    fromICAO: Optional[str] = None
    # Matches destination airport ICAO
    toICAO: Optional[str] = None
    # Matches departure airport name
    fromName: Optional[str] = None
    # Matches destination airport name
    toName: Optional[str] = None
    # Matches flight number
    flightNumber: Optional[str] = None
    # Minimum route distance
    distanceMin: Optional[str] = None
    # Maximum route distance, with units determined by the X-Units header
    distanceMax: Optional[str] = None
    # Tag names to search, comma separated
    tags: Optional[str] = None
    # Include route objects for each plan in the response.
    # Setting to true requires the request be authenticated with an API key
    includeRoute: Optional[str] = None
    # The page of results to fetch
    page: Optional[str] = None
    # The number of plans to return per page (max 100)
    limit: Optional[int] = None
    # The order of the returned plans. See Pagination for more options
    sort: Optional[str] = None

    def as_dict(self):
        return {
            f.name[0].lower()+f.name[1:]: getattr(self, f.name)
            for f in fields(self)
            if getattr(self, f.name)
        }
