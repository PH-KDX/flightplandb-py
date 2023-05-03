from unittest import mock

import pytest

import flightplandb
from flightplandb.datatypes import Tag


# localhost is set on every test to allow async loops
@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_tags_api(patched_internal_get):
    json_response = [
        {
            "name": "Decoded",
            "description": "Flight plans decoded",
            "planCount": 7430,
            "popularity": 0.010143822356129395,
        },
        {
            "name": "Generated",
            "description": "Computer generated plans",
            "planCount": 35343,
            "popularity": 0.009036140132228622,
        },
    ]

    correct_response = [
        Tag(
            name="Decoded",
            description="Flight plans decoded",
            planCount=7430,
            popularity=0.010143822356129395,
        ),
        Tag(
            name="Generated",
            description="Computer generated plans",
            planCount=35343,
            popularity=0.009036140132228622,
        ),
    ]

    patched_internal_get.return_value = json_response

    response = await flightplandb.tags.fetch()
    # check that TagsAPI method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="/tags", key=None)
    # check that TagsAPI method decoded data correctly for given response
    assert response == correct_response
