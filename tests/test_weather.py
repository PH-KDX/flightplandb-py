from unittest import TestCase, main
from unittest.mock import patch, call
from flightplandb.submodules.weather import WeatherAPI
from flightplandb.datatypes import Weather


class WeatherTest(TestCase):
    def test_weather_api(self):

        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._get.return_value = {
                "METAR": "EHAM 250755Z 02009KT 330V130 9999\
                 BKN033 07/M00 Q1029 NOSIG",
                "TAF": "TAF EHAM 250442Z 2506/2612 02012KT 9999 BKN030 BECMG\
                 2507/2510 CAVOK BECMG 2608/2611 05009KT"
            }
            sub_instance = WeatherAPI(instance)
            response = sub_instance.fetch("EHAM")
            correct_response = Weather(
                METAR="EHAM 250755Z 02009KT 330V130 9999\
                 BKN033 07/M00 Q1029 NOSIG",
                TAF="TAF EHAM 250442Z 2506/2612 02012KT 9999 BKN030 BECMG\
                 2507/2510 CAVOK BECMG 2608/2611 05009KT"
            )
            # check that WeatherAPI method made correct request of FlightPlanDB
            instance.assert_has_calls([call._get('/weather/EHAM')])
            # check WeatherAPI method decoded data correctly for given response
            assert response == correct_response


if __name__ == "__main__":
    main()
