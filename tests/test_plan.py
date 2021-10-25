from unittest import TestCase, main
from unittest.mock import patch, call
import flightplandb
from flightplandb.submodules.plan import PlanAPI
from flightplandb.datatypes import (
    Plan, PlanQuery, User, Route, GenerateQuery,
    RouteNode, Cycle, StatusResponse
)
import datetime
from dateutil.tz import tzutc


def test_plan_fetch(mocker):
    json_response = {
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
            "encodedPolyline": "aaf{E`|y}T|Ftf@px\\hpe@lnCxw "
                "Dbsk@rfx@vhjC`nnDd~f@zkv@nb~ChdmH",
            "createdAt": "2015-08-04T20:48:08.000Z",
            "updatedAt": "2015-08-04T20:48:08.000Z",
            "tags": [
                "generated"
            ],
            "user": {
                "id": 2429,
                "username": "example",
                "gravatarHash": "f30b58b998a11b5d417cc2c78df3f764",
                "location": None
            }
        }

    correct_response = Plan(
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
            encodedPolyline="aaf{E`|y}T|Ftf@px\\hpe@lnCxw "
                "Dbsk@rfx@vhjC`nnDd~f@zkv@nb~ChdmH",
            createdAt="2015-08-04T20:48:08.000Z",
            updatedAt="2015-08-04T20:48:08.000Z",
            tags=[
                "generated"
            ],
            user=User(
                id=2429,
                username="example",
                gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                location=None
            ))

    def patched_get(self, path, return_format, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_get",
        new=patched_get)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_get")

    response = instance.fetch(62373)
    # check that PlanAPI method decoded data correctly for given response
    assert response == correct_response
    # check that PlanAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='/plan/62373', return_format='native', key=None)


def test_plan_create(mocker):
    json_response = {
        "id": None,
        "fromICAO": "EHAM",
        "toICAO": "KJFK",
        "fromName": "Schiphol",
        "toName": "John F Kennedy Intl",
        "route": {
            "nodes": [
                {
                    "ident": "EHAM",
                    "type": "APT",
                    "lat": 52.31485,
                    "lon": 4.75812,
                    "alt": 0,
                    "name": "Schiphol",
                    "via": None
                },
                {
                    "ident": "KJFK",
                    "type": "APT",
                    "lat": 40.63990,
                    "lon": -73.77666,
                    "alt": 0,
                    "name": "John F Kennedy Intl",
                    "via": None
                }
            ]
        }
    }

    correct_response = Plan(
        id=None,
        fromICAO="EHAM",
        toICAO="KJFK",
        fromName="Schiphol",
        toName="John F Kennedy Intl",
        user=None,
        route=Route([
            RouteNode(**{
                "ident": "EHAM",
                "type": "APT",
                "lat": 52.31485,
                "lon": 4.75812,
                "alt": 0,
                "name": "Schiphol",
                "via": None}),
            RouteNode(**{
                "ident": "KJFK",
                "type": "APT",
                "lat": 40.63990,
                "lon": -73.77666,
                "alt": 0,
                "name": "John F Kennedy Intl",
                "via": None})]))
        
    request_data = Plan(
        id=None,
        fromICAO="EHAM",
        toICAO="KJFK",
        fromName="Schiphol",
        toName="John F Kennedy Intl",
        user=None,
        route=Route([
            RouteNode(**{
                "ident": "EHAM",
                "type": "APT",
                "lat": 52.31485,
                "lon": 4.75812,
                "alt": 0,
                "name": "Schiphol",
                "via": None}),
            RouteNode(**{
                "ident": "KJFK",
                "type": "APT",
                "lat": 40.63990,
                "lon": -73.77666,
                "alt": 0,
                "name": "John F Kennedy Intl",
                "via": None})]))
    correct_call = {
        'path':'/plan/',
        'json':{
            'id': None,
            'fromICAO': 'EHAM',
            'toICAO': 'KJFK',
            'fromName': 'Schiphol',
            'toName': 'John F Kennedy Intl',
            'flightNumber': None,
            'distance': None,
            'maxAltitude': None,
            'waypoints': None,
            'likes': None,
            'downloads': None,
            'popularity': None,
            'notes': None,
            'encodedPolyline': None,
            'createdAt': None,
            'updatedAt': None,
            'tags': None,
            'user': None,
            'application': None,
            'route': {
                'nodes': [
                    {'ident': 'EHAM',
                        'type': 'APT',
                        'lat': 52.31485,
                        'lon': 4.75812,
                        'id': None,
                        'alt': 0,
                        'name': 'Schiphol',
                        'via': None},
                    {'ident': 'KJFK',
                        'type': 'APT',
                        'lat': 40.6399,
                        'lon': -73.77666,
                        'id': None,
                        'alt': 0,
                        'name': 'John F Kennedy Intl',
                        'via': None}],
                'eastLevels': None,
                'westLevels': None},
            'cycle': None},
        'return_format':'native',
        'key':None
    }

    def patched_post(self, path, return_format, json, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_post",
        new=patched_post)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_post")

    response = instance.create(request_data)
    # check that PlanAPI method decoded data correctly for given response
    assert response == correct_response
    # check that PlanAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(**correct_call)


