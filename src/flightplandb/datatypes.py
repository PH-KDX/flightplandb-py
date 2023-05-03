#!/usr/bin/env python3

# Copyright 2021 PH-KDX
# This file is part of FlightplanDB-py.

# FlightplanDB-py is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FlightplanDB-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with FlightplanDB-py.  If not, see <https://www.gnu.org/licenses/>.


from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

from dateutil.parser import isoparse


def _datetime_to_iso(timestamp: datetime):
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


@dataclass
class StatusResponse:
    """
    Returned for some functions to indicate execution status

    Attributes
    ----------
    message : str
        The message associated with the status returned
    errors : Optional[List[str]]
        A list of any errors raised
    """

    message: str
    errors: Optional[List[str]]

    def to_api_dict(self):
        return self.__dict__


@dataclass
class User:
    """Describes users registered on the website

    Attributes
    ----------
    id : int
        Unique user identifier number
    username : str
        Username
    location : Optional[str]
        User provided location information. ``None`` if not available
    gravatarHash : Optional[str]
        Gravatar hash based on user's account email address.
    joined : Optional[datetime] = None
        UTC Date and time of user registration
    lastSeen : Optional[datetime] = None
        UTC Date and time the user was last connected
    plansCount : Optional[int]
        Number of flight plans created by the user
    plansDistance : Optional[float]
        Total distance of all user's flight plans
    plansDownloads : Optional[int]
        Total download count of all user's plans
    plansLikes : Optional[int]
        Total like count of all user's plans
    """

    id: int
    username: str
    location: Optional[str] = None
    gravatarHash: Optional[str] = None
    joined: Optional[datetime] = None
    lastSeen: Optional[datetime] = None
    plansCount: Optional[int] = 0
    plansDistance: Optional[float] = 0.0
    plansDownloads: Optional[int] = 0
    plansLikes: Optional[int] = 0

    def __post_init__(self):
        if self.joined and isinstance(self.joined, str):
            self.joined = isoparse(self.joined)
        if self.lastSeen and isinstance(self.lastSeen, str):
            self.lastSeen = isoparse(self.lastSeen)

    def to_api_dict(self):
        resp_dict = self.__dict__
        if isinstance(resp_dict["joined"], datetime):
            resp_dict["joined"] = _datetime_to_iso(resp_dict["joined"])
        if isinstance(resp_dict["lastSeen"], datetime):
            resp_dict["lastSeen"] = _datetime_to_iso(resp_dict["lastSeen"])
        return resp_dict


@dataclass
class UserSmall:
    """Describes users registered on the website, with far less info

    Attributes
    ----------
    id : int
        Unique user identifier number
    username : str
        Username
    location : Optional[str]
        User provided location information. ``None`` if not available
    gravatarHash : Optional[str]
        Gravatar hash based on user's account email address.
    """

    id: int
    username: str
    location: Optional[str] = None
    gravatarHash: Optional[str] = None

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Application:
    """Describes application associated with a flight plan

    Attributes
    ----------
    id : int
        Unique application identifier number
    name : Optional[str]
        Application name
    url : Optional[str]
        Application URL
    """

    id: int
    name: Optional[str] = None
    url: Optional[str] = None

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Via:
    """Describes routes to :class:`RouteNode` s

    Attributes
    ----------
    ident : str
        desc
    type : str
        Type of Via; must be one of :py:obj:`Via.validtypes`
    validtypes : List[str]
        Do not change. Valid Via types.
    """

    ident: str
    type: str

    validtypes = ["SID", "STAR", "AWY-HI", "AWY-LO", "NAT", "PACOT"]

    def __post_init__(self):
        if self.type not in self.validtypes:
            raise ValueError(f"{self.type} is not a valid Via type")

    def to_api_dict(self):
        return self.__dict__


