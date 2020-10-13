#!/usr/bin/env bash
set -euo pipefail

# Run pip install ".[dev]" to get all
# get all the development dependencies
flake8 src/
mypy src/FlightPlanDB