def test_plan_delete(mocker):
    json_response = {
        "message": "OK",
        "errors": None
        }

    correct_response = StatusResponse(message="OK", errors=None)

    def patched_delete(self, path, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_delete",
        new=patched_delete)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_delete")

    response = instance.delete(62493)
    # check that TagsAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='/plan/62493', key=None)
    # check that TagsAPI method decoded data correctly for given response
    assert response == correct_response


def test_plan_edit(mocker):
    json_response = {
        "id": 23896,
        "fromICAO": "EHAM",
        "toICAO": "KJFK",
        "fromName": "Schiphol",
        "toName": "John F Kennedy Intl",
        "route": {
            "nodes": [
                {
                    "ident": "EHAM",
                    "type": "APT",
                    "lat": 52.31485,
                    "lon": 4.75812,
                    "alt": 0,
                    "name": "Schiphol",
                    "via": None
                },
                {
                    "ident": "KJFK",
                    "type": "APT",
                    "lat": 40.63990,
                    "lon": -73.77666,
                    "alt": 0,
                    "name": "John F Kennedy Intl",
                    "via": None
                }
            ]
        }
    }

    correct_response = Plan(
        id=23896,
        fromICAO="EHAM",
        toICAO="KJFK",
        fromName="Schiphol",
        toName="John F Kennedy Intl",
        user=None,
        route=Route([
            RouteNode(**{
                "ident": "EHAM",
                "type": "APT",
                "lat": 52.31485,
                "lon": 4.75812,
                "alt": 0,
                "name": "Schiphol",
                "via": None
            }),
            RouteNode(**{
                "ident": "KJFK",
                "type": "APT",
                "lat": 40.63990,
                "lon": -73.77666,
                "alt": 0,
                "name": "John F Kennedy Intl",
                "via": None
            })
        ])
    )
        
    request_data = Plan(
        id=23896,
        fromICAO="EHAM",
        toICAO="KJFK",
        fromName="Schiphol",
        toName="John F Kennedy Intl",
        user=None,
        route=Route([
            RouteNode(**{
                "ident": "EHAM",
                "type": "APT",
                "lat": 52.31485,
                "lon": 4.75812,
                "alt": 0,
                "name": "Schiphol",
                "via": None
            }),
            RouteNode(**{
                "ident": "KJFK",
                "type": "APT",
                "lat": 40.63990,
                "lon": -73.77666,
                "alt": 0,
                "name": "John F Kennedy Intl",
                "via": None
            })
        ])
    )
    correct_call = {
        'path':'/plan/23896',
        'json':{
            'id': 23896,
            'fromICAO': 'EHAM',
            'toICAO': 'KJFK',
            'fromName': 'Schiphol',
            'toName': 'John F Kennedy Intl',
            'flightNumber': None,
            'distance': None,
            'maxAltitude': None,
            'waypoints': None,
            'likes': None,
            'downloads': None,
            'popularity': None,
            'notes': None,
            'encodedPolyline': None,
            'createdAt': None,
            'updatedAt': None,
            'tags': None,
            'user': None,
            'application': None,
            'route': {
                'nodes': [
                    {'ident': 'EHAM',
                        'type': 'APT',
                        'lat': 52.31485,
                        'lon': 4.75812,
                        'id': None,
                        'alt': 0,
                        'name': 'Schiphol',
                        'via': None},
                    {'ident': 'KJFK',
                        'type': 'APT',
                        'lat': 40.6399,
                        'lon': -73.77666,
                        'id': None,
                        'alt': 0,
                        'name': 'John F Kennedy Intl',
                        'via': None}],
                'eastLevels': None,
                'westLevels': None},
            'cycle': None},
        'return_format':'native',
        'key':None
    }

    def patched_patch(self, path, return_format, json, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_patch",
        new=patched_patch)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_patch")

    response = instance.edit(plan=request_data, return_format="native", key=None)
    # check that PlanAPI method decoded data correctly for given response
    assert response == correct_response
    # check that PlanAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(**correct_call)


