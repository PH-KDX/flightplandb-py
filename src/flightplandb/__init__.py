#!/usr/bin/env python3
"""
This is a Python 3 wrapper for the Flight Plan Database API. Flight Plan
Database is a website for creating and sharing flight plans for use in
flight simulation.
For more information on Flight Plan Database, read their excellent About page
at https://flightplandatabase.com/about. For more information about this
library, read the documentation at https://flightplandb-py.readthedocs.io/.
"""


# Version of the flightplandb package
__version__ = "0.8.0"

from . import api, datatypes, exceptions, internal, nav, plan, tags, user, weather

__all__ = [
    "internal",
    "exceptions",
    "datatypes",
    "api",
    "nav",
    "plan",
    "tags",
    "user",
    "weather",
]
