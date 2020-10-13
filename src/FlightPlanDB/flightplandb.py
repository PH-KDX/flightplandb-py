#!/usr/bin/env python

from functools import partial
from typing import List
from dataclasses import asdict

import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from urllib.parse import urljoin

from FlightPlanDB.response_types import (
    StatusResponse, PlanQuery, Plan)


class FlightPlanDB:
    def __init__(
            self, key: str,
            base_url: str = "https://api.flightplandatabase.com"):
        """
        To get an API key, visit your account settings page.
        Your account will need a verified email address to add an API key.
        https://flightplandatabase.com/settings

        Args:
            key (str): api token
        """
        self.key: str = key
        self._header: CaseInsensitiveDict[str] = CaseInsensitiveDict()
        self.base_url = base_url

    def __call__(self, method: str, path, *args, **kwargs):
        resp = requests.request(
            method,
            urljoin(self.base_url, path),
            auth=HTTPBasicAuth(self.key, None),
            *args, **kwargs)
        self._header = resp.headers
        return resp.json()

    def __getattr__(self, attr):
        """
        The api only supports the following http verbs
        """
        if attr not in ["get", "post", "patch", "delete"]:
            raise AttributeError(
                f"'{self.__class__.__name__}' has no attribute '{attr}'")

        return partial(self, attr)

    def _header_value(self, header_key):
        if header_key not in self._header:
            self.ping()  # Make atleast one request
        return self._header[header_key]

    @property
    def api_version(self) -> int:
        """
        Returns:
            int: API version that returned the response
        """
        return int(self._header_value("X-API-Version"))

    @property
    def units(self) -> str:
        """The units system used for numeric values.
        https://flightplandatabase.com/dev/api#units

        Returns:
            String: AVIATION, METRIC or SI
        """
        return self._header_value("X-Units")

    @property
    def limit_cap(self) -> int:
        """
        The number of requests allowed per day, operated on an hourly rolling
        basis. i.e Requests used between 19:00 and 20:00 will become available
        again at 19:00 the following day. API key authenticated requests get a
        higher daily rate limit and can be raised if a compelling
        use case is presented.
        Returns:
            int: number of allowed requests per day
        """
        return int(self._header_value("X-Limit-Cap"))

    @property
    def limit_used(self) -> int:
        """
        The number of requests used in the current period
        by the presented API key or IP address

        Returns:
            int: number of requests used in period
        """
        return int(self._header_value("X-Limit-Used"))

    def ping(self) -> StatusResponse:
        """Checks API status to see if it is up"""
        resp = self.get("")
        return StatusResponse(**resp)

    def revoke(self) -> StatusResponse:
        """
        Revoke the API key in use in the vent it is compromised.

        If the HTTP response code is 200 and the status message is "OK", then
        the key has been revoked and any further requests will be rejected.
        Any other status code or message indicates an error
        has occurred and the errors array will give further details.
        """
        resp = self.get("/auth/revoke")
        self._header = resp.headers
        return StatusResponse(**resp.json())

    def plan(self, id: int) -> Plan:
        """
        Fetches a flight plan and its by ID and returns it in specified format
        """
        return Plan(**self.get(f"/plan/{id}"))

    def new_plan(self, plan: Plan) -> Plan:
        return Plan(**self.post("/plan", json=asdict(plan)))

    def edit_plan(self, plan: Plan) -> Plan:
        return Plan(**self.patch(f"/plan/{plan.id}", json=asdict(plan)))

    def delete_plan(self, id: int) -> StatusResponse:
        return StatusResponse(**self.delete("/plan/{id}"))

    def search(self, plan_query: PlanQuery) -> List[Plan]:
        return list(
            map(
                lambda p: Plan(**p),
                self.get("/search/plans", params=plan_query.as_dict())))

#     def generate(key, params):

#         url = f"{baseurl}/auto/generate"

#         result = requests.post(
#             url,
#             json=params,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         result_dict = result.json()
#         try:
#             result_dict = fptimestamp(result_dict)
#         except TypeError:
#             pass
#         return(result.headers, result_dict)

#     # Decodes a route from a space-separated string to a flight plan
#     @staticmethod
#     def decode(key, route):
#         url = f"{baseurl}/auto/decode"
#         route_dict = {"route": route}
#         result = requests.post(
#             url,
#             json=route_dict,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         result_dict = result.json()
#         try:
#             result_dict = fptimestamp(result_dict)
#         except TypeError:
#             pass
#         return(result.headers, result_dict)

#     # Searches for a route based on several parameters
#     @staticmethod
#     # Contains everything for working with flight plan likes
#     class Like:

#         # Gets like status for flight plan
#         @staticmethod
#         def get(key, id):
#             url = f"{baseurl}/{id}/like"

#             result = requests.get(
#                 url,
#                 auth=HTTPBasicAuth(key, None)
#                 )