def test_plan_search(mocker):
    json_response = [
        {
            'application': None,
            'createdAt': '2020-09-30T21:22:37.000Z',
            'cycle': {
                'id': 31,
                'ident': 'FPD2009',
                'release': 9,
                'year': 20},
            'distance': 76.676565810015,
            'downloads': 2,
            'encodedPolyline': 'slg~Haoa\\_fiA{xlAkotC{xcB',
            'flightNumber': None,
            'fromICAO': 'EHAM',
            'fromName': 'Amsterdam Schiphol',
            'id': 3491827,
            'likes': 0,
            'maxAltitude': 9600,
            'notes': 'foo',
            'popularity': 1601846557,
            'tags': ['generated'],
            'toICAO': 'EHAL',
            'toName': 'Ameland',
            'updatedAt': '2020-09-30T21:22:37.000Z',
            'user': None,
            'waypoints': 3},

        {
            'application': None,
            'createdAt': '2018-09-08T12:23:04.000Z',
            'cycle': {
                'id': 5,
                'ident': 'FPD1809',
                'release': 9,
                'year': 18},
            'distance': 76.44654421193701,
            'downloads': 0,
            'encodedPolyline': 'slg~Haoa\\{hlC}|xBolqAytw@',
            'flightNumber': None,
            'fromICAO': 'EHAM',
            'fromName': 'Amsterdam Schiphol Airport',
            'id': 1295630,
            'likes': 0,
            'maxAltitude': 7700,
            'notes': 'foo',
            'popularity': 1536409384,
            'tags': ['generated'],
            'toICAO': 'EHAL',
            'toName': 'Ameland',
            'updatedAt': '2018-09-08T12:23:04.000Z',
            'user': None,
            'waypoints': 3}
    ]

    correct_response_list = [
        Plan(
            id=3491827,
            fromICAO='EHAM',
            toICAO='EHAL',
            fromName='Amsterdam Schiphol',
            toName='Ameland',
            flightNumber=None,
            distance=76.676565810015,
            maxAltitude=9600,
            waypoints=3,
            likes=0,
            downloads=2,
            popularity=1601846557,
            notes='foo',
            encodedPolyline='slg~Haoa\\_fiA{xlAkotC{xcB',
            createdAt=datetime.datetime(2020, 9, 30, 21, 22, 37,
                                        tzinfo=tzutc()),
            updatedAt=datetime.datetime(2020, 9, 30, 21, 22, 37,
                                        tzinfo=tzutc()),
            tags=['generated'], user=None, application=None,
            route=None,
            cycle=Cycle(id=31, ident='FPD2009', year=20, release=9)),

        Plan(
            id=1295630,
            fromICAO='EHAM',
            toICAO='EHAL',
            fromName='Amsterdam Schiphol Airport',
            toName='Ameland',
            flightNumber=None,
            distance=76.44654421193701,
            maxAltitude=7700,
            waypoints=3,
            likes=0,
            downloads=0,
            popularity=1536409384,
            notes='foo',
            encodedPolyline='slg~Haoa\\{hlC}|xBolqAytw@',
            createdAt=datetime.datetime(2018, 9, 8, 12, 23, 4,
                                        tzinfo=tzutc()),
            updatedAt=datetime.datetime(2018, 9, 8, 12, 23, 4,
                                        tzinfo=tzutc()),
            tags=['generated'],
            user=None,
            application=None,
            route=None,
            cycle=Cycle(id=5, ident='FPD1809', year=18, release=9))

    ]
    correct_calls = [mocker.call(
        path='/search/plans',
        sort='created',
        params={
            'q': None,
            'From': None,
            'to': None,
            'fromICAO': 'EHAM',
            'toICAO': 'EHAL',
            'fromName': None,
            'toName': None,
            'flightNumber': None,
            'distanceMin': None,
            'distanceMax': None,
            'tags': None,
            'includeRoute': None
            },
        limit=2,
        key=None)]

    def patched_getiter(self, path, sort="created", params=None, limit=100, key=None):
        return (i for i in json_response)

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_getiter",
        new=patched_getiter)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_getiter")

    response = instance.search(
            PlanQuery(
                fromICAO="EHAM",
                toICAO="EHAL"),
            limit=2)
    # check that PlanAPI method decoded data correctly for given response
    assert list(i for i in response) == correct_response_list
    # check that PlanAPI method made correct request of FlightPlanDB
    spy.assert_has_calls(correct_calls)