@dataclass
class RouteNode:
    """Describes nodes in :class:`Route` s

    Attributes
    ----------
    id: Optional[int]
        For some obscure reason an apparently useless id is included with
        each node when the node is inside a :class:`Track` route.
        Goodness knows why.
    ident : str
        Node navaid identifier
    type : str
        Type of RouteNode; must be one of :py:obj:`RouteNode.validtypes`
    lat : float
        Node latitude in decimal degrees
    lon : float
        Node longitude in decimal degrees
    alt : Optional[float]
        Suggested altitude at node
    name : Optional[str]
        Node name.
    via : Optional[Via]
        Route to node.
    validtypes : List[str]
        Do not change. Valid RouteNode types.
    """

    ident: str
    type: str
    lat: float
    lon: float
    id: Optional[int] = None
    alt: Optional[float] = None
    name: Optional[str] = None
    via: Optional[Via] = None

    validtypes = ["UKN", "APT", "NDB", "VOR", "FIX", "DME", "LATLON"]

    def __post_init__(self):
        if self.type not in self.validtypes:
            raise ValueError(f"{self.type} is not a valid RouteNode type")
        self.via = Via(**self.via) if isinstance(self.via, dict) else self.via

    def to_api_dict(self):
        resp_dict = self.__dict__
        if resp_dict["via"] and isinstance(resp_dict["via"], Via):
            resp_dict["via"] = resp_dict["via"].to_api_dict()
        return resp_dict


@dataclass
class Route:
    """Describes the route of a :class:`Plan`

    Attributes
    ----------
    nodes : List[RouteNode]
        A list of :class:`RouteNode` s. A route must have at least 2 nodes.
    eastLevels : Optional[List[str]]
        Valid eastbound flightlevels. Only used inside a NATS :class:`Track`.
    westLevels : Optional[List[str]]
        Valid westbound flightlevels. Only used inside a NATS :class:`Track`.
    """

    nodes: List[RouteNode]
    eastLevels: Optional[List[str]] = None
    westLevels: Optional[List[str]] = None

    def __post_init__(self):
        self.nodes = list(
            map(
                lambda node: (RouteNode(**node) if (isinstance(node, dict)) else node),
                self.nodes,
            )
        )

    def to_api_dict(self):
        resp_dict = self.__dict__
        resp_dict["nodes"] = list(
            map(lambda node: node.to_api_dict(), resp_dict["nodes"])
        )
        return resp_dict


