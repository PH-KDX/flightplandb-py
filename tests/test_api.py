import flightplandb
from flightplandb.datatypes import StatusResponse


# parametrise this for key and no key, perhaps
def test_api_header_value(mocker):
    json_response = {
        "X-Limit-Cap": "2000",
        "X-Limit-Used": "150"
        }

    correct_response = "150"

    def patched_get_headers(key):
        return json_response

    mocker.patch(
        target="flightplandb.internal.get_headers",
        new=patched_get_headers)

    spy = mocker.spy(flightplandb.internal, "get_headers")

    response = flightplandb.api.header_value(
        header_key="X-Limit-Used",
        key="qwertyuiop"
        )
    # check that API method made correct request of FlightPlanDB
    spy.assert_called_once_with(
        key="qwertyuiop"
        )
    # check that API method decoded data correctly for given response
    assert response == correct_response


def test_api_version(mocker):
    header_response = "1"

    correct_response = 1

    def patched_get(header_key, key):
        return header_response

    mocker.patch(
        target="flightplandb.api.header_value",
        new=patched_get)
    
    spy = mocker.spy(flightplandb.api, "header_value")

    response = flightplandb.api.version()
    # check that API method made correct request of FlightPlanDB
    spy.assert_called_once_with(header_key="X-API-Version", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


def test_api_units(mocker):
    header_response = "AVIATION"

    correct_response = "AVIATION"

    def patched_get(header_key, key):
        return header_response

    mocker.patch(
        target="flightplandb.api.header_value",
        new=patched_get)
    
    spy = mocker.spy(flightplandb.api, "header_value")

    response = flightplandb.api.units()
    # check that API method made correct request of FlightPlanDB
    spy.assert_called_once_with(header_key="X-Units", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


def test_api_limit_cap(mocker):
    header_response = "100"

    correct_response = 100

    def patched_get(header_key, key):
        return header_response

    mocker.patch(
        target="flightplandb.api.header_value",
        new=patched_get)
    
    spy = mocker.spy(flightplandb.api, "header_value")

    response = flightplandb.api.limit_cap()
    # check that API method made correct request of FlightPlanDB
    spy.assert_called_once_with(header_key="X-Limit-Cap", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


def test_api_limit_used(mocker):
    header_response = "50"

    correct_response = 50

    def patched_get(header_key, key):
        return header_response

    mocker.patch(
        target="flightplandb.api.header_value",
        new=patched_get)
    
    spy = mocker.spy(flightplandb.api, "header_value")

    response = flightplandb.api.limit_used()
    # check that API method made correct request of FlightPlanDB
    spy.assert_called_once_with(header_key="X-Limit-Used", key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


def test_api_ping(mocker):
    json_response = {
        "message": "OK",
        "errors": None
        }

    correct_response = StatusResponse(message="OK", errors=None)

    def patched_get(path, key):
        return json_response

    mocker.patch(
        target="flightplandb.internal.get",
        new=patched_get)
    
    spy = mocker.spy(flightplandb.internal, "get")

    response = flightplandb.api.ping()
    # check that API method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='', key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response


def test_key_revoke(mocker):
    json_response = {
        "message": "OK",
        "errors": None
        }

    correct_response = StatusResponse(message="OK", errors=None)

    def patched_get(path, key):
        return json_response

    mocker.patch(
        target="flightplandb.internal.get",
        new=patched_get)
    
    spy = mocker.spy(flightplandb.internal, "get")

    response = flightplandb.api.revoke(key="qwertyuiop")
    # check that API method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='/auth/revoke', key="qwertyuiop")
    # check that API method decoded data correctly for given response
    assert response == correct_response
