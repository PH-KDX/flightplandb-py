#!/usr/bin/env python3

from typing import List, Union, Optional
from dataclasses import dataclass, fields
from dateutil.parser import isoparse
from datetime import datetime
from enum import Enum, EnumMeta, auto


@dataclass
class StatusResponse:
    message: str
    errors: Union[List[str], None]


@dataclass
class User:
    # Unique user identifier number
    id: int
    # Username
    username: str
    # User provided location information. Null if not available
    location: Optional[Union[str, None]] = None
    # Gravatar hash based on user's account email address.
    gravatarHash: Optional[str] = None
    # UTC Date and time of user registration
    joined: Optional[datetime] = None
    # UTC Date and time the user was last connected
    lastSeen: Optional[datetime] = None
    # Number of flight plans created by the user
    plansCount: Optional[int] = 0
    # Total distance of all user's flight plans
    plansDistance: Optional[float] = 0.0
    # Total download count of all user's plans
    plansDownloads: Optional[int] = 0
    # Total like count of all user's plans
    plansLikes: Optional[int] = 0

    def __post_init__(self):
        self.joined = isoparse(self.joined) \
            if self.joined else self.joined
        self.lastSeen = isoparse(self.lastSeen) \
            if self.lastSeen else self.lastSeen


@dataclass
class Application:
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

    def __str__(self):
        return self.value


# ViaType = Enum('ViaType', 'SID STAR AWY-HI AWY-LO NAT PACOT')
# ViaType.__deepcopy__ = lambda self, memo: self.name  # type: ignore

class ViaTypeMeta(EnumMeta):
    def __getitem__(cls, name):
        return cls._member_map_[name.replace("-", "_")]


class ViaType(Enum, metaclass=ViaTypeMeta):
    SID = auto()
    STAR = auto()
    AWY_HI = auto()
    AWY_LO = auto()
    NAT = auto()
    PACOT = auto()


@dataclass
class Via:
    ident: str
    type: ViaType

    def __post_init__(self):
        self.type = ViaType[self.type]


@dataclass
class RouteNode:
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
        self.via = Via(**self.via) if type(self.via) == dict else self.via


@dataclass
class Route:
    # An array of route nodes. A route must have at least 2 nodes
    nodes: List[RouteNode]

    def __post_init__(self):
        self.nodes = list(
            map(
                lambda x: RouteNode(**x) if type(x) == dict else x,
                self.nodes
                )
            )


@dataclass
class Cycle:
    # FlightPlanDB cycle id
    id: int
    # AIP-style cycle id
    ident: str
    # last two digits of cycle year
    year: int
    # cycle release
    release: int


@dataclass
class Plan:
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
    # The flight plan route
    route: Optional[Route] = None
    # The navigation data cycle
    cycle: Optional[Cycle] = None

    def __post_init__(self):
        self.createdAt = (isoparse(self.createdAt)
                          if type(self.createdAt) != datetime
                          else self.createdAt)
        self.updatedAt = (isoparse(self.updatedAt)
                          if type(self.updatedAt) != datetime
                          else self.updatedAt)

        self.user = User(**self.user) if self.user else self.user
        if self.application:
            self.application = Application(**self.application)
        self.route = (Route(**self.route)
                      if type(self.route) == dict else self.route)
        self.cycle = (Cycle(**self.cycle)
                      if type(self.cycle) == dict else self.cycle)


@dataclass
class PlanQuery:
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


@dataclass
class GenerateQuery:
    # Generate plan query.
    # The departure airport ICAO code
    fromICAO: str
    # The destination airport ICAO code
    toICAO: str
    # Use North Atlantic Tracks in the route generation
    useNAT: Optional[bool] = True
    # Use Pacific Organized Track System tracks in the route generation
    usePACOT: Optional[bool] = True
    # Use low-level airways in the route generation
    useAWYLO: Optional[bool] = True
    # Use high-level airways in the route generation
    useAWYHI: Optional[bool] = True
    # Basic flight profile cruise altitude (altitude)
    cruiseAlt: Optional[float] = 35000
    # Basic flight profile cruise speed (speed)
    cruiseSpeed: Optional[float] = 420
    # Basic flight profile ascent rate (climb rate)
    ascentRate: Optional[float] = 2500
    # Basic flight profile ascent speed (speed)
    ascentSpeed: Optional[float] = 250
    # Basic flight profile descent rate (climb rate)
    descentRate: Optional[float] = 1500
    # Basic flight profile descent speed (speed)
    descentSpeed: Optional[float] = 250


@dataclass
class Tag:
    # Tag name
    name: str
    # Description of the tag. Null if no description is available
    description: Union[str, None]
    # Number of plans with this tag
    planCount: int
    # Popularity index of the tag
    popularity: int


