<!--
Copyright 2020 PH-KDX
This file is part of FlightplanDB-python.

FlightplanDB-python is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FlightplanDB-python is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with FlightplanDB-python.  If not, see <https://www.gnu.org/licenses/>.
-->

# FlightplanDB-python

<!-- TOC titleSize:2 tabSpaces:2 depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 skip:0 title:1 charForUnorderedList:* -->
## Table of Contents
* [FlightplanDB-python](#flightplandb-python)
  * [Introduction](#introduction)
  * [Data format](#data-format)
    * [General](#general)
    * [Header](#header)
    * [Flight plan response](#flight-plan-response)
  * [Commands](#commands)
    * [API class](#api-class)
    * [Plan class](#plan-class)
      * [Like class](#like-class)
    * [Nav class](#nav-class)
      * [Airport class](#airport-class)
    * [User class](#user-class)
<!-- /TOC -->

## Introduction
This is a Python 3 wrapper for the Flight Plan Database API. Please read the terms of use for this API at [https://flightplandatabase.com/dev/api](https://flightplandatabase.com/dev/api). A large part of this documentation also comes from that website.

This library consists of several classes of commands. They are as follows:
  * API - Commands in here pertain to the API interface itself.
  * Plan - Flight plan creation, removal, editing etc.
    * Like (subclass of Plan) - You might like some flight plans more than others. This section allows you to express your deepest feelings.
  * Nav - Everything related to navigation, including airways, waypoints, and airport info.
    * Airport (subclass of Nav) - These commands retrieve information about airports.
  * User - Data about the users of Flight Plan Database.

Authentication occurs using the HTTPBasicAuth scheme. An API token is passed, referred to in here as `key`, as the username only. No password is used. It is recommended to keep the token outside of your code, using something like `python-dotenv`.

When using this wrapper, `key` needs to be passed as the first argument for every request.

This wrapper does not support changing the units in which the flight plans are returned to anything other than aviation units, and that's not on the to-do list. Feel free to implement it yourself in a branch, however, and push the changed branch back to main.


## Data format
### General
All commands in this wrapper return two variables: `headers`, which is the response headers, and `result`, which is the message response returned by the server. The first one is always a dict, and the second one is a native Python structure such as dicts or booleans. If the server returns an invalid status code, the wrapper will raise an HTTPError.

### Header
A typical header dict looks as follows. Note that choosing pages or units has not been implemented in this wrapper, so the units, for instance, will always be `AVIATION`. When headers are not applicable to the response, they will not be included. In the code examples in this file, I have placed the intended value of each field and its type between `<>` brackets. :
```
{
    "X-API-Version":<api version that returned response, int>
    "X-Units":<units system used for numerical values, str>
    "X-Limit-Cap":<limit of requests per day on hourly rolling basis, int>
    "X-Limit-By":<what the limit is based on, str>
    "X-Limit-Used":<requests used so far of the quota, int>
    "X-Page-Count":<number of pages of result available, int>
    "X-Page-Current":<the current page returned, int>
    "X-Page-PerPage":<number of items per page, int>
    "X-Item-Count":<number of items available, int>
    "X-Sort":<sort order for returned results, str>
    "Links":<HTTP link header with links to related data, str>
}
```

### Flight plan response
By default, flight plan responses are passed as `result` when using commands pertaining to flight plans. They look as follows:
```
{
    "id":<flight plan ID, int>,
    "fromICAO":<ICAO of departure airport, str or None>,
    "toICAO":<ICAO of arrival airport, str or None>,
    "fromName":<name of departure airport, str or None>,
    "toName":<name of arrival airport, str or None>,
    "flightNumber":<str or None>,
    "distance":<total distance of the flight plan, float>,
    "maxAltitude":<maximum altitude of the flight plan, int>,
    "waypoints":<number of nodes in flight plan route, int>,
    "likes":<number of times flight plan was liked, int>,
    "downloads":<number of times flight plan was downloaded, int>,
    "popularity":<popularity of the plan, int>,
    "notes":<extra info about flight plan, str>,
    "encodedPolyline":<encoded polyline of the route, str>,
    "createdAt":<creation time stamp, datetime>,
    "updatedAt":<last edited time stamp, datetime>,
    "tags":<flight plan tags, array>,
    "user":{<user associated with flight plan, nested or None>
        "id":<user id, int>,
        "username":<username, str>,
        "gravatarHash":<gravatar hash used for profile pic based on email address, str>,
        "location":<location info of user, str or None>
    },
    "application":{<application linked with the flight plan, nested or None>
        "id":<unique application identifier number, int>,
        "name":<application name, str or None>,
        "url":<application URL, str or None>
    },
    "cycle":{<AIRAC navigation data cycle associated with this plan>
      "id":<cycle id, int>,
      "ident":<AIRAC cycle identifier, str>,
      "year":<last two digits of year in which the cycle was released, int>,
      "release":<subrelease within the year release, int>
    },
    "route":{<route object linked with the flight plan>
        "nodes":[<nodes in the route (2 minimum, though only one is shown), array>
            {
                "type":<node type, see valid types below>,
                "ident":<node navaid identifier, str>,
                "name":<node name, str>,
                "lat":<node latitude, float>,
                "lon":<node latitude, float>,
                "alt":<node altitude, int>,
                "via":{<route to this node from previous node, nested or None. Obviously this could never occur in the first node IRL>
                  "ident":<route to node identifier>,
                    "type":<route to node type, one of [SID, STAR, AWY-HI, AWY-LO, NAT, PACOT]>
                }
            }
        ]
    }
}
```
The valid node types are as follows:
| Type   | Meaning                          |
|:------:|:--------------------------------:|
| UKN    | Unknown                          |
| APT    | Airport                          |
| NDB    | Non-directional beacon (NDB)     |
| VOR    | VHF omni-directional range (VOR) |
| FIX    | Navigational fix                 |
| DME    | Distance measuring equipment     |
| LATLON | Latitude/Longitude point         |

## Commands
### API class
The `API` class has the following commands:
  * `ping()`: This checks the API status to see if it is up. Usage is `flightplandb.API.ping(key)`.
  * `revoke()`: This permanently deactivates the key passed in the revoke request. After running this, a new key must be set by hand in the Flight Plan Database settings, under the section "API Access". Usage is `flightplandb.API.revoke(key)`.

For both `ping()` and `revoke()`, if the request is successful, `result` is `True`; otherwise it raises an `HTTPError`.

### Plan class
The `Plan` class has the following commands:
  * `fetch()`This fetches a flight plan based on its ID. Usage is `flightplandb.Plan.fetch(key, id)`. The `result` returned is the flight plan with fields as shown earlier.
  Optionally, you can do `fetch(key, id, format)` to fetch a flight plan in a specific format, where the format can be one of the following:

  | Format key value |              Flight plan format              |
  |:----------------:|:--------------------------------------------:|
  |     `native`     | JSON (default, autoconverted to Python dict) |
  |       `xml`      |                      XML                     |
  |       `csv`      |                      CSV                     |
  |       `pdf`      |             PDF (very extensive)             |
  |       `kml`      |               Google Maps route              |
  |     `xplane`     |            X-Plane 8, 9, 10 (FMS)            |
  |    `xplane11`    |                  X-Plane 11                  |
  |       `fs9`      |                  FS2004/FS9                  |
  |       `fsx`      |                    FSX XML                   |
  |    `squawkbox`   |                   Squawkbox                  |
  |      `xfmc`      |                     X-FMC                    |
  |      `pmdg`      |                   PMDG rte                   |
  |     `airbusx`    |                   Airbus X                   |
  |  `qualitywings`  |                 QualityWings                 |
  |     `ifly747`    |               iFly 747 (.route)              |
  |   `flightgear`   |          FlightGear (version 2 XML)          |
  |     `tfdi717`    |        TFDi Design 717 (version 1 XML)       |
  | `infiniteflight` |                Infinite Flight               |

  * `post()`: This posts a flight plan which is passed to it as a route object (see `"route":` in the response form earlier). Usage is `flightplandb.Plan.fetch(key, route)`. Returns the same as `fetch()`, so essentially first posts and then fetches the flight plan.
  * `edit()`: This updates a pre-existing flight plan. Usage is `flightplandb.Plan.edit(key, id, route)`. Basically does the same as `post()`, with the same `result` value, but overwrites the flight plan which has the passed id with the new data passed in `route`.
  * `delete()`: This deletes an existing flight plan by ID. Usage is `flightplandb.Plan.delete(key, id)`. If the deletion is successful, then the `result` returned is the same as that for `ping()`.
  * `generate()`: This sends some parameters as a dict to the flight planning engine, which generates a route based on them and sends the route back as in `fetch()`. Usage is `flightplandb.Plan.generate(key, parameters)`. The parameter specification is shown below.

All these commands raise an `HTTPError` on failure.


The parameters for flight plan generation are as follows, where I have added `req` to the required fields and `def` followed by the default value to the nonrequired fields:
```
{
    "fromICAO":<departure ICAO, str, req>,
    "toICAO":<arrival ICAO, str, req>,
    "useNAT":<use NAT tracks in route, bool, def True>,
    "usePACOT":<use PACOT tracks in route, bool, def True>,
    "useAWYLO":<use low-level airways in route, bool, def True>,
    "useAWYHI":<use high-level airways in route, bool, def True>,
    "cruiseAlt":<cruising altitude, int, def 35000>
    "cruiseSpeed":<cruising speed, int, def 420>
    "ascentRate":<ascent rate, int, def 2500>
    "ascentSpeed":<ascent speed, int, def 250>
    "descentRate":<descent rate, int, def 1500>
    "descentSpeed":<descent speed, int, def 250>
}
```
* `decode()`: This sends a string of comma- or space-separated waypoints, beginning and ending with valid airport ICAOs, to the decoder. The decoder then creates a route with that info and sends the route back as in `fetch()`. Usage is `flightplandb.Plan.decode(key, route_string)`. An example `route_string` would be `EHAM SPY VENAS KJFK`.
* `search()`: Searches for flight plans. Results are paginated, and contained in nested dictionaries. Usage is `flightplandb.Plan.search(key, params)`.
The following search parameters are available and will be combined to form a search request. None of the fields are required, but at least one must be provided:
```
{
  "q": <search query, str>,
  "from": <departure airport; ICAO or name, str>,
  "to": <arrival airport; ICAO or name, str>,
  "fromICAO": <departure airport; ICAO only, str>,
  "toICAO": <arrival airport; ICAO only, str>,
  "fromName": <departure airport; name only, str>,
  "toName": <arrival airport; name only, str>,
  "flightNumber":<flight number, str>,
  "distanceMin":<minimum flight distance, int>,
  "distanceMax":<maximum flight distance, int>,
  "tags":<comma separated tag names, str>,
  "includeRoute":<include route for each plan (default False), bool>,
  "page":<number of results to fetch, int>,
  "limit":<number of plans to return per page (max 100), int>,
  "sort":<order of the returned plans (default created), str>
}
```
#### Like class
The `Like` subclass of `Plan` has the following commands:
  * `get()`: This gets the like status of a flight plan, as specified by plan id, passed as an `int`. Returns a `result` of `True` if the plan was liked, `False` if it was not liked or else raises an `HTTPError`. Usage is `flightplandb.Plan.Like.get(key, id)`.
  * `create()`: This adds a like to a flight plan, as specified by plan id, passed as an `int`. Returns a `result` of `True` if the plan was successfully liked, `False` if it was already liked or else raises an `HTTPError`. Usage is `flightplandb.Plan.Like.create(key, id)`.
  * `remove()`: This removes a like from a flight plan, as specified by plan id, passed as an `int`. Returns a `result` of `True` if the plan was successfully unliked, `False` if it was already unliked or else raises an `HTTPError`. Usage is `flightplandb.Plan.Like.remove(key, id)`.

### Nav class
The `Nav` class has the following commands:
  * `NATS()`: This fetches the current North Atlantic Tracks. It takes no parameters. Usage is `flightplandb.Nav.NATS()`.
  Returns a `response` which looks like this:
  ```
  {
      "ident": <track identifier, string>,
      "route": <route object, like that in a flight plan response, with valid FLs eastLevels and westLevels>,
      "validFrom": <timestamp of validity start, datetime>,
      "validTo": <timestamp of validity end, datetime>
  }
  ```
  * `PACOTS()`: This fetches the current Pacific Organized Track System tracks. Usage is `flightplandb.Nav.PACOTS()`.
  Returns a `response` which looks like the `NATS()` response without the flight levels.
  * `search()`: This fetches the current Pacific Organized Track System tracks. Usage is `flightplandb.Nav.search()`.
  Returns a list of navaids, where each navaid looks like this:
  ```
  {
    "ident": <navaid identifier, str>
    "type": <navaid type as in the flight plan response , str>
    "lat": <navaid latitude, float>
    "lon": <navaid longitude, float>
    "name": <navaid name if available, str or None>
    "elevation": <navaid elevation, float>
    "airportICAO": <airport ICAO if available, str or None>
    "runwayIdent": <airport identifier if available, str or None>
  }
  ```

They raise an `HTTPError` on failure.

#### Airport class
The `Airport` subclass of `Nav` has the following commands, both of which raise an `HTTPError` on failure:
  * `weather()`: This gets the weather of an airport, as specified by ICAO code, passed as a string. Usage is `flightplandb.Airport.weather(key, ICAO)`. The `result` returned is as follows:
```
{
    "METAR":<current metar of the airport, str>,
    "TAF":<current taf of the airport, str>
}
```
  * `info()`: This gets the general information about an airport, as specified by ICAO code. The result includes the weather. Usage is `flightplandb.Airport.info(key, ICAO)`. The `result` returned is as shown below.
```
{
  "ICAO": <icao code of the airport, str>,
  "IATA": <iata code of the airport, str or None>,
  "name": <name of the airport, str>,
  "regionName": <name of the geographical region, str or None>,
  "elevation": <airport elevation above sea level, int>,
  "lat": <airport latitude, float>,
  "lon": <airport longitude, float>,
  "magneticVariation": <magnetic deviation at airport, float>,
  "timezone": {<timezone at airport>
    "name": <IANA timezone, str or None>,
    "offset": <offset of timezone from UTC, int or None>
  },
  "times": {<relevant times at airport in UTC>
    "sunrise": <sunrise, datetime>,
    "sunset": <sunset, datetime>,
    "dawn": <dawn, datetime>,
    "dusk": <dusk, datetime>"
  },
  "runwayCount": <number of runways at airport, int>,
  "runways": [<array of all runways. Note each runway will appear twice, once from each end. For this example. though, we only have one runway for simplicity>
    {
      "ident": <name of runway, str>,
      "width": <width of runway, float>,
      "length": <length of runway, float>,
      "bearing": <true heading of runway, float>,
      "surface": <runway surface, str>,
      "thresholdOffset": <distance of threshold from runway end, float>,
      "overrunLength": <runway overrun length, float>,
      "ends": [<array of both ends of the runway>
        {
          "ident": <name of first end, str>,
          "lat": <latitude of first end, int>,
          "lon": <latitude of first end, int>
        },
        {
          "ident": <name of second end, str>,
          "lat": <latitude of second end, int>,
          "lon": <latitude of second end, int>        }
      ],
      "navaids": [<array of navaids associated with runway>
        {
          "ident": <navaid identifier, str>,
          "type": <navaid type, str>,
          "lat": <latitude of navaid, float>,
          "lon": <longitude of navaid, float>,
          "airport": <airport ICAO, str>,
          "runway": <runway heading, float>,
          "frequency": <navaid frequency in Hz, int or None>,
          "slope": <navaid slope in degrees from horizontal, float or None>,
          "bearing": <navaid bearing, float or None>,
          "name": <navaid name, str or None>,
          "elevation": <navaid elevation, int>,
          "range": <navaid range, int>
        }
      ]
    }
  ],
  "frequencies": [<array of voice frequencies associated with the airport>
    {
      "type": <type of frequency eg GND or TWR, str>,
      "frequency": <frequency in Hz, int>,
      "name": <frequency name, str>
    }
  ],
  "weather": {<see weather() documentation for details like types>
    "METAR": <metar>,
    "TAF": <taf>
  }
}
```

### User class
The `User` class has the following commands, which raise an `HTTPError` on failure:
  * `info()`: fetches profile information for any registered user. Usage is `flightplandb.User.info(key, username)`. Returns the following response:
```
{
  "id": <user id, int>,
  "username": <user name, str>,
  "location": <user-provided location, str or None>,
  "gravatarHash": <gravatar hash based on user email, str>,
  "joined": <UTC user registration, datetime>,
  "lastSeen": <UTC user last seen, datetime>,
  "plansCount": <count of flight plans created by user, int>,
  "plansDistance": <total distance of user flight plans, float>,
  "plansDownloads": <download count of user plans, int>,
  "plansLikes": <like count of user plans, int>
}
```
  * `info_me()`: alias for `info()`, where `username` is the current user. Usage is `flightplandb.User.info_me(key)`.
  * `plans()`: fetches flight plans made by a user. Returns an array of flight plan responses as described earlier, leaving out the `route` section in each. Usage is `flightplandb.User.plans(key, username, params)`. The possible options for `params` are described in detail below.
  * `likes()`: fetches a list of the flight plans liked by the user. Usage is `flightplandb.User.likes(key, username, params)`. Like `plans()`, it returns an array of flight plan responses as described earlier, leaving out the `route` section in each.
For both `plans()` and `likes()`, `params` is set to `None` by default. The `params` options are as follows, where all the parameters are optional:
```
{
  "page":<number of results to fetch, int>,
  "limit":<number of plans to return per page (max 100), int>,
  "sort":<order of the returned plans (default created), str>
}
```
  * `search()`: searches for a user by username. `query` is a plain string, containing all or part of a username. Usage is `flightplandb.User.search(key, query)`. Returns a list of possible users like this:
  ```
  {
    "id": <user id, int>,
    "username": <user name, str>,
    "location": <user-provided location, str or None>,
    "gravatarHash": <gravatar hash based on user email, str>
  },
  {
    "id": 8473892,
    "username": "somerandomname",
    "gravatarHash": "802350da209d5a382493cde1594ba059",
    "location": None
  }
  ```
