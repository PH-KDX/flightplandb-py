from unittest import TestCase, main
from unittest.mock import patch, call
from flightplandb.submodules.plan import PlanAPI
from flightplandb.datatypes import Plan, PlanQuery, User, Application, Route, RouteNode, Via, Cycle, StatusResponse
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
            instance.assert_has_calls([call._get('/plan/62373', return_format='dict')])
           
            correct_response = Plan(id=62373,
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
                )
            
                     
            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response

    def test_plan_search(self):
    
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            mock_response = [
                {'application': None,
                'createdAt': '2020-09-30T21:22:37.000Z',
                'cycle': {'id': 31, 'ident': 'FPD2009', 'release': 9, 'year': 20},
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
                
                {'application': None,
                'createdAt': '2018-09-08T12:23:04.000Z',
                'cycle': {'id': 5, 'ident': 'FPD1809', 'release': 9, 'year': 18},
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
            response = sub_instance.search(PlanQuery(fromICAO="EHAM", toICAO="EHAL"), limit=2)

            correct_response_list = [
                Plan(id=3491827, 
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
                    createdAt=datetime.datetime(2020, 9, 30, 21, 22, 37, tzinfo=tzutc()), 
                    updatedAt=datetime.datetime(2020, 9, 30, 21, 22, 37, tzinfo=tzutc()),
                    tags=['generated'], user=None, application=None, 
                    route=None, 
                    cycle=Cycle(id=31, ident='FPD2009', year=20, release=9)),
                
                Plan(id=1295630, 
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
                    createdAt=datetime.datetime(2018, 9, 8, 12, 23, 4, tzinfo=tzutc()), 
                    updatedAt=datetime.datetime(2018, 9, 8, 12, 23, 4, tzinfo=tzutc()), 
                    tags=['generated'], 
                    user=None, 
                    application=None, 
                    route=None, 
                    cycle=Cycle(id=5, ident='FPD1809', year=18, release=9))
               
            ]
            
            # check PlanAPI method decoded data correctly for given response
            assert list(i for i in response) == correct_response_list
            # check that PlanAPI method made the correct request of FlightPlanDB
            
            instance.assert_has_calls([call._getiter('/search/plans', sort='created', 
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
            instance._post.return_value = {"message":"Not Found",
                                          "errors":None}
            
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
            instance._delete.return_value = {"message":"Not Found",
                                          "errors":None}
            
            sub_instance = PlanAPI(instance)
            response = sub_instance.unlike(42)
            # check PlanAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([call._delete('/plan/42/like', ignore_statuses=[404])])
           
            correct_response = False
            
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
            instance.assert_has_calls([call._get('/plan/42/like', ignore_statuses=[404])])
           
            correct_response = True
            
            # check PlanAPI method decoded data correctly for given response
            assert response == correct_response     
            
            
if __name__ == "__main__":
    main()
