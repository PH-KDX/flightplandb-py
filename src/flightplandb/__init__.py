#!/usr/bin/env python3
"""
This is a Python 3 wrapper for the Flight Plan Database API. Flight Plan
Database is a website for creating and sharing flight plans for use in
flight simulation.
For more information on Flight Plan Database, see their excellent About page
at https://flightplandatabase.com/about. For more information about this
library, check out the documentation at https://flightplandb-py.readthedocs.io/
"""


# Version of the flightplandb package
__version__ = "0.5.0"

from . import internal, exceptions, datatypes, submodules

__all__ = ["internal", "exceptions", "datatypes", "submodules"]
