import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


# base API URL
baseurl = "https://api.flightplandatabase.com"


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
        url = baseurl

        # BasicHTTPAuth with API key passed as username, no password
        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None)
            )

        if result.status_code == 200:
            response = True
        else:
            result.raise_for_status()

        return(result.headers, response)

    # Revokes API key
    @staticmethod
    def revoke(key):
        url = f"{baseurl}/auth/revoke"

        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None)
            )

        # key was successfully revoked
        if result.status_code == 200:
            response = True
        # else raise HTTP error
        else:
            result.raise_for_status()

        return(result.headers, response)


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
        url = f"{baseurl}/plan/{id}"
        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None),
            headers=headers
            )

        # raise exception if HTTP status code is not in 200 range
        result.raise_for_status()

        if format == "json":
            result_dict = result.json()
            try:
                # converts JS timestamps to datetime objects
                result_dict = fptimestamp(result_dict)
            except TypeError:
                pass
            return(result.headers, result_dict)
        else:
            return headers, result.text

    # Takes a dict and posts it to a flight plan
    @staticmethod
    def post(key, route):
        url = f"{baseurl}/plan"

        result = requests.post(
            url,
            json=route,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

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
            url = f"{baseurl}/plan/{id}"

            result = requests.patch(
                url,
                json=route,
                auth=HTTPBasicAuth(key, None)
            )

            result.raise_for_status()

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
            url = f"{baseurl}/plan/{id}"

            result = requests.delete(
                url,
                auth=HTTPBasicAuth(key, None)
                )

            if result.status_code == 200:
                response = True

            result.raise_for_status()

            return(result.headers, response)

    # Creates a new flight plan using the route generator
    @staticmethod
    def generate(key, params):
        url = f"{baseurl}/auto/generate"

        result = requests.post(
            url,
            json=params,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        result_dict = result.json()
        try:
            result_dict = fptimestamp(result_dict)
        except TypeError:
            pass
        return(result.headers, result_dict)

    # Decodes a route from a space-separated string to a flight plan
    @staticmethod
    def decode(key, route):
        url = f"{baseurl}/auto/decode"
        route_dict = {"route": route}
        result = requests.post(
            url,
            json=route_dict,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        result_dict = result.json()
        try:
            result_dict = fptimestamp(result_dict)
        except TypeError:
            pass
        return(result.headers, result_dict)

    # Searches for a route based on several parameters
    @staticmethod
    def search(key, params):
        url = f"{baseurl}/search/plans"

        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        result_dict = result.json()
        print(result_dict)
        try:
            for i in result_dict:
                i = fptimestamp(i)
        except TypeError:
            pass
        return(result.headers, result_dict)

    # Contains everything for working with flight plan likes
    class Like:

        # Gets like status for flight plan
        @staticmethod
        def get(key, id):
            url = f"{baseurl}/{id}/like"

            result = requests.get(
                url,
                auth=HTTPBasicAuth(key, None)
                )

            if result.status_code == 200:
                status = True
            elif result.status_code == 404:
                status = False
            else:
                result.raise_for_status()

            return(result.headers, status)

        # Adds like to flight plan
        @staticmethod
        def create(key, id):
            url = f"{baseurl}/{id}/like"

            result = requests.post(
                url,
                auth=HTTPBasicAuth(key, None)
                )

            if result.status_code == 201:
                status = True
            elif result.status_code == 200:
                status = False
            else:
                result.raise_for_status()

            return(result.headers, status)

        # Removes like from flight plan
        @staticmethod
        def remove(key):
            url = f"{baseurl}/{id}/like"

            result = requests.delete(
                url,
                auth=HTTPBasicAuth(key, None)
                )

            if result.status_code == 200:
                status = True
            elif result.status_code == 404:
                status = False
            else:
                result.raise_for_status()

            return(result.headers, status)


# Contains everything pertaining to navigation
class Nav:

    # NATS
    @staticmethod
    def NATS(key):
        url = f"{baseurl}/nav/NATS"

        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        return(result.headers, result.json())

    # PACOTS
    @staticmethod
    def PACOTS(key):
        url = f"{baseurl}/nav/PACOTS"

        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        return(result.headers, result.json())

    # Search
    @staticmethod
    def search(key, query, types=None):
        params = {"q": query, "types": types}
        url = f"{baseurl}/search/nav"

        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        return(result.headers, result.json())

    # Fetches various info related to airports
    class Airport:

        # Fetches info about airport by ICAO code
        @staticmethod
        def info(key, icao):
            url = f"{baseurl}/nav/airport/{icao}"

            result = requests.get(
                url,
                auth=HTTPBasicAuth(key, None)
                )

            result.raise_for_status()

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
            url = f"{baseurl}/weather/{icao}"
            result = requests.get(url, auth=HTTPBasicAuth(key, None))

            result.raise_for_status()

            return(result.headers, result.json())


# Commands related to registered users
class User:

    # Fetches profile information
    @staticmethod
    def info(key, username):
        url = f"{baseurl}/user/{username}"

        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

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
        url = f"{baseurl}/me/"

        result = requests.get(
            url,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        return(result.headers, result.json())

    # Fetches flight plans by user
    @staticmethod
    def plans(key, username, params=None):
        url = f"{baseurl}/user/{username}/plans"

        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        return(result.headers, result.json())

    # Fetches flight plans liked by user
    @staticmethod
    def likes(key, username, params=None):
        url = f"{baseurl}/user/{username}/likes"

        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        return(result.headers, result.json())

    # Searches for user by username
    @staticmethod
    def search(key, query):
        url = f"{baseurl}/search/users"
        params = {"q": query}

        result = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(key, None)
            )

        result.raise_for_status()

        return(result.headers, result.json())