def test_plan_like(mocker):
    json_response = {
        "message": "Not Found",
        "errors": None
        }

    correct_response = StatusResponse(message='Not Found', errors=None)

    def patched_post(self, path, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_post",
        new=patched_post)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_post")

    response = instance.like(42)
    # check that TagsAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='/plan/42/like', key=None)
    # check that TagsAPI method decoded data correctly for given response
    assert response == correct_response


def test_plan_unlike(mocker):
    json_response = {
        "message": "OK",
        "errors": None
        }

    correct_response = True

    def patched_delete(self, path, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_delete",
        new=patched_delete)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_delete")

    response = instance.unlike(42)
    # check that TagsAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='/plan/42/like', key=None)
    # check that TagsAPI method decoded data correctly for given response
    assert response == correct_response


def test_plan_has_liked(mocker):
    json_response = {
        "message": "OK",
        "errors": None
        }

    correct_response = True

    def patched_get(self, path, ignore_statuses=None, key=None):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_get",
        new=patched_get)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_get")

    response = instance.has_liked(42)
    # check that TagsAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='/plan/42/like', ignore_statuses=[404], key=None)
    # check that TagsAPI method decoded data correctly for given response
    assert response == correct_response


def test_plan_generate(mocker):
    json_response = {
        'application': None,
        'createdAt': '2021-04-28T19:55:45.000Z',
        'cycle': {
            'id': 38,
            'ident': 'FPD2104',
            'release': 4,
            'year': 21},
        'distance': 36.666306664518004,
        'downloads': 0,
        'encodedPolyline': '_dgeIybta@niaA~vdD',
        'flightNumber': None,
        'fromICAO': 'EHAL',
        'fromName': 'Ameland',
        'id': 4179148,
        'likes': 0,
        'maxAltitude': 0,
        'notes': 'Basic altitude profile:\n'
                    '- Ascent Rate: 2500ft/min\n'
                    '- Ascent Speed: 250kts\n'
                    '- Cruise Altitude: 35000ft\n'
                    '- Cruise Speed: 420kts\n'
                    '- Descent Rate: 1500ft/min\n'
                    '- Descent Speed: 250kts\n'
                    '\n'
                    'Options:\n'
                    '- Use NATs: yes\n'
                    '- Use PACOTS: yes\n'
                    '- Use low airways: yes\n'
                    '- Use high airways: yes\n',
        'popularity': 1619639745,
        'tags': ['generated'],
        'toICAO': 'EHTX',
        'toName': 'Texel',
        'updatedAt': '2021-04-28T19:55:45.000Z',
        'user': {
            'gravatarHash': '3bcb4f39a24700e081f49c3d2d43d277',
            'id': 18990,
            'location': None,
            'username': 'discordflightplannerbot'},
        'waypoints': 2
    }

    request_data = GenerateQuery(
        fromICAO="EHAL",
        toICAO="EHTX"
    )

    correct_response = Plan(
        id=4179148,
        fromICAO='EHAL',
        toICAO='EHTX',
        fromName='Ameland',
        toName='Texel',
        flightNumber=None,
        distance=36.666306664518004,
        maxAltitude=0,
        waypoints=2,
        likes=0,
        downloads=0,
        popularity=1619639745,
        notes='Basic altitude profile:\n'
        '- Ascent Rate: 2500ft/min\n'
        '- Ascent Speed: 250kts\n'
        '- Cruise Altitude: 35000ft\n'
        '- Cruise Speed: 420kts\n'
        '- Descent Rate: 1500ft/min\n'
        '- Descent Speed: 250kts\n\nOptions:\n'
        '- Use NATs: yes\n'
        '- Use PACOTS: yes\n'
        '- Use low airways: yes\n'
        '- Use high airways: yes\n',
        encodedPolyline='_dgeIybta@niaA~vdD',
        createdAt=datetime.datetime(
            2021, 4, 28, 19, 55, 45, tzinfo=tzutc()),
        updatedAt=datetime.datetime(
            2021, 4, 28, 19, 55, 45, tzinfo=tzutc()),
        tags=['generated'],
        user=User(
            id=18990,
            username='discordflightplannerbot',
            location=None,
            gravatarHash='3bcb4f39a24700e081f49c3d2d43d277',
            joined=None,
            lastSeen=None,
            plansCount=0,
            plansDistance=0.0,
            plansDownloads=0,
            plansLikes=0),
        application=None,
        route=None,
        cycle=Cycle(
            id=38,
            ident='FPD2104',
            year=21,
            release=4)
    )

    correct_call = {
        "path":'/auto/generate',
        "json":{
            'fromICAO': 'EHAL',
            'toICAO': 'EHTX',
            'useNAT': True,
            'usePACOT': True,
            'useAWYLO': True,
            'useAWYHI': True,
            'cruiseAlt': 35000,
            'cruiseSpeed': 420,
            'ascentRate': 2500,
            'ascentSpeed': 250,
            'descentRate': 1500,
            'descentSpeed': 250
        },
        "return_format":"native",
        "key":None
    }

    def patched_post(self, path, return_format, json, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_post",
        new=patched_post)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_post")

    response = instance.generate(request_data)
    # check that PlanAPI method decoded data correctly for given response
    assert response == correct_response
    # check that PlanAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(**correct_call)