@dataclass
class Cycle:
    """Navdata cycle

    Attributes
    ----------
    id : int
        FlightPlanDB cycle id
    ident : str
        AIP-style cycle id
    year : int
        Last two digits of cycle year
    release : int
        Cycle release
    """

    id: int
    ident: str
    year: int
    release: int

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Plan:
    """A flight plan; the thing this whole API revolves around

    Attributes
    ----------
    id : int
        Unique plan identifier number
    fromICAO : Optional[str]
        ICAO code of the departure airport
    toICAO : Optional[str]
        ICAO code of the destination airport
    fromName : Optional[str]
        Name of the departure airport
    toName : Optional[str]
        Name of the destination airport
    flightNumber : Optional[str]
        Flight number of the flight plan
    distance : Optional[float]
        Total distance of the flight plan route
    maxAltitude : Optional[float]
        Maximum altitude of the flight plan route
    waypoints : Optional[int]
        Number of nodes in the flight plan route
    likes : Optional[int]
        Number of times the flight plan has been liked
    downloads : Optional[int]
        Number of times the flight plan has been downloaded
    popularity : Optional[int]
        Relative popularity of the plan based on downloads and likes
    notes : Optional[str]
        Extra information about the flight plan
    encodedPolyline : Optional[str]
        Encoded polyline of route, which can be used for quickly drawing maps
    createdAt : Optional[datetime]
        UTC Date and time of flight plan creation
    updatedAt : Optional[datetime]
        UTC Date and time of the last flight plan edit
    tags : Optional[List[str]]
        List of flight plan tags
    user : Optional[User]
        User associated with the item. ``None`` if no user linked
    application : Optional[Application]
        Application associated with the item. ``None`` if no application linked
    route : Optional[Route]
        The flight plan route
    cycle : Optional[Cycle]
        Navigation data cycle associated with the item.
        ``None`` if no cycle linked
    """

    fromICAO: Optional[str]
    toICAO: Optional[str]
    fromName: Optional[str]
    toName: Optional[str]
    id: Optional[int] = None
    flightNumber: Optional[str] = None
    distance: Optional[float] = None
    maxAltitude: Optional[float] = None
    waypoints: Optional[int] = None
    likes: Optional[int] = None
    downloads: Optional[int] = None
    popularity: Optional[int] = None
    notes: Optional[str] = None
    encodedPolyline: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    tags: Optional[List[str]] = None
    user: Optional[User] = None
    application: Optional[Application] = None
    route: Optional[Route] = None
    cycle: Optional[Cycle] = None

    def __post_init__(self):
        if self.createdAt and type(self.createdAt) != datetime:
            self.createdAt = isoparse(self.createdAt)

        if self.updatedAt and type(self.updatedAt) != datetime:
            self.updatedAt = isoparse(self.updatedAt)

        if self.user and isinstance(self.user, dict):
            self.user = User(**self.user)

        if self.application and isinstance(self.application, dict):
            self.application = Application(**self.application)

        if self.route and isinstance(self.route, dict):
            self.route = Route(**self.route)

        if self.cycle and isinstance(self.cycle, dict):
            self.cycle = Cycle(**self.cycle)

    def to_api_dict(self):
        plan_dict = self.__dict__
        if isinstance(plan_dict["createdAt"], datetime):
            plan_dict["createdAt"] = _datetime_to_iso(plan_dict["createdAt"])
        if isinstance(plan_dict["updatedAt"], datetime):
            plan_dict["updatedAt"] = _datetime_to_iso(plan_dict["updatedAt"])
        if isinstance(plan_dict["user"], User):
            plan_dict["user"] = plan_dict["user"].to_api_dict()
        if isinstance(plan_dict["route"], Route):
            plan_dict["route"] = plan_dict["route"].to_api_dict()
        return plan_dict


@dataclass
class PlanQuery:
    """Simple search query.

    Attributes
    ----------
    q : Optional[str]
        Username, tags and the flight number
    From : Optional[str]
        From search query. Search departure ICAO & name
    to : Optional[str]
        To search query. Search departure ICAO & name
    fromICAO : Optional[str]
        Matches departure airport ICAO
    toICAO : Optional[str]
        Matches destination airport ICAO
    fromName : Optional[str]
        Matches departure airport name
    toName : Optional[str]
        Matches destination airport name
    flightNumber : Optional[str]
        Matches flight number
    distanceMin : Optional[str]
        Minimum route distance
    distanceMax : Optional[str]
        Maximum route distance, with units determined by the X-Units header
    tags : Optional[List[str]]
        List of tag names to search
    """

    q: Optional[str] = None
    From: Optional[str] = None
    to: Optional[str] = None
    fromICAO: Optional[str] = None
    toICAO: Optional[str] = None
    fromName: Optional[str] = None
    toName: Optional[str] = None
    flightNumber: Optional[str] = None
    distanceMin: Optional[str] = None
    distanceMax: Optional[str] = None
    tags: Optional[List[str]] = None
    includeRoute: Optional[bool] = None

    def to_api_dict(self):
        plan_query_dict = self.__dict__
        if self.tags:
            plan_query_dict["tags"] = ", ".join(self.tags)
        return plan_query_dict


