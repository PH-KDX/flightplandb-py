from unittest import TestCase, main
from unittest.mock import patch, call
from flightplandb.submodules.nav import NavAPI
from flightplandb.datatypes import (
    Airport, Timezone, Runway, RunwayEnds,
    Frequency, Weather, Times
)
import datetime
from dateutil.tz import tzutc


class NavTest(TestCase):

    def test_airport_info(self):
        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._get.return_value = {
                'ICAO': 'EHAL',
                'IATA': None,
                'name': 'Ameland',
                'regionName': 'Netherlands',
                'elevation': 11.00000001672,
                'lat': 53.4536,
                'lon': 5.67869,
                'magneticVariation': 1.8677087306751243,
                'timezone': {
                    'name': 'Europe/Amsterdam',
                    'offset': 7200},
                'times': {
                    'sunrise': '2021-04-26T04:14:10.584Z',
                    'sunset': '2021-04-26T18:58:16.572Z',
                    'dawn': '2021-04-26T03:34:40.249Z',
                    'dusk': '2021-04-26T19:37:46.907Z'},
                'runwayCount': 1,
                'runways': [
                    {
                        'ident': '08',
                        'width': 97.998687813,
                        'length': 2627.1784816836002,
                        'bearing': 87.4099,
                        'surface': 'GRASS',
                        'markings': ['VISUAL'],
                        'lighting': [''],
                        'thresholdOffset': 0,
                        'overrunLength': 0,
                        'ends': [
                            {
                                'ident': '08',
                                'lat': 53.4534,
                                'lon': 5.67265},
                            {
                                'ident': '26',
                                'lat': 53.4534,
                                'lon': 53.4538}],
                        'navaids': []},
                    {
                        'ident': '26',
                        'width': 97.998687813,
                        'length': 2627.1784816836002,
                        'bearing': 267.42,
                        'surface': 'GRASS',
                        'markings': ['NONE'],
                        'lighting': [''],
                        'thresholdOffset': 0,
                        'overrunLength': 0,
                        'ends': [
                            {
                                'ident': '26',
                                'lat': 53.4538,
                                'lon': 5.68473},
                            {
                                'ident': '08',
                                'lat': 53.4538,
                                'lon': 53.4534}],
                        'navaids': []}],
                'frequencies': [
                    {
                        'type': 'TWR',
                        'frequency': 118350000,
                        'name': 'Ameland Radio'}],
                'weather': {
                    'METAR': None,
                    'TAF': None}}
            sub_instance = NavAPI(instance)
            response = sub_instance.airport("EHAL")
            correct_response = Airport(
                ICAO='EHAL',
                IATA=None,
                name='Ameland',
                regionName='Netherlands',
                elevation=11.00000001672,
                lat=53.4536,
                lon=5.67869,
                magneticVariation=1.8677087306751243,
                timezone=Timezone(
                    name='Europe/Amsterdam',
                    offset=7200),
                times=Times(
                    sunrise=datetime.datetime(
                        2021, 4, 26, 4, 14, 10, 584000, tzinfo=tzutc()),
                    sunset=datetime.datetime(
                        2021, 4, 26, 18, 58, 16, 572000, tzinfo=tzutc()),
                    dawn=datetime.datetime(
                        2021, 4, 26, 3, 34, 40, 249000, tzinfo=tzutc()),
                    dusk=datetime.datetime(
                        2021, 4, 26, 19, 37, 46, 907000, tzinfo=tzutc())),
                runwayCount=1,
                runways=[
                    Runway(
                        ident='08',
                        width=97.998687813,
                        length=2627.1784816836002,
                        bearing=87.4099,
                        surface='GRASS',
                        markings=['VISUAL'],
                        lighting=[''],
                        thresholdOffset=0,
                        overrunLength=0,
                        ends=[
                            RunwayEnds(
                                ident='08',
                                lat=53.4534,
                                lon=5.67265),
                            RunwayEnds(
                                ident='26',
                                lat=53.4534,
                                lon=53.4538)],
                        navaids=[]),
                    Runway(
                        ident='26',
                        width=97.998687813,
                        length=2627.1784816836002,
                        bearing=267.42,
                        surface='GRASS',
                        markings=['NONE'],
                        lighting=[''],
                        thresholdOffset=0,
                        overrunLength=0,
                        ends=[
                            RunwayEnds(
                                ident='26',
                                lat=53.4538,
                                lon=5.68473),
                            RunwayEnds(
                                ident='08',
                                lat=53.4538,
                                lon=53.4534)],
                        navaids=[])],
                frequencies=[
                        Frequency(
                            type='TWR',
                            frequency=118350000,
                            name='Ameland Radio')
                    ],
                weather=Weather(
                        METAR=None,
                        TAF=None))
            # check that NavAPI method made correct request of FlightPlanDB
            instance.assert_has_calls([call._get('/nav/airport/EHAL',
                                       ignore_statuses=[404])])
            # check NavAPI method decoded data correctly for given response
            assert response == correct_response


if __name__ == "__main__":
    main()
