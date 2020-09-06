import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


# Small functions used for type conversions etc
# general js to python timestamp
def fromjsiso(timestamp):
    timestamp_formatted = timestamp.replace('Z', '+00:00')
    timestamp_py = datetime.fromisoformat(timestamp_formatted)
    return(timestamp_py)


# converts the same datetime fields in every flight plan response
def fptimestamp(result_dict):
    # convert all the ISO-8601 JS timestamps to Python datetime object
    for i in ["createdAt", "updatedAt"]:
        try:
            result_dict[i] = fromjsiso(
                result_dict[i]
                )
        except KeyError:
            pass
        except ValueError:
            print(f"{i} did not contain a valid timestamp")
            raise
    return(result_dict)


# Actions purely related to the API interaction
class API:

    # Checks API status to see if it is up
    @staticmethod
    def ping(key):
        url = "https://api.flightplandatabase.com/"
        # BasicHTTPAuth with API key passed as username, no password
        result = requests.get(url, auth=HTTPBasicAuth(key, None))
        # the headers and response get passed back as a dict
        return(result.headers, result.json())

    # Revokes API key
    @staticmethod
    def revoke(key):
        url = "https://api.flightplandatabase.com/auth/revoke"
        result = requests.get(url, auth=HTTPBasicAuth(key, None))
        return(result.headers, result.json())


# General actions pertaining to flight plans
class Plan:

    # Fetches a flight plan and its by ID and returns it in specified format
    @staticmethod
    def fetch(key, id, format="json"):
        exports = {
            "json": "application/json",
            "xml": "application/xml",
            "csv": "text/csv",
            "pdf": "application/pdf",
            "kml": "application/vnd.fpd.export.v1.kml+xml",
            "xplane": "application/vnd.fpd.export.v1.xplane",
            "xplane11": "application/vnd.fpd.export.v1.xplane11",
            "fs9": "application/vnd.fpd.export.v1.fs9",
            "fsx": "application/vnd.fpd.export.v1.fsx",
            "squawkbox": "application/vnd.fpd.export.v1.squawkbox",
            "xfmc": "application/vnd.fpd.export.v1.xfmc",
            "pmdg": "application/vnd.fpd.export.v1.pmdg",
            "airbusx": "application/vnd.fpd.export.v1.airbusx",
            "qualitywings": "application/vnd.fpd.export.v1.qualitywings",
            "ifly747": "application/vnd.fpd.export.v1.ifly747",
            "flightgear": "application/vnd.fpd.export.v1.flightgear",
            "tfdi717": "application/vnd.fpd.export.v1.tfdi717",
            "infiniteflight": "application/vnd.fpd.export.v1.infiniteflight"
            }
        if format not in exports:
            raise ValueError(
                "Format must be one of the options specified in the docs"
                )
        headers = {"Accept": str(exports[format.lower()])}
        url = f"https://api.flightplandatabase.com/plan/{id}"
        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None),
            headers=headers
            )
        if format == "json":
            result_dict = result.json()
            try:
                result_dict = fptimestamp(result_dict)
            except TypeError:
                pass
            return(result.headers, result_dict)
        else:
            return headers, result.text

    # Takes a dict and posts it to a flight plan
    @staticmethod
    def post(key, route):
        url = "https://api.flightplandatabase.com/plan"
        result = requests.post(url, json=route, auth=HTTPBasicAuth(key, None))
        result_dict = result.json()
        try:
            result_dict = fptimestamp(result_dict)
        except TypeError:
            pass
        return(result.headers, result_dict)

    # Takes a dict and updates an existing flight plan based on it
    @staticmethod
    def edit(key, id, route):
        if not isinstance(id, int):
            raise ValueError("The flight plan ID must be an integer")
        else:
            url = f"https://api.flightplandatabase.com/plan/{id}"
            result = requests.patch(
                url,
                json=route,
                auth=HTTPBasicAuth(key, None)
            )
            result_dict = result.json()
            try:
                result_dict = fptimestamp(result_dict)
            except TypeError:
                pass
            return(result.headers, result_dict)

    # Deletes a flight plan and its associated route by ID
    @staticmethod
    def delete(key, id):
        if not isinstance(id, int):
            raise ValueError("The flight plan ID must be an integer")
        else:
            url = f"https://api.flightplandatabase.com/plan/{id}"
            result = requests.delete(url, auth=HTTPBasicAuth(key, None))
            return(result.headers, result.json())

    # Creates a new flight plan using the route generator
    @staticmethod
    def generate(key, params):
        url = "https://api.flightplandatabase.com/auto/generate"
        result = requests.post(url, json=params, auth=HTTPBasicAuth(key, None))
        result_dict = result.json()
        try:
            result_dict = fptimestamp(result_dict)
        except TypeError:
            pass
        return(result.headers, result_dict)

    # Decodes a route from a space-separated string to a flight plan
    @staticmethod
    def decode(key, route):
        url = "https://api.flightplandatabase.com/auto/decode"
        route_dict = {"route": route}
        result = requests.post(
            url,
            json=route_dict,
            auth=HTTPBasicAuth(key, None)
            )
        result_dict = result.json()
        try:
            result_dict = fptimestamp(result_dict)
        except TypeError:
            pass
        return(result.headers, result_dict)

    # Searches for a route based on several parameters
    @staticmethod
    def search(key, params):
        url = "https://api.flightplandatabase.com/search/plans"
        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )
        result_dict = result.json()
        print(result_dict)
        try:
            for i in result_dict:
                i = fptimestamp(i)
        except TypeError:
            pass
        return(result.headers, result_dict)