@dataclass
class GenerateQuery:
    """Generate plan query.

    Attributes
    ----------
    fromICAO : str
        The departure airport ICAO code
    toICAO : str
        The destination airport ICAO code
    useNAT : Optional[bool]
        Use Pacific Organized Track System tracks in the route generation
    usePACOT : Optional[bool]
        Use Pacific Organized Track System tracks in the route generation
    useAWYLO : Optional[bool]
        Use low-level airways in the route generation
    useAWYHI : Optional[bool]
        Use high-level airways in the route generation
    cruiseAlt : Optional[float]
        Basic flight profile cruise altitude (altitude)
    cruiseSpeed : Optional[float]
        Basic flight profile cruise speed (speed)
    ascentRate : Optional[float]
        Basic flight profile ascent rate (climb rate)
    ascentSpeed : Optional[float]
        Basic flight profile ascent speed (speed)
    descentRate : Optional[float]
        Basic flight profile descent rate (climb rate)
    descentSpeed : Optional[float]
        Basic flight profile descent speed (speed)
    """

    fromICAO: str
    toICAO: str
    useNAT: Optional[bool] = True
    usePACOT: Optional[bool] = True
    useAWYLO: Optional[bool] = True
    useAWYHI: Optional[bool] = True
    cruiseAlt: Optional[float] = 35000
    cruiseSpeed: Optional[float] = 420
    ascentRate: Optional[float] = 2500
    ascentSpeed: Optional[float] = 250
    descentRate: Optional[float] = 1500
    descentSpeed: Optional[float] = 250

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Tag:
    """Flight plan tag

    Attributes
    ----------
    name : str
        Tag name
    description : Optional[str]
        Description of the tag. ``None`` if no description is available
    planCount : int
        Number of plans with this tag
    popularity: int
        Popularity index of the tag
    """

    name: str
    description: Optional[str]
    planCount: int
    popularity: int

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Timezone:
    """Contains timezone information

    Attributes
    ----------
    name : Optional[str]
        The IANA timezone the airport is located in. ``None`` if not available
    offset : Optional[float]
        The number of seconds the airport timezone is currently
        offset from UTC. Positive is ahead of UTC. ``None`` if not available
    """

    name: Optional[str]
    offset: Optional[float]

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Times:
    """Contains relevant times information

    Attributes
    ----------
    sunrise : datetime
        Time of sunrise
    sunset : datetime
        Time of sunset
    dawn : datetime
        Time of dawn
    dusk : datetime
        Time of dusk
    """

    sunrise: datetime
    sunset: datetime
    dawn: datetime
    dusk: datetime

    def __post_init__(self):
        self.sunrise = (
            isoparse(self.sunrise)
            if not isinstance(self.sunrise, datetime)
            else self.sunrise
        )
        self.sunset = (
            isoparse(self.sunset)
            if not isinstance(self.sunset, datetime)
            else self.sunset
        )
        self.dawn = (
            isoparse(self.dawn) if not isinstance(self.dawn, datetime) else self.dawn
        )
        self.dusk = (
            isoparse(self.dusk) if not isinstance(self.dusk, datetime) else self.dusk
        )

    def to_api_dict(self):
        plan_dict = self.__dict__
        plan_dict["sunrise"] = _datetime_to_iso(plan_dict["sunrise"])
        plan_dict["sunset"] = _datetime_to_iso(plan_dict["sunset"])
        plan_dict["dawn"] = _datetime_to_iso(plan_dict["dawn"])
        plan_dict["dusk"] = _datetime_to_iso(plan_dict["dusk"])
        return plan_dict


