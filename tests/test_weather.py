import flightplandb
from flightplandb.datatypes import Weather


def test_weather_api(mocker):
    json_response = {
        "METAR": "EHAM 250755Z 02009KT 330V130 9999\
            BKN033 07/M00 Q1029 NOSIG",
        "TAF": "TAF EHAM 250442Z 2506/2612 02012KT 9999 BKN030 BECMG\
            2507/2510 CAVOK BECMG 2608/2611 05009KT"
        }

    correct_response = Weather(
        METAR="EHAM 250755Z 02009KT 330V130 9999\
            BKN033 07/M00 Q1029 NOSIG",
        TAF="TAF EHAM 250442Z 2506/2612 02012KT 9999 BKN030 BECMG\
            2507/2510 CAVOK BECMG 2608/2611 05009KT"
        )

    def patched_get(self, path, key):
        return json_response

    mocker.patch.object(
        target=flightplandb.submodules.weather.WeatherAPI,
        attribute="_get",
        new=patched_get)
    instance = flightplandb.submodules.weather.WeatherAPI()
    spy = mocker.spy(instance, "_get")

    response = instance.fetch("EHAM")
    # check that TagsAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='/weather/EHAM', key=None)
    # check that TagsAPI method decoded data correctly for given response
    assert response == correct_response