# Contains everything pertaining to navigation
class Nav:

    # NATS
    @staticmethod
    def NATS(key):
        url = "https://api.flightplandatabase.com/nav/NATS"
        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None)
            )
        return(result.headers, result.json())

    # PACOTS
    @staticmethod
    def PACOTS(key):
        url = "https://api.flightplandatabase.com/nav/PACOTS"
        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None)
            )
        return(result.headers, result.json())

    # Search
    @staticmethod
    def search(key, query, types=None):
        params = {"q": query, "types": types}
        url = "https://api.flightplandatabase.com/search/nav"
        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )
        return(result.headers, result.json())

    # Fetches various info related to airports
    class Airport:

        # Fetches info about airport by ICAO code
        @staticmethod
        def info(key, icao):
            url = f"https://api.flightplandatabase.com/nav/airport/{icao}"
            result = requests.get(url, auth=HTTPBasicAuth(key, None))
            result_dict = result.json()
            # convert all the ISO-8601 JS timestamps to Python datetime object
            for i in ["sunrise", "sunset", "dawn", "dusk"]:
                try:
                    result_dict["times"][i] = fromjsiso(
                        result_dict["times"][i]
                        )
                except KeyError:
                    pass
                except ValueError:
                    print(f"[times][{i}] was not a valid timestamp")
                    raise
            return(result.headers, result_dict)

        # Fetches weather for airport by ICAO code
        @staticmethod
        def weather(key, icao):
            url = f"https://api.flightplandatabase.com/weather/{icao}"
            result = requests.get(url, auth=HTTPBasicAuth(key, None))
            return(result.headers, result.json())


# Commands related to registered users
class User:

    # Fetches profile information
    @staticmethod
    def info(key, username):
        url = f"https://api.flightplandatabase.com/user/{username}"
        result = requests.get(url, auth=HTTPBasicAuth(key, None))
        result_dict = result.json()
        # convert all the ISO-8601 JS timestamps to Python datetime object
        for i in ["joined", "lastSeen"]:
            try:
                result_dict[i] = fromjsiso(
                    result_dict[i]
                    )
            except KeyError:
                pass
            except ValueError:
                print(f"[{i}] was not a valid timestamp")
                raise
        return(result.headers, result_dict)

    # An alias for info where username is the current user
    @staticmethod
    def info_me(key):
        url = "https://api.flightplandatabase.com/me/"
        result = requests.get(url, auth=HTTPBasicAuth(key, None))
        return(result.headers, result.json())

    # Fetches flight plans by user
    @staticmethod
    def plans(key, username, params=None):
        url = f"https://api.flightplandatabase.com/user/{username}/plans"
        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )
        return(result.headers, result.json())

    # Fetches flight plans liked by user
    @staticmethod
    def likes(key, username, params=None):
        url = f"https://api.flightplandatabase.com/user/{username}/likes"
        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )
        return(result.headers, result.json())

    # Searches for user by username
    @staticmethod
    def search(key, query):
        url = "https://api.flightplandatabase.com/search/users"
        params = {"q": query}
        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )
        return(result.headers, result.json())