@dataclass
class RunwayEnds:
    """Ends of :class:`Runway` . No duh.

    Attributes
    ----------
    ident : str
        The identifier of the runway end
    lat : float
        The latitude of the runway end
    lon : float
        The longitude of the runway end
    """

    ident: str
    lat: float
    lon: float

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Navaid:
    """Describes a navigational aid

    Attributes
    ----------
    ident: str
        The navaid identifier
    type: str
        The navaid type. Must be one of :py:obj:`Navaid.validtypes`
    lat: float
        The navaid latitude
    lon: float
        The navaid longitude
    airport: str
        The airport associated with the navaid
    runway: str
        The runway associated with the navaid
    frequency: Optional[float]
        The navaid frequency in Hz. ``None`` if not available
    slope: Optional[float]
        The navaid slope in degrees from horizontal used for type GS
    bearing: Optional[float]
        The navaid bearing in true degrees. ``None`` if not available
    name: Optional[str]
        The navaid name. ``None`` if not available
    elevation: float
        The navaid elevation above mean sea level (elevation)
    range: float
        The navaid range; units determined by the X-Units header (distance)
    validtypes : List[str]
        Do not change. Valid Navaid types.
    """

    ident: str
    type: str
    lat: float
    lon: float
    airport: str
    runway: str
    frequency: Optional[float]
    slope: Optional[float]
    bearing: Optional[float]
    name: Optional[str]
    elevation: float
    range: float

    validtypes = ["LOC-ILS", "LOC-LOC", "GS", "DME", "OM", "MM", "IM"]

    def __post_init__(self):
        if self.type not in self.validtypes:
            raise ValueError(f"{self.type} is not a valid Navaid type")

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Runway:
    """Describes a runway at an :class:`Airport`

    Attributes
    ----------
    ident: str
        The runway identifier
    width: float
        The runway width, with units determined by the X-Units header (length)
    length: float
        The runway length, with units determined by the X-Units header (length)
    bearing: float
        The runway bearing in true degrees
    surface: str
        The runway surface material
    markings: List[str]
        List of strings of runway markings
    lighting: List[str]
        List of strings of runway lighting types
    thresholdOffset: float
        The distance of the displaced threshold from the runway end (length)
    overrunLength: float
        The runway overrun length, with units determined by the X-Units header
    ends: List[RunwayEnds]
        Two element List containing the location of the two ends of the runway
    navaids: List[Navaid]
        List of navaids associated with the current runway
    """

    ident: str
    width: float
    length: float
    bearing: float
    surface: str
    markings: List[str]
    lighting: List[str]
    thresholdOffset: float
    overrunLength: float
    ends: List[RunwayEnds]
    navaids: List[Navaid]

    def __post_init__(self):
        if self.ends and (isinstance(self.ends[0], dict)):
            self.ends = list(map(lambda rw: RunwayEnds(**rw), self.ends))
        if self.navaids and (isinstance(self.navaids[0], dict)):
            self.navaids = list(map(lambda n: Navaid(**n), self.navaids))

    def to_api_dict(self):
        resp_dict = self.__dict__
        resp_dict["ends"] = list(map(lambda end: end.to_api_dict(), resp_dict["ends"]))
        resp_dict["navaids"] = list(
            map(lambda aid: aid.to_api_dict(), resp_dict["navaids"])
        )
        return resp_dict


@dataclass
class Frequency:
    """Holds frequency information

    Attributes
    ----------
    type : str
        The frequency type
    frequency : float
        The frequency in Hz
    name : Optional[str]
        The frequency name. ``None`` if not available

    """

    type: str
    frequency: float
    name: Optional[str]

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Weather:
    """Contains weather reports and predictions

    Attributes
    ----------
    METAR : Optional[str]
        Current METAR report for the airport
    TAF : Optional[str]
        Current TAF report for the airport
    """

    METAR: Optional[str]
    TAF: Optional[str]

    def to_api_dict(self):
        return self.__dict__


