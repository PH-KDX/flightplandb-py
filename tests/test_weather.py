from unittest import mock

import pytest

import flightplandb
from flightplandb.datatypes import Weather


# localhost is set on every test to allow async loops
@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_weather_api(patched_internal_get):
    json_response = {
        "METAR": "EHAM 250755Z 02009KT 330V130 9999\
            BKN033 07/M00 Q1029 NOSIG",
        "TAF": "TAF EHAM 250442Z 2506/2612 02012KT 9999 BKN030 BECMG\
            2507/2510 CAVOK BECMG 2608/2611 05009KT",
    }

    correct_response = Weather(
        METAR="EHAM 250755Z 02009KT 330V130 9999\
            BKN033 07/M00 Q1029 NOSIG",
        TAF="TAF EHAM 250442Z 2506/2612 02012KT 9999 BKN030 BECMG\
            2507/2510 CAVOK BECMG 2608/2611 05009KT",
    )

    patched_internal_get.return_value = json_response

    response = await flightplandb.weather.fetch("EHAM")
    # check that TagsAPI method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="/weather/EHAM", key=None)
    # check that TagsAPI method decoded data correctly for given response
    assert response == correct_response
