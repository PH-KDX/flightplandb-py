import requests
from requests.auth import HTTPBasicAuth


class API:

    # Checks API status to see if it is up
    @staticmethod
    def ping(key):
        url = "https://api.flightplandatabase.com/"
        # BasicHTTPAuth with API key passed as username, no password
        result = requests.get(url, auth=HTTPBasicAuth(key, None))
        # the headers get passed back as a dict
        # the reponse gets passed back as JSON
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