@dataclass
class Timezone:
    # The IANA timezone the airport is located in. Null if not available
    name: Union[str, None]
    # The number of seconds the airport timezone is currently offset from UTC.
    # Positive is ahead of UTC. Null if not available
    offset: Union[float, None]


@dataclass
class Times:
    # Time of sunrise
    sunrise: datetime
    # time of sunset
    sunset: datetime
    # time of dawn
    dawn: datetime
    # time of dusk
    dusk: datetime

    def __post_init__(self):
        self.sunrise = (isoparse(self.sunrise)
                        if type(self.sunrise) != datetime
                        else self.sunrise)
        self.sunset = (isoparse(self.sunset)
                       if type(self.sunset) != datetime
                       else self.sunset)
        self.dawn = (isoparse(self.dawn)
                     if type(self.dawn) != datetime
                     else self.dawn)
        self.dusk = (isoparse(self.dusk)
                     if type(self.dusk) != datetime
                     else self.dusk)


@dataclass
class RunwayEnds:
    # The identifier of the runway end
    ident: str
    # The latitude of the runway end
    lat: float
    # The longitude of the runway end
    lon: float


NavaidType = Enum('NavaidType', 'LOC-ILS LOC-LOC GS DME')
NavaidType.__deepcopy__ = lambda self, memo: self.name  # type: ignore


@dataclass
class Navaid:
    # The navaid identifier
    ident: str
    # The navaid type. One of
    type: NavaidType
    # The navaid latitude
    lat: float
    # The navaid longitude
    lon: float
    # The airport associated with the navaid
    airport: str
    # The runway associated with the navaid
    runway: str
    # The navaid frequency in Hz. Null if not available
    frequency: Union[float, None]
    # The navaid slope in degrees from horizontal used for type GS
    slope: Union[float, None]
    # The navaid bearing in true degrees. Null if not available
    bearing: Union[float, None]
    # The navaid name. Null if not available
    name: Union[float, None]
    # The navaid elevation above mean sea level (elevation)
    elevation: float
    # The navaid range, with units determined by the X-Units header (distance)
    range: float

    def __post_init__(self):
        self.type = NavaidType[self.type]


@dataclass
class Runway:
    # The runway identifier
    ident: str
    # The runway width, with units determined by the X-Units header (length)
    width: float
    # The runway length, with units determined by the X-Units header (length)
    length: float
    # The runway bearing in true degrees
    bearing: float
    # The runway surface material
    surface: str
    # Array of strings of runway markings
    markings: List[str]
    # Array of strings of runway lighting types
    lighting: List[str]
    # The distance of the displaced threshold from the runway end (length)
    thresholdOffset: float
    # The runway overrun length, with units determined by the X-Units header
    overrunLength: float
    # Two element array containing the location of the two ends of the runway
    ends: List[RunwayEnds]
    # Array of navaids associated with the current runway
    navaids: List[Navaid]

    def __post_init__(self):
        self.ends = list(map(lambda rw: RunwayEnds(**rw), self.ends))
        self.navaids = list(map(lambda n: Navaid(**n), self.navaids))


@dataclass
class Frequency:
    # The frequency type
    type: str
    # The frequency in Hz
    frequency: float
    # The frequency name. Null if not available
    name: Union[str, None]


@dataclass
class Weather:
    # Current METAR report for the airport
    METAR: Union[str, None]
    # Current TAF report for the airport
    TAF: Union[str, None]


@dataclass
class Airport:
    # The airport ICAO code
    ICAO: str
    # The airport IATA code. Null if not available
    IATA: Union[str, None]
    # The airport name
    name: str
    # The geographical region the airport is located in. Null if not available
    regionName: Union[str, None]
    # The airport elevation above mean sea level (elevation)
    elevation: float
    # The airport latitude in degrees
    lat: float
    # The airport longitude in degrees
    lon: float
    # The current magnetic variation/declination at the airport,
    # based on the World Magnetic Model
    magneticVariation: float
    # The airport timezone information
    timezone: Timezone
    # Relevant times at the airport
    times: Times
    # The number of runways at the airport
    runwayCount: int
    # Array of runways.
    # Note: each physical runway will appear twice, once from each end
    runways: List[Runway]
    # Array of frequencies associated with the airport
    frequencies: List[Frequency]
    # Airport weather information
    weather: Weather

    def __post_init__(self):
        self.timezone = Timezone(**self.timezone)
        self.runways = list(map(lambda rw: Runway(**rw), self.runways))
        self.frequencies = list(
            map(lambda rw: Frequency(**rw), self.frequencies))
        self.weather = Weather(**self.weather)


@dataclass
class Track:
    # Track identifier
    ident: str
    route: Route
    validFrom: datetime
    validTo: datetime

    def __port_init__(self):
        self.validFrom = isoparse(self.validFrom)
        self.validTo = isoparse(self.validTo)
