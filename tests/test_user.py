from unittest import TestCase, main
from unittest.mock import patch, call
from flightplandb.submodules.user import UserAPI
from flightplandb.datatypes import User, Plan, UserSmall
import datetime
from dateutil.tz import tzutc


class UserTest(TestCase):
    def test_self_info(self):

        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._get.return_value = {
                "id": 18990,
                "username": "discordflightplannerbot",
                "location": None,
                "gravatarHash": "3bcb4f39a24700e081f49c3d2d43d277",
                "joined": "2020-08-06T17:04:30.000Z",
                "lastSeen": "2020-12-27T12:40:06.000Z",
                "plansCount": 2,
                "plansDistance": 794.0094160460012,
                "plansDownloads": 0,
                "plansLikes": 0
            }
            sub_instance = UserAPI(instance)
            response = sub_instance.me
            correct_response = User(
                id=18990,
                username="discordflightplannerbot",
                location=None,
                gravatarHash="3bcb4f39a24700e081f49c3d2d43d277",
                joined=datetime.datetime(
                    2020, 8, 6, 17, 4, 30,
                    tzinfo=tzutc()
                ),
                lastSeen=datetime.datetime(2020, 12, 27, 12, 40, 6,
                                           tzinfo=tzutc()),
                plansCount=2,
                plansDistance=794.0094160460012,
                plansDownloads=0,
                plansLikes=0
            )
            # check that UserAPI method made correct request of FlightPlanDB
            instance.assert_has_calls([call._get("/me")])
            # check UserAPI method decoded data correctly for given response
            assert response == correct_response

    def test_user_info(self):

        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._get.return_value = {
                "id": 1,
                "username": "lemon",
                "location": "😁",
                "gravatarHash": "7889b0d4380a7194b6b67c8e2765289d",
                "joined": "2008-12-31T15:49:18.000Z",
                "lastSeen": "2021-04-24T00:22:46.000Z",
                "plansCount": 479,
                "plansDistance": 1212799.2736187153,
                "plansDownloads": 10341,
                "plansLikes": 33
            }
            sub_instance = UserAPI(instance)
            response = sub_instance.fetch("lemon")
            correct_response = User(
                id=1,
                username="lemon",
                location="😁",
                gravatarHash="7889b0d4380a7194b6b67c8e2765289d",
                joined=datetime.datetime(
                    2008, 12, 31, 15, 49, 18,
                    tzinfo=tzutc()
                ),
                lastSeen=datetime.datetime(2021, 4, 24, 0, 22, 46,
                                           tzinfo=tzutc()),
                plansCount=479,
                plansDistance=1212799.2736187153,
                plansDownloads=10341,
                plansLikes=33
            )
            # check that UserAPI method made correct request of FlightPlanDB
            instance.assert_has_calls([call._get("/user/lemon")])
            # check UserAPI method decoded data correctly for given response
            assert response == correct_response

    def test_user_plans(self):

        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            mock_response = [
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
                        "location": None
                    }
                }
            ]
            instance._getiter.return_value = (i for i in mock_response)

            sub_instance = UserAPI(instance)
            response = sub_instance.plans("lemon")

            correct_response_list = [
                Plan(id=62373,
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
                     user=User(id=2429,
                               username="example",
                               gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                               location=None
                               )
                     ),
                Plan(id=62493,
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
                     user=User(id=1,
                               username="example",
                               gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                               location=None
                               )
                     )
            ]
            # check UserAPI method decoded data correctly for given response
            assert list(i for i in response) == correct_response_list
            # check that UserAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([call._getiter('/user/lemon/plans',
                                       limit=100,
                                       sort='created')])

    def test_user_likes(self):

        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            mock_response = [
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
                        "location": None
                    }
                }
            ]
            instance._getiter.return_value = (i for i in mock_response)

            sub_instance = UserAPI(instance)
            response = sub_instance.likes("lemon")

            correct_response_list = [
                Plan(id=62373,
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
                     user=User(id=2429,
                               username="example",
                               gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                               location=None
                               )
                     ),
                Plan(id=62493,
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
                     user=User(id=1,
                               username="example",
                               gravatarHash="f30b58b998a11b5d417cc2c78df3f764",
                               location=None
                               )
                     )
            ]
            # check UserAPI method decoded data correctly for given response
            assert list(i for i in response) == correct_response_list
            # check that UserAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([call._getiter('/user/lemon/likes',
                                       limit=100,
                                       sort='created')])

    def test_user_search(self):

        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            mock_response = [
                {"id": 1,
                 "username": 'lemon',
                 "location": '😁',
                 "gravatarHash": '7889b0d4380a7194b6b67c8e2765289d'},
                {"id": 1851,
                 "username": 'lemon2',
                 "location": None,
                 "gravatarHash": '94ff72a00d4ead8c49abd5a0cf411c6f'},
                {"id": 1950,
                 "username": 'lemon6',
                 "location": None,
                 "gravatarHash": 'b807060d00c10513ce04b70918dd07a1'}
            ]
            instance._getiter.return_value = (i for i in mock_response)

            sub_instance = UserAPI(instance)
            response = sub_instance.search("lemon")

            correct_response_list = [
                UserSmall(id=1,
                          username='lemon',
                          location='😁',
                          gravatarHash='7889b0d4380a7194b6b67c8e2765289d'),
                UserSmall(id=1851,
                          username='lemon2',
                          location=None,
                          gravatarHash='94ff72a00d4ead8c49abd5a0cf411c6f'),
                UserSmall(id=1950,
                          username='lemon6',
                          location=None,
                          gravatarHash='b807060d00c10513ce04b70918dd07a1')
            ]
            # check UserAPI method decoded data correctly for given response
            assert list(i for i in response) == correct_response_list
            # check that UserAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([call._getiter('/search/users',
                                       limit=100,
                                       params={'q': 'lemon'})])


if __name__ == "__main__":
    main()
