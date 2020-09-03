import requests
from requests.auth import HTTPBasicAuth


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

    # Fetches a flight plan and its associated route by ID
    @staticmethod
    def fetch(key, id):
        if not isinstance(id, int):
            raise ValueError("The flight plan ID must be an integer")
        else:
            url = f"https://api.flightplandatabase.com/plan/{id}"
            result = requests.get(url, auth=HTTPBasicAuth(key, None))
            return(result.headers, result.json())

    # Takes a dict and posts it to a flight plan
    @staticmethod
    def post(key, route):
        url = "https://api.flightplandatabase.com/plan"
        result = requests.post(url, json=route, auth=HTTPBasicAuth(key, None))
        return(result.headers, result.json())

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
            return(result.headers, result.json())

    # Deletes a flight plan and its associated route by ID
    @staticmethod
    def delete(key, id):
        if not isinstance(id, int):
            raise ValueError("The flight plan ID must be an integer")
        else:
            url = f"https://api.flightplandatabase.com/plan/{id}"
            result = requests.delete(url, auth=HTTPBasicAuth(key, None))
            return(result.headers, result.json())


    """Creates a Flight Plan and Returns The Plan in Specific Format"""
    @staticmethod
    def formattedFetch(key, route, format="json"):
        jsonPlan = Plan.generate(key, route)
        id = jsonPlan[1]['id']
        exports = {"xplane" : "application/vnd.fpd.export.v1.xplane", "xplane11" : "application/vnd.fpd.export.v1.xplane11", "fsx" : "application/vnd.fpd.export.v1.fsx",
                   "fs9" : "application/vnd.fpd.export.v1.fs9", "squawkbox" : "application/vnd.fpd.export.v1.squawkbox", "xfmc" : "application/vnd.fpd.export.v1.xfmc",
                   "pmdg" : "application/vnd.fpd.export.v1.pmdg", "pdf" : "application/pdf", "kml" : "application/vnd.fpd.export.v1.kml+xml",
                   "json" : "application/vnd.fpd.export.v1.json+json", "airbusx" : "application/vnd.fpd.export.v1.airbusx", "qualitywings" : "application/vnd.fpd.export.v1.qualitywings",
                   "ifly747" : "application/vnd.fpd.export.v1.ifly747", "flightgear" : "application/vnd.fpd.export.v1.flightgear", "tfdi717" : "application/vnd.fpd.export.v1.tfdi717"}
        headers = {"Accept" : str(exports[format.lower()])}
        url = f"https://api.flightplandatabase.com/plan/{id}"
        result = requests.get(url, auth=HTTPBasicAuth(key, None), headers=headers)
        return result.text
      
    # Creates a new flight plan using the route generator
    @staticmethod
    def generate(key, params):
        url = "https://api.flightplandatabase.com/auto/generate"
        result = requests.post(url, json=params, auth=HTTPBasicAuth(key, None))
        return(result.headers, result.json())

    # Converts a route from a space-separated string to a flight plan
    @staticmethod
    def decode(key, route):
        url = "https://api.flightplandatabase.com/auto/decode"
        route_dict = {"route": route}
        result = requests.post(
            url,
            json=route_dict,
            auth=HTTPBasicAuth(key, None)
            )
        return(result.headers, result.json())

    # Searches for a route based on several parameters
    @staticmethod
    def search(key, params):
        url = "https://api.flightplandatabase.com/search/plans"
        result = requests.post(url, json=params, auth=HTTPBasicAuth(key, None))
        return(result.headers, result.json())

    # Everything to do with flightplan likes
    class Like:

        # Fetches your like status for a flight plan.
        @staticmethod
        def get(id):
            url = "https://api.flightplandatabase.com/search/plans"


# Contains everything pertaining to navigation
#class Nav:

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
            return(result.headers, result.json())

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
        return(result.headers, result.json())

    # An alias for info where username is the current user
    @staticmethod
    def info_me(key):
        url = "https://api.flightplandatabase.com/me/"
        result = requests.get(url, auth=HTTPBasicAuth(key, None))
        return(result.headers, result.json())

    # Fetches profile information
    @staticmethod
    def plans(key, username):
        url = f"https://api.flightplandatabase.com/user/{username}/plans"
        result = requests.get(url, auth=HTTPBasicAuth(key, None))
        return(result.headers, result.json())

    # Fetches profile information
    @staticmethod
    def likes(key, username):
        url = f"https://api.flightplandatabase.com/user/{username}/likes"
        result = requests.get(url, auth=HTTPBasicAuth(key, None))
        return(result.headers, result.json())

    # Fetches profile information
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
