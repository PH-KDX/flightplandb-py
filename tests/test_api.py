import flightplandb
from flightplandb.datatypes import StatusResponse, Weather
import pytest


@pytest.mark.parametrize(
    "header_key,ping_headers,existing_headers,correct_response,correct_mock_calls",
    [
        ("X-API-Version", {"X-API-Version": 1}, {"X-API-Version": 1}, 1, None),
        ("X-API-Version", {"X-API-Version": 1}, {}, 1, {"key": None}),
        ("X-Units", {"X-Units": "AVIATION"}, {"X-Units": "AVIATION"}, "AVIATION", None),
        ("X-Units", {"X-Units": "AVIATION"}, {}, "AVIATION", {"key": None}),
        ("X-Limit-Cap", {"X-Limit-Cap": 100}, {"X-Limit-Cap": 100}, 100, None),
        ("X-Limit-Cap", {"X-Limit-Cap": 100}, {}, 100, {"key": None}),
        ("X-Limit-Used", {"X-Limit-Used": 1}, {"X-Limit-Used": 1}, 1, None),
        ("X-Limit-Used", {"X-Limit-Used": 1}, {}, 1, {"key": None}),
    ],
)
def test_api_headers(header_key, mocker, ping_headers, existing_headers, correct_response, correct_mock_calls):

    def patched_ping(self, key):
        self._header = ping_headers

    mocker.patch.object(
        target=flightplandb.submodules.api.API,
        attribute="ping",
        new=patched_ping)
    instance = flightplandb.submodules.api.API()
    spy = mocker.spy(instance, "ping")

    instance._header = existing_headers

    response = instance._header_value(header_key=header_key, key=None)
    if correct_mock_calls == None:
        spy.assert_not_called()
    else:
        spy.assert_called_once_with(**correct_mock_calls)
    assert(response==correct_response)


def test_api_ping(mocker):
    json_response = {
        "message": "OK",
        "errors": None
        }

    correct_response = StatusResponse(message="OK", errors=None)

    def patched_get(self, path, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.api.API,
        attribute="_get",
        new=patched_get
        )
    instance = flightplandb.submodules.api.API()
    spy = mocker.spy(instance, "_get")

    response = instance.ping()
    # check that API method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='', key=None)
    # check that API method decoded data correctly for given response
    assert response == correct_response