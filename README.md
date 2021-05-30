<p align="center">
    <img src="https://raw.githubusercontent.com/PH-KDX/flightplandb-py/feature/artwork/png/240x240.png" alt="FlightPlanDB-py logo">
</p>

# FlightplanDB-py

## Project status
![Unittests and lint](https://github.com/PH-KDX/flightplandb-py/actions/workflows/test_and_lint.yml/badge.svg)
[![PyPi](https://img.shields.io/pypi/v/flightplandb.svg)](https://pypi.org/project/flightplandb/)
![Python](https://img.shields.io/pypi/pyversions/flightplandb.svg)

## Introduction
This is a Python 3 wrapper for the [Flight Plan Database API](https://flightplandatabase.com/dev/api). Flight Plan Database is a website for creating and sharing flight plans for use in flight simulation.

For more information on Flight Plan Database, see their excellent [About page](https://flightplandatabase.com/about).

## API
All the API commands can be called via the `flightplandb.FlightPlanDB` class.
It is organized into subsections as specified in the docs; i.e. `FlightPlanDB.plan` has all the plan API commands.

## Data Types
All datatypes can be found in `flightplandb.datatypes`.

## Exceptions
All exceptions can be found in `flightplandb.exceptions`.

## Documentation
The documentation for this library can be found on readthedocs.io [here](https://flightplandb-py.readthedocs.io/).

## Installation
The library can be installed from PyPi using `pip install flightplandb`;
the installation page link is [here](https://pypi.org/project/flightplandb/). For more details on
installing bleeding-edge versions, see the Installation section of the documentation.
