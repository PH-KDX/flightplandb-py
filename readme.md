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
    * [Airport class](#airport-class)
<!-- /TOC -->

##Introduction
This is a Python 3 wrapper for the [flightplandatabase.com](https://www.flightplandatabase.com/) API. Please read the terms of use for this API at [https://flightplandatabase.com/dev/api](https://flightplandatabase.com/dev/api). A large part of this documentation also comes from that website.

This library consists of three classes of commands. They are as follows:
  * API - Commands in this class are meant to make it easier to use the API. They do not serve actual flight resources, but only information linked to the API itself.
  * Plan - All the commands in here have to do with flight planning.
  * Airport - These commands fetch info about airports, rather than flight plans.

Authentication occurs using the HTTPBasicAuth scheme. An API token is passed, referred to in here as `key`, as the username only. No password is used. It is recommended to keep the token outside of your code, using something like `python-dotenv`.

When using this wrapper, `key` needs to be passed as the first argument for every request.

This wrapper does not support changing the units in which the flight plans are returned to anything other than aviation units, and that's not on the to-do list. Feel free to implement it yourself in a branch, however, and push the changed branch back to main.


##Data format
###General
Information is passed to or from the library as nested native Python dicts, lists, etc. This is converted to and from JSON by the library for interaction with the API.

All commands in this wrapper return two variables: `headers`, which is the response headers, and `result`, which is the message response returned by the server. Both consist of native Python structures.

###Header
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

###Flight plan response
Flight plan responses are passed as `result` when using commands pertaining to flight plans. They look as follows:
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

##Commands
###API class
The API class has the following commands:
  * `ping(key)`: This checks the API status to see if it is up. Usage is `flightplandb.API.ping(key)`. If successful, `result` is
```
{
    "message": "OK",
    "errors": None
}
```
  * `revoke(key)`: This permanently deactivates the key passed in the revoke request. After running this, a new key must be set by hand in the FlightPlanDatabase settings, under the section "API Access". If successful, `result` is the same as for `ping()`.

###Plan class
The Plan class has the following commands:
  * `fetch(key, id)`This fetches a flight plan based on its ID. Usage is `flightplandb.Plan.fetch(key, id)`. The `result` returned is the flight plan with fields as shown earlier.
  * `post(key, route)`: This posts a flight plan which is passed to it as a route object (see `"route":` in the response form earlier ). Usage is `flightplandb.Plan.fetch(key, route)`. Returns the same as `fetch()`, so essentially first posts and then fetches the flight plan.
  * `patch(key, id, route)`: This updates a pre-existing flight plan. Usage is `flightplandb.Plan.patch(key, id, route)`. Basically does the same as `post()`, with the same `result` value, but overwrites the flight plan which has the passed id with the new data passed in `route`.
  * `generate(key, params)`: This sends some parameters to the flight planning engine, which generates a route based on them and sends the route back as in `fetch()`. Usage is `flightplandb.Plan.patch(key, id, route)`. The parameter specification is shown below.
  * `delete(key, id)`: This deletes an existing flight plan by ID. If the deletion is successful, then the `result` returned is the same as that for `ping()`.

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

###Airport class
The Airport class has the following commands:
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
  "runways": \[<array of all runways. Note each runway will appear twice, once from each end. For this example. though, we only have one runway for simplicity>
    {
      "ident": <name of runway, str>,
      "width": <width of runway, float>,
      "length": <length of runway, float>,
      "bearing": <true heading of runway, float>,
      "surface": <runway surface, str>,
      "thresholdOffset": <distance of threshold from runway end, float>,
      "overrunLength": <runway overrun length, float>,
      "ends": \[<array of both ends of the runway>
        {
          "ident": <name of first end, str>,
          "lat": <latitude of first end, int>,
          "lon": <latitude of first end, int>
        },
        {
          "ident": <name of second end, str>,
          "lat": <latitude of second end, int>,
          "lon": <latitude of second end, int>        }
      \],
      "navaids": \[<array of navaids associated with runway>
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
      \]
    }
  \],
  "frequencies": \[<array of voice frequencies associated with the airport>
    {
      "type": <type of frequency eg GND or TWR, str>,
      "frequency": <frequency in Hz, int>,
      "name": <frequency name, str>
    }
  \],
  "weather": {<see weather() documentation for details like types>
    "METAR": <metar>,
    "TAF": <taf>
  }
}
```