#             if result.status_code == 200:
#                 status = True
#             elif result.status_code == 404:
#                 status = False
#             else:
#                 result.raise_for_status()

#             return(result.headers, status)

#         # Adds like to flight plan
#         @staticmethod
#         def create(key, id):
#             url = f"{baseurl}/{id}/like"

#             result = requests.post(
#                 url,
#                 auth=HTTPBasicAuth(key, None)
#                 )

#             if result.status_code == 201:
#                 status = True
#             elif result.status_code == 200:
#                 status = False
#             else:
#                 result.raise_for_status()

#             return(result.headers, status)

#         # Removes like from flight plan
#         @staticmethod
#         def remove(key):
#             url = f"{baseurl}/{id}/like"

#             result = requests.delete(
#                 url,
#                 auth=HTTPBasicAuth(key, None)
#                 )

#             if result.status_code == 200:
#                 status = True
#             elif result.status_code == 404:
#                 status = False
#             else:
#                 result.raise_for_status()

#             return(result.headers, status)


# # Contains everything pertaining to navigation
# class Nav:

#     # NATS
#     @staticmethod
#     def NATS(key):
#         url = f"{baseurl}/nav/NATS"

#         result = requests.get(
#             url,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         return(result.headers, result.json())

#     # PACOTS
#     @staticmethod
#     def PACOTS(key):
#         url = f"{baseurl}/nav/PACOTS"

#         result = requests.get(
#             url,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         return(result.headers, result.json())

#     # Search
#     @staticmethod
#     def search(key, query, types=None):
#         params = {"q": query, "types": types}
#         url = f"{baseurl}/search/nav"

#         result = requests.get(
#             url,
#             params=params,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         return(result.headers, result.json())

#     # Fetches various info related to airports
#     class Airport:

#         # Fetches info about airport by ICAO code
#         @staticmethod
#         def info(key, icao):
#             url = f"{baseurl}/nav/airport/{icao}"

#             result = requests.get(
#                 url,
#                 auth=HTTPBasicAuth(key, None)
#                 )

#             result.raise_for_status()

#             result_dict = result.json()
#             # convert all the ISO-8601 JS
#             # timestamps to Python datetime object
#             for i in ["sunrise", "sunset", "dawn", "dusk"]:
#                 try:
#                     result_dict["times"][i] = fromjsiso(
#                         result_dict["times"][i]
#                         )
#                 except KeyError:
#                     pass
#                 except ValueError:
#                     print(f"[times][{i}] was not a valid timestamp")
#                     raise
#             return(result.headers, result_dict)

#         # Fetches weather for airport by ICAO code
#         @staticmethod
#         def weather(key, icao):
#             url = f"{baseurl}/weather/{icao}"
#             result = requests.get(url, auth=HTTPBasicAuth(key, None))

#             result.raise_for_status()

#             return(result.headers, result.json())


# # Commands related to registered users
# class User:

#     # Fetches profile information
#     @staticmethod
#     def info(key, username):
#         url = f"{baseurl}/user/{username}"

#         result = requests.get(
#             url,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         result_dict = result.json()
#         # convert all the ISO-8601 JS timestamps to Python datetime object
#         for i in ["joined", "lastSeen"]:
#             try:
#                 result_dict[i] = fromjsiso(
#                     result_dict[i]
#                     )
#             except KeyError:
#                 pass
#             except ValueError:
#                 print(f"[{i}] was not a valid timestamp")
#                 raise
#         return(result.headers, result_dict)

#     # An alias for info where username is the current user
#     @staticmethod
#     def info_me(key):
#         url = f"{baseurl}/me/"

#         result = requests.get(
#             url,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         return(result.headers, result.json())

#     # Fetches flight plans by user
#     @staticmethod
#     def plans(key, username, params=None):
#         url = f"{baseurl}/user/{username}/plans"

#         result = requests.get(
#             url,
#             params=params,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         return(result.headers, result.json())

#     # Fetches flight plans liked by user
#     @staticmethod
#     def likes(key, username, params=None):
#         url = f"{baseurl}/user/{username}/likes"

#         result = requests.get(
#             url,
#             params=params,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         return(result.headers, result.json())

#     # Searches for user by username
#     @staticmethod
#     def search(key, query):
#         url = f"{baseurl}/search/users"
#         params = {"q": query}

#         result = requests.get(
#             url,
#             params=params,
#             auth=HTTPBasicAuth(key, None)
#             )

#         result.raise_for_status()

#         return(result.headers, result.json())


def test_run():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    token = os.environ["FLIGHT_TOKEN"]
    api = FlightPlanDB(token)

    print(api.ping())
    print(api.limit_used)

    plan_id = 98
    plan = api.plan(plan_id)
    plan_dict = asdict(plan)
    print(plan_dict)

    # print(api.get())
