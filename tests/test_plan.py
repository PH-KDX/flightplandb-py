from unittest import TestCase, main
from unittest.mock import patch, call
from flightplandb.submodules.plan import PlanAPI
from flightplandb.datatypes import (
    Plan, PlanQuery, User, Route, GenerateQuery,
    RouteNode, Cycle, StatusResponse
)
import datetime
from dateutil.tz import tzutc


class PlanTest(TestCase):
    def test_plan_fetch(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._get.return_value = {
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
                "encodedPolyline": r"aaf{E`|y}T|Ftf@px\\hpe@lnCxw \
                Dbsk@rfx@vhjC`nnDd~f@zkv@nb~ChdmH",
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

            sub_instance = PlanAPI(instance)
            response = sub_instance.fetch(62373)
            # check PlanAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls(
                [call._get('/plan/62373', return_format='dict')])

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
                encodedPolyline=r"aaf{E`|y}T|Ftf@px\\hpe@lnCxw \
                Dbsk@rfx@vhjC`nnDd~f@zkv@nb~ChdmH",
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

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_create(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._post.return_value = {
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
            sub_instance = PlanAPI(instance)
            response = sub_instance.create(Plan(
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
                        "via": None})])))
            # check PlanAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([
                call._post(
                    '/plan/',
                    json={
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
                    return_format='dict')])

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

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_delete(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._delete.return_value = {"message": "OK",
                                             "errors": None}

            sub_instance = PlanAPI(instance)
            response = sub_instance.delete(62493)
            # check PlanAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([call._delete('/plan/62493')])

            correct_response = StatusResponse(message="OK", errors=None)

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_edit(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._patch.return_value = {
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
            sub_instance = PlanAPI(instance)
            response = sub_instance.edit(
                Plan(
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
            )
            # check PlanAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls(
                [call._patch(
                    '/plan/None',
                    json={
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
                                {
                                    'ident': 'EHAM', 'type': 'APT',
                                    'lat': 52.31485, 'lon': 4.75812,
                                    'id': None, 'alt': 0, 'name': 'Schiphol',
                                    'via': None
                                },
                                {
                                    'ident': 'KJFK', 'type': 'APT',
                                    'lat': 40.6399, 'lon': -73.77666,
                                    'id': None, 'alt': 0,
                                    'name': 'John F Kennedy Intl',
                                    'via': None
                                }
                            ],
                            'eastLevels': None,
                            'westLevels': None
                        },
                        'cycle': None
                    }
                )]
            )

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

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_search(self):

        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            mock_response = [
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
            instance._getiter.return_value = (i for i in mock_response)

            sub_instance = PlanAPI(instance)
            response = sub_instance.search(
                PlanQuery(
                    fromICAO="EHAM",
                    toICAO="EHAL"),
                limit=2)

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

            # check PlanAPI method decoded data correctly for given response
            assert list(i for i in response) == correct_response_list
            # check that PlanAPI method made the correct request of FlightPlanDB

            instance.assert_has_calls([call._getiter(
                '/search/plans',
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
                    'includeRoute': None,
                    'limit': None},
                limit=2)])

    def test_plan_like(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._post.return_value = {"message": "Not Found",
                                           "errors": None}

            sub_instance = PlanAPI(instance)
            response = sub_instance.like(42)

            # check PlanAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([call._post('/plan/42/like')])

            correct_response = StatusResponse(message='Not Found', errors=None)

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_unlike(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._delete.return_value = {"message": "OK",
                                             "errors": None}

            sub_instance = PlanAPI(instance)
            response = sub_instance.unlike(42)
            # check PlanAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([
                call._delete('/plan/42/like')])

            correct_response = True

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_has_liked(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._get.return_value = {"message": "OK",
                                          "errors": None}

            sub_instance = PlanAPI(instance)
            response = sub_instance.has_liked(42)
            # check PlanAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([
                call._get('/plan/42/like', ignore_statuses=[404])])

            correct_response = True

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_generate(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._post.return_value = {
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
                'waypoints': 2}

            sub_instance = PlanAPI(instance)
            request_query = GenerateQuery(fromICAO="EHAL", toICAO="EHTX")
            response = sub_instance.generate(request_query)
            # check PlanAPI method made the correct request of FlightPlanDB
            correct_calls = [
                call._post(
                    '/auto/generate',
                    json={
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
                        'descentSpeed': 250})]

            instance.assert_has_calls(correct_calls)

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
                    release=4))

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_decode(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._post.return_value = {
                'application': None,
                'createdAt': '2021-04-28T20:33:57.000Z',
                'cycle': {
                    'id': 38, 'ident': 'FPD2104', 'release': 4, 'year': 21},
                'distance': 757.3434118878,
                'downloads': 0,
                'encodedPolyline': '_hxfEntgjUr_S_`qAgvaEo'
                'cvBsksPgn_a@_~kSwgbc@',
                'flightNumber': None,
                'fromICAO': 'KSAN',
                'fromName': 'San Diego Intl',
                'id': 4179222,
                'likes': 0,
                'maxAltitude': 0,
                'notes': 'Requested: KSAN BROWS TRM LRAIN KDEN',
                'popularity': 1619642037,
                'tags': ['decoded'],
                'toICAO': 'KDEN',
                'toName': 'Denver Intl',
                'updatedAt': '2021-04-28T20:33:57.000Z',
                'user': {
                    'gravatarHash': '3bcb4f39a24700e081f49c3d2d43d277',
                    'id': 18990,
                    'location': None,
                    'username': 'discordflightplannerbot'},
                'waypoints': 5}

            sub_instance = PlanAPI(instance)
            request_query = GenerateQuery(fromICAO="EHAL", toICAO="EHTX")
            response = sub_instance.generate(request_query)
            # check PlanAPI method made the correct request of FlightPlanDB
            correct_calls = [
                call._post(
                    '/auto/generate',
                    json={
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
                        'descentSpeed': 250})]

            instance.assert_has_calls(correct_calls)

            correct_response = Plan(
                id=4179222,
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
                popularity=1619642037,
                notes='Requested: KSAN BROWS TRM LRAIN KDEN',
                encodedPolyline='_hxfEntgjUr_S_`qAgvaEocvBsksPgn_a@_~kSwgbc@',
                createdAt=datetime.datetime(
                    2021, 4, 28, 20, 33, 57, tzinfo=tzutc()),
                updatedAt=datetime.datetime(
                    2021, 4, 28, 20, 33, 57, tzinfo=tzutc()),
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
                    id=38,
                    ident='FPD2104',
                    year=21,
                    release=4))

            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response


if __name__ == "__main__":
    main()
