import dotenv
import os

import flightplandb as fpdb

from dotenv import load_dotenv
load_dotenv("../.env")

APIKEY = os.environ.get("KEY")

api = fpdb.FlightPlanDB(APIKEY)

# FlightPlanDB

# connection
assert api.ping() == fpdb.datatypes.StatusResponse(message='OK', errors=None)
# version
assert api.version == 1
# units
assert api.units in ["AVIATION", "METRIC", "SI"]
# capped limit
assert api.limit_cap == 1500
# requests used so far
assert type(api.limit_used) == int and 0 <= api.limit_used <= api.limit_cap

# PlanAPI


# fetch