@dataclass
class Airport:
    """Describes an airport.
    An oversized dataclass with more information than you'd need in 500 years.

    Attributes
    ----------
    ICAO: str
        The airport ICAO code
    IATA: Optional[str]
        The airport IATA code. ``None`` if not available
    name: str
        The airport name
    regionName: Optional[str]
        The geographical region the airport is located in.
        ``None`` if not available
    elevation: float
        The airport elevation above mean sea level (elevation)
    lat: float
        The airport latitude in degrees
    lon: float
        The airport longitude in degrees
    magneticVariation: float
        The current magnetic variation/declination at the airport,
        based on the World Magnetic Model
    timezone: Timezone
        The airport timezone information
    times: Times
        Relevant times at the airport
    runwayCount: int
        The number of runways at the airport
    runways: List[Runway]
        List of runways.
        Note: each physical runway will appear twice, once from each end
    frequencies: List[Frequency]
        List of frequencies associated with the airport
    weather: Weather
        Airport weather information
    """

    ICAO: str
    IATA: Optional[str]
    name: str
    regionName: Optional[str]
    elevation: float
    lat: float
    lon: float
    magneticVariation: float
    timezone: Timezone
    times: Times
    runwayCount: int
    runways: List[Runway]
    frequencies: List[Frequency]
    weather: Weather

    def __post_init__(self):
        if self.timezone and isinstance(self.timezone, dict):
            self.timezone = Timezone(**self.timezone)

        if self.times and isinstance(self.times, dict):
            self.times = Times(**self.times)

        if self.runways and isinstance(self.runways[0], dict):
            self.runways = list(map(lambda rw: Runway(**rw), self.runways))

        if self.frequencies and isinstance(self.frequencies[0], dict):
            self.frequencies = list(map(lambda rw: Frequency(**rw), self.frequencies))

        if self.weather and isinstance(self.weather, dict):
            self.weather = Weather(**self.weather)

    def to_api_dict(self):
        resp_dict = self.__dict__
        resp_dict["timezone"] = resp_dict["timezone"].to_api_dict()
        resp_dict["times"] = resp_dict["times"].to_api_dict()
        resp_dict["runways"] = list(
            map(lambda rwy: rwy.to_api_dict(), resp_dict["runways"])
        )
        resp_dict["frequencies"] = list(
            map(lambda freq: freq.to_api_dict(), resp_dict["frequencies"])
        )
        resp_dict["weather"] = resp_dict["weather"].to_api_dict()
        return resp_dict


@dataclass
class Track:
    """Used for NATS and PACOTS tracks

    Attributes
    ----------
    ident: Union[str, int]
        Track identifier; str in NATS, int in PACOTS
    route : Route
        Route of the track
    validFrom : datetime
        UTC datetime the track is valid from
    validTo : datetime
        UTC datetime the track is valid to
    """

    ident: Union[str, int]
    route: Route
    validFrom: datetime
    validTo: datetime

    def __post_init__(self):
        if self.route and isinstance(self.route, dict):
            self.route = Route(**self.route)
        if self.validFrom and isinstance(self.validFrom, str):
            self.validFrom = isoparse(self.validFrom)
        if self.validTo and isinstance(self.validTo, str):
            self.validTo = isoparse(self.validTo)

    def to_api_dict(self):
        resp_dict = self.__dict__
        if isinstance(resp_dict["validFrom"], datetime):
            resp_dict["validFrom"] = _datetime_to_iso(resp_dict["validFrom"])
        if isinstance(resp_dict["validTo"], datetime):
            resp_dict["validTo"] = _datetime_to_iso(resp_dict["validTo"])
        return resp_dict


@dataclass
class SearchNavaid:
    """Describes a navigational aid, as returned by the search function

    Attributes
    ----------
    ident: str
        The navaid identifier
    type: str
        The navaid type. Must be one of :py:obj:`SearchNavaid.validtypes`
    lat: float
        The navaid latitude
    lon: float
        The navaid longitude
    elevation: float
        The navaid elevation above mean sea level (elevation)
    runwayIdent: Optional[str]
        The runway associated with the navaid. ``None`` if not available
    airportICAO: Optional[str]
        The ICAO of the airport associated with the navaid.
        ``None`` if not available
    name: Optional[float]
        The navaid name. ``None`` if not available
    validtypes : List[str]
        Do not change. Valid SearchNavaid types
    """

    ident: str
    type: str
    lat: float
    lon: float
    elevation: float
    runwayIdent: Optional[str] = None
    airportICAO: Optional[str] = None
    name: Optional[float] = None

    validtypes = ["UKN", "APT", "NDB", "VOR", "FIX", "DME", "LATLON"]

    def __post_init__(self):
        if self.type not in self.validtypes:
            raise ValueError(f"{self.type} is not a valid SearchNavaid type")

    def to_api_dict(self):
        return self.__dict__