def test_plan_decode(mocker):
    json_response = {
        "id":4708699,
        "fromICAO":"KSAN",
        "toICAO":"KDEN",
        "fromName":"San Diego Intl",
        "toName":"Denver Intl",
        "flightNumber":None,
        "distance":757.3434118878,
        "maxAltitude":0,
        "waypoints":5,
        "likes":0,
        "downloads":0,
        "popularity":1635191202,
        "notes":"Requested: KSAN BROWS TRM LRAIN KDEN",
        "encodedPolyline":"_hxfEntgjUr_S_`qAgvaEocvBsksPgn_a@_~kSwgbc@",
        "createdAt":"2021-10-25T19:46:42.000Z",
        "updatedAt":"2021-10-25T19:46:42.000Z",
        "tags":["decoded"],
        'user': {
            'gravatarHash': '3bcb4f39a24700e081f49c3d2d43d277',
            'id': 18990,
            'location': None,
            'username': 'discordflightplannerbot'},
        "application":None,
        "cycle":{
            "id":40,
            "ident":"FPD2106",
            "year":21,
            "release":6
            }
        }

    request_data = {"KSAN BROWS TRM LRAIN KDEN"}

    correct_response = Plan(
        id=4708699,
        fromICAO='KSAN',
        toICAO='KDEN',
        fromName='San Diego Intl',
        toName='Denver Intl',
        flightNumber=None,
        distance=757.3434118878,
        maxAltitude=0,
        waypoints=5,
        likes=0,
        downloads=0,
        popularity=1635191202,
        notes='Requested: KSAN BROWS TRM LRAIN KDEN',
        encodedPolyline='_hxfEntgjUr_S_`qAgvaEocvBsksPgn_a@_~kSwgbc@',
        createdAt=datetime.datetime(
            2021, 10, 25, 19, 46, 42,
            tzinfo=tzutc()
            ),
        updatedAt=datetime.datetime(
            2021, 10, 25, 19, 46, 42,
            tzinfo=tzutc()
            ),
        tags=['decoded'],
        user=User(
            id=18990,
            username='discordflightplannerbot',
            location=None,
            gravatarHash='3bcb4f39a24700e081f49c3d2d43d277',
            joined=None,
            lastSeen=None,
            plansCount=0,
            plansDistance=0.0,
            plansDownloads=0,
            plansLikes=0),
            application=None,
            route=None,
            cycle=Cycle(
                id=40,
                ident='FPD2106',
                year=21,
                release=6
                )
            )

    correct_call = {
        "path":'/auto/decode',
        "json":{
            'route': {
                'KSAN BROWS TRM LRAIN KDEN'
                }
        },
        "key":None
    }

    def patched_post(self, path, json, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.plan.PlanAPI,
        attribute="_post",
        new=patched_post)
    instance = flightplandb.submodules.plan.PlanAPI()
    spy = mocker.spy(instance, "_post")

    response = instance.decode(request_data)
    # check that PlanAPI method decoded data correctly for given response
    assert response == correct_response
    # check that PlanAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(**correct_call)
