from unittest import mock

import pytest

import flightplandb
from flightplandb.datatypes import StatusResponse


# parametrise this for key and no key, perhaps
# localhost is set on every test to allow async loops
@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get_headers")
async def test_api_header_value(patched_get_headers):
    json_response = {"X-Limit-Cap": "2000", "X-Limit-Used": "150"}

    correct_response = "150"

    patched_get_headers.return_value = json_response

    response = await flightplandb.api.header_value(
        header_key="X-Limit-Used", key="qwertyuiop"
    )
    # check that API method made correct request of FlightPlanDB
    patched_get_headers.assert_awaited_once_with(key="qwertyuiop")
    # check that API method decoded data correctly for given response
    assert response == correct_response


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.api.header_value")
async def test_api_version(patched_header_value):
    header_response = "1"

    correct_response = 1

    patched_header_value.return_value = header_response

    response = await flightplandb.api.version()
    # check that API method made correct request of FlightPlanDB
    patched_header_value.assert_awaited_once_with(header_key="X-API-Version", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.api.header_value")
async def test_api_units(patched_header_value):
    header_response = "AVIATION"

    correct_response = "AVIATION"

    patched_header_value.return_value = header_response

    response = await flightplandb.api.units()
    # check that API method made correct request of FlightPlanDB
    patched_header_value.assert_awaited_once_with(header_key="X-Units", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.api.header_value")
async def test_api_limit_cap(patched_header_value):
    header_response = "100"

    correct_response = 100

    patched_header_value.return_value = header_response

    response = await flightplandb.api.limit_cap()
    # check that API method made correct request of FlightPlanDB
    patched_header_value.assert_awaited_once_with(header_key="X-Limit-Cap", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.api.header_value")
async def test_api_limit_used(patched_header_value):
    header_response = "50"

    correct_response = 50

    patched_header_value.return_value = header_response

    response = await flightplandb.api.limit_used()
    # check that API method made correct request of FlightPlanDB
    patched_header_value.assert_awaited_once_with(header_key="X-Limit-Used", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_api_ping(patched_internal_get):
    json_response = {"message": "OK", "errors": None}

    correct_response = StatusResponse(message="OK", errors=None)

    patched_internal_get.return_value = json_response

    response = await flightplandb.api.ping()
    # check that API method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_key_revoke(patched_internal_get):
    json_response = {"message": "OK", "errors": None}

    correct_response = StatusResponse(message="OK", errors=None)

    patched_internal_get.return_value = json_response

    response = await flightplandb.api.revoke(key="qwertyuiop")
    # check that API method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="/auth/revoke", key="qwertyuiop")
    # check that API method decoded data correctly for given response
    assert response == correct_response
