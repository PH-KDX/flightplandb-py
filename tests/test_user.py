import datetime
from unittest import mock

import pytest
from dateutil.tz import tzutc

import flightplandb
from flightplandb.datatypes import Plan, User, UserSmall


class AsyncIter:
    def __init__(self, items):
        self.items = items

    async def __aiter__(self):
        for item in self.items:
            yield item


# localhost is set on every test to allow async loops
@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_self_info(patched_internal_get):
    json_response = {
        "id": 18990,
        "username": "discordflightplannerbot",
        "location": None,
        "gravatarHash": "3bcb4f39a24700e081f49c3d2d43d277",
        "joined": "2020-08-06T17:04:30.000Z",
        "lastSeen": "2020-12-27T12:40:06.000Z",
        "plansCount": 2,
        "plansDistance": 794.0094160460012,
        "plansDownloads": 0,
        "plansLikes": 0,
    }

    correct_response = User(
        id=18990,
        username="discordflightplannerbot",
        location=None,
        gravatarHash="3bcb4f39a24700e081f49c3d2d43d277",
        joined=datetime.datetime(2020, 8, 6, 17, 4, 30, tzinfo=tzutc()),
        lastSeen=datetime.datetime(2020, 12, 27, 12, 40, 6, tzinfo=tzutc()),
        plansCount=2,
        plansDistance=794.0094160460012,
        plansDownloads=0,
        plansLikes=0,
    )

    patched_internal_get.return_value = json_response

    response = await flightplandb.user.me()
    # check that UserAPI method decoded data correctly for given response
    assert response == correct_response
    # check that UserAPI method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="/me", key=None)


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_user_info(patched_internal_get):
    json_response = {
        "id": 1,
        "username": "lemon",
        "location": "\U0001F601",
        "gravatarHash": "7889b0d4380a7194b6b67c8e2765289d",
        "joined": "2008-12-31T15:49:18.000Z",
        "lastSeen": "2021-04-24T00:22:46.000Z",
        "plansCount": 479,
        "plansDistance": 1212799.2736187153,
        "plansDownloads": 10341,
        "plansLikes": 33,
    }

    correct_response = User(
        id=1,
        username="lemon",
        location="\U0001F601",
        gravatarHash="7889b0d4380a7194b6b67c8e2765289d",
        joined=datetime.datetime(2008, 12, 31, 15, 49, 18, tzinfo=tzutc()),
        lastSeen=datetime.datetime(2021, 4, 24, 0, 22, 46, tzinfo=tzutc()),
        plansCount=479,
        plansDistance=1212799.2736187153,
        plansDownloads=10341,
        plansLikes=33,
    )

    patched_internal_get.return_value = json_response

    response = await flightplandb.user.fetch("lemon")
    # check that UserAPI method decoded data correctly for given response
    assert response == correct_response
    # check that UserAPI method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="/user/lemon", key=None)


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.getiter")
async def test_user_plans(patched_internal_getiter):
    json_response = [
        {
            "id": 62373,
            "fromICAO": "KLAS",
            "toICAO": "KLAX",
            "fromName": "Mc Carran Intl",
            "toName": "Los Angeles Intl",
            "flightNumber": None,
            "distance": 206.39578816273502,
            "maxAltitude": 18000,
            "waypoints": 8,
            "likes": 0,
            "downloads": 1,
            "popularity": 1,
            "notes": "",
            "encodedPolyline": r"aaf{E`|y}T|Ftf@px\\hp e@`nnDd~f@zkmH",
            "createdAt": "2015-08-04T20:48:08.000Z",
            "updatedAt": "2015-08-04T20:48:08.000Z",
            "tags": ["generated"],
            "user": {
                "id": 2429,
                "username": "example",
                "gravatarHash": "f30b58b998a11b5d417cc2c78df3f764",
                "location": None,
            },
        },
        {
            "id": 62493,
            "fromICAO": "EHAM",
            "toICAO": "KJFK",
            "fromName": "Schiphol",
            "toName": "John F Kennedy Intl",
            "flightNumber": None,
            "distance": 3157.88876623323,
            "maxAltitude": 0,
            "waypoints": 2,
            "popularity": 0,
            "notes": None,
            "encodedPolyline": r"yvh~Hgi`\\lggfAjyi~M",
            "createdAt": "2015-08-05T22:44:34.000Z",
            "updatedAt": "2015-08-05T22:44:34.000Z",
            "tags": ["atlantic"],
            "user": {
                "id": 1,
                "username": "example",
                "gravatarHash": "f30b58b998a11b5d417cc2c78df3f764",
                "location": None,
            },
        },
    ]

    correct_response_list = [
        Plan(
            id=62373,
            fromICAO="KLAS",
            toICAO="KLAX",
            fromName="Mc Carran Intl",
            toName="Los Angeles Intl",
            flightNumber=None,
            distance=206.39578816273502,
            maxAltitude=18000,
            waypoints=8,
            likes=0,
            downloads=1,
            popularity=1,
            notes="",
            encodedPolyline=r"aaf{E`|y}T|Ftf@px\\hp e@`nnDd~f@zkmH",
            createdAt="2015-08-04T20:48:08.000Z",
            updatedAt="2015-08-04T20:48:08.000Z",
            tags=["generated"],
            user=User(
                id=2429,
                username="example",
                gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                location=None,
            ),
        ),
        Plan(
            id=62493,
            fromICAO="EHAM",
            toICAO="KJFK",
            fromName="Schiphol",
            toName="John F Kennedy Intl",
            flightNumber=None,
            distance=3157.88876623323,
            maxAltitude=0,
            waypoints=2,
            popularity=0,
            notes=None,
            encodedPolyline=r"yvh~Hgi`\\lggfAjyi~M",
            createdAt="2015-08-05T22:44:34.000Z",
            updatedAt="2015-08-05T22:44:34.000Z",
            tags=["atlantic"],
            user=User(
                id=1,
                username="example",
                gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                location=None,
            ),
        ),
    ]

    correct_calls = [
        mock.call(path="/user/lemon/plans", limit=100, sort="created", key=None)
    ]

    patched_internal_getiter.return_value = AsyncIter(json_response)

    response = flightplandb.user.plans("lemon")
    # check that UserAPI method decoded data correctly for given response
    response_list = []
    async for i in response:
        response_list.append(i)
    assert response_list == correct_response_list
    # check that UserAPI method made correct request of FlightPlanDB
    patched_internal_getiter.assert_has_calls(correct_calls)


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.getiter")
async def test_user_likes(patched_internal_getiter):
    json_response = [
        {
            "id": 62373,
            "fromICAO": "KLAS",
            "toICAO": "KLAX",
            "fromName": "Mc Carran Intl",
            "toName": "Los Angeles Intl",
            "flightNumber": None,
            "distance": 206.39578816273502,
            "maxAltitude": 18000,
            "waypoints": 8,
            "likes": 0,
            "downloads": 1,
            "popularity": 1,
            "notes": "",
            "encodedPolyline": r"aaf{E`|y}T|Ftf@px\\hp e@`nnDd~f@zkmH",
            "createdAt": "2015-08-04T20:48:08.000Z",
            "updatedAt": "2015-08-04T20:48:08.000Z",
            "tags": ["generated"],
            "user": {
                "id": 2429,
                "username": "example",
                "gravatarHash": "f30b58b998a11b5d417cc2c78df3f764",
                "location": None,
            },
        },
        {
            "id": 62493,
            "fromICAO": "EHAM",
            "toICAO": "KJFK",
            "fromName": "Schiphol",
            "toName": "John F Kennedy Intl",
            "flightNumber": None,
            "distance": 3157.88876623323,
            "maxAltitude": 0,
            "waypoints": 2,
            "popularity": 0,
            "notes": None,
            "encodedPolyline": r"yvh~Hgi`\\lggfAjyi~M",
            "createdAt": "2015-08-05T22:44:34.000Z",
            "updatedAt": "2015-08-05T22:44:34.000Z",
            "tags": ["atlantic"],
            "user": {
                "id": 1,
                "username": "example",
                "gravatarHash": "f30b58b998a11b5d417cc2c78df3f764",
                "location": None,
            },
        },
    ]

    correct_response_list = [
        Plan(
            id=62373,
            fromICAO="KLAS",
            toICAO="KLAX",
            fromName="Mc Carran Intl",
            toName="Los Angeles Intl",
            flightNumber=None,
            distance=206.39578816273502,
            maxAltitude=18000,
            waypoints=8,
            likes=0,
            downloads=1,
            popularity=1,
            notes="",
            encodedPolyline=r"aaf{E`|y}T|Ftf@px\\hp e@`nnDd~f@zkmH",
            createdAt="2015-08-04T20:48:08.000Z",
            updatedAt="2015-08-04T20:48:08.000Z",
            tags=["generated"],
            user=User(
                id=2429,
                username="example",
                gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                location=None,
            ),
        ),
        Plan(
            id=62493,
            fromICAO="EHAM",
            toICAO="KJFK",
            fromName="Schiphol",
            toName="John F Kennedy Intl",
            flightNumber=None,
            distance=3157.88876623323,
            maxAltitude=0,
            waypoints=2,
            popularity=0,
            notes=None,
            encodedPolyline=r"yvh~Hgi`\\lggfAjyi~M",
            createdAt="2015-08-05T22:44:34.000Z",
            updatedAt="2015-08-05T22:44:34.000Z",
            tags=["atlantic"],
            user=User(
                id=1,
                username="example",
                gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                location=None,
            ),
        ),
    ]

    correct_calls = [
        mock.call(path="/user/lemon/likes", limit=100, sort="created", key=None)
    ]

    patched_internal_getiter.return_value = AsyncIter(json_response)

    response = flightplandb.user.likes("lemon")
    # check that UserAPI method decoded data correctly for given response
    response_list = []
    async for i in response:
        response_list.append(i)
    assert response_list == correct_response_list
    # check that UserAPI method made correct request of FlightPlanDB
    patched_internal_getiter.assert_has_calls(correct_calls)


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.getiter")
async def test_user_search(patched_internal_getiter):
    json_response = [
        {
            "id": 1,
            "username": "lemon",
            "location": "\U0001F601",
            "gravatarHash": "7889b0d4380a7194b6b67c8e2765289d",
        },
        {
            "id": 1851,
            "username": "lemon2",
            "location": None,
            "gravatarHash": "94ff72a00d4ead8c49abd5a0cf411c6f",
        },
        {
            "id": 1950,
            "username": "lemon6",
            "location": None,
            "gravatarHash": "b807060d00c10513ce04b70918dd07a1",
        },
    ]

    correct_response_list = [
        UserSmall(
            id=1,
            username="lemon",
            location="\U0001F601",
            gravatarHash="7889b0d4380a7194b6b67c8e2765289d",
        ),
        UserSmall(
            id=1851,
            username="lemon2",
            location=None,
            gravatarHash="94ff72a00d4ead8c49abd5a0cf411c6f",
        ),
        UserSmall(
            id=1950,
            username="lemon6",
            location=None,
            gravatarHash="b807060d00c10513ce04b70918dd07a1",
        ),
    ]

    correct_calls = [
        mock.call(path="/search/users", limit=100, params={"q": "lemon"}, key=None)
    ]

    patched_internal_getiter.return_value = AsyncIter(json_response)

    response = flightplandb.user.search("lemon")
    # check that UserAPI method decoded data correctly for given response
    response_list = []
    async for i in response:
        response_list.append(i)
    assert response_list == correct_response_list
    # check that UserAPI method made correct request of FlightPlanDB
    patched_internal_getiter.assert_has_calls(correct_calls)
