import datetime
from unittest import mock

import pytest
from dateutil.tz import tzutc

import flightplandb
from flightplandb.datatypes import (
    Airport,
    Frequency,
    Route,
    RouteNode,
    Runway,
    RunwayEnds,
    SearchNavaid,
    Times,
    Timezone,
    Track,
    Weather,
)


class AsyncIter:
    def __init__(self, items):
        self.items = items

    async def __aiter__(self):
        for item in self.items:
            yield item


# localhost is set on every test to allow async loops
@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_airport_info(patched_internal_get):
    json_response = {
        "ICAO": "EHAL",
        "IATA": None,
        "name": "Ameland",
        "regionName": "Netherlands",
        "elevation": 11.00000001672,
        "lat": 53.4536,
        "lon": 5.67869,
        "magneticVariation": 1.8677087306751243,
        "timezone": {"name": "Europe/Amsterdam", "offset": 7200},
        "times": {
            "sunrise": "2021-04-26T04:14:10.584Z",
            "sunset": "2021-04-26T18:58:16.572Z",
            "dawn": "2021-04-26T03:34:40.249Z",
            "dusk": "2021-04-26T19:37:46.907Z",
        },
        "runwayCount": 1,
        "runways": [
            {
                "ident": "08",
                "width": 97.998687813,
                "length": 2627.1784816836002,
                "bearing": 87.4099,
                "surface": "GRASS",
                "markings": ["VISUAL"],
                "lighting": [""],
                "thresholdOffset": 0,
                "overrunLength": 0,
                "ends": [
                    {"ident": "08", "lat": 53.4534, "lon": 5.67265},
                    {"ident": "26", "lat": 53.4534, "lon": 53.4538},
                ],
                "navaids": [],
            },
            {
                "ident": "26",
                "width": 97.998687813,
                "length": 2627.1784816836002,
                "bearing": 267.42,
                "surface": "GRASS",
                "markings": ["NONE"],
                "lighting": [""],
                "thresholdOffset": 0,
                "overrunLength": 0,
                "ends": [
                    {"ident": "26", "lat": 53.4538, "lon": 5.68473},
                    {"ident": "08", "lat": 53.4538, "lon": 53.4534},
                ],
                "navaids": [],
            },
        ],
        "frequencies": [
            {"type": "TWR", "frequency": 118350000, "name": "Ameland Radio"}
        ],
        "weather": {"METAR": None, "TAF": None},
    }

    correct_response = Airport(
        ICAO="EHAL",
        IATA=None,
        name="Ameland",
        regionName="Netherlands",
        elevation=11.00000001672,
        lat=53.4536,
        lon=5.67869,
        magneticVariation=1.8677087306751243,
        timezone=Timezone(name="Europe/Amsterdam", offset=7200),
        times=Times(
            sunrise=datetime.datetime(2021, 4, 26, 4, 14, 10, 584000, tzinfo=tzutc()),
            sunset=datetime.datetime(2021, 4, 26, 18, 58, 16, 572000, tzinfo=tzutc()),
            dawn=datetime.datetime(2021, 4, 26, 3, 34, 40, 249000, tzinfo=tzutc()),
            dusk=datetime.datetime(2021, 4, 26, 19, 37, 46, 907000, tzinfo=tzutc()),
        ),
        runwayCount=1,
        runways=[
            Runway(
                ident="08",
                width=97.998687813,
                length=2627.1784816836002,
                bearing=87.4099,
                surface="GRASS",
                markings=["VISUAL"],
                lighting=[""],
                thresholdOffset=0,
                overrunLength=0,
                ends=[
                    RunwayEnds(ident="08", lat=53.4534, lon=5.67265),
                    RunwayEnds(ident="26", lat=53.4534, lon=53.4538),
                ],
                navaids=[],
            ),
            Runway(
                ident="26",
                width=97.998687813,
                length=2627.1784816836002,
                bearing=267.42,
                surface="GRASS",
                markings=["NONE"],
                lighting=[""],
                thresholdOffset=0,
                overrunLength=0,
                ends=[
                    RunwayEnds(ident="26", lat=53.4538, lon=5.68473),
                    RunwayEnds(ident="08", lat=53.4538, lon=53.4534),
                ],
                navaids=[],
            ),
        ],
        frequencies=[Frequency(type="TWR", frequency=118350000, name="Ameland Radio")],
        weather=Weather(METAR=None, TAF=None),
    )

    patched_internal_get.return_value = json_response

    response = await flightplandb.nav.airport("EHAL")
    # check that NavAPI method decoded data correctly for given response
    assert response == correct_response
    # check that NavAPI method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="/nav/airport/EHAL", key=None)


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_nats(patched_internal_get):
    json_response = [
        {
            "ident": "A",
            "route": {
                "eastLevels": [],
                "nodes": [
                    {
                        "id": 8465100,
                        "ident": "RESNO",
                        "lat": 55,
                        "lon": -15,
                        "type": "FIX",
                    },
                    {
                        "id": 243738,
                        "ident": "55/20",
                        "lat": 55,
                        "lon": -20,
                        "type": "LATLON",
                    },
                    {
                        "id": 243581,
                        "ident": "54/30",
                        "lat": 54,
                        "lon": -30,
                        "type": "LATLON",
                    },
                    {
                        "id": 243584,
                        "ident": "53/40",
                        "lat": 53,
                        "lon": -40,
                        "type": "LATLON",
                    },
                    {
                        "id": 243583,
                        "ident": "52/50",
                        "lat": 52,
                        "lon": -50,
                        "type": "LATLON",
                    },
                    {
                        "id": 8423845,
                        "ident": "TUDEP",
                        "lat": 51.1667,
                        "lon": -53.2333,
                        "type": "FIX",
                    },
                ],
                "westLevels": ["350", "370", "390"],
            },
            "validFrom": "2021-04-28T11:30:00.000Z",
            "validTo": "2021-04-28T19:00:00.000Z",
        }
    ]

    correct_response = [
        Track(
            ident="A",
            route=Route(
                nodes=[
                    RouteNode(
                        ident="RESNO",
                        type="FIX",
                        lat=55,
                        lon=-15,
                        id=8465100,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="55/20",
                        type="LATLON",
                        lat=55,
                        lon=-20,
                        id=243738,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="54/30",
                        type="LATLON",
                        lat=54,
                        lon=-30,
                        id=243581,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="53/40",
                        type="LATLON",
                        lat=53,
                        lon=-40,
                        id=243584,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="52/50",
                        type="LATLON",
                        lat=52,
                        lon=-50,
                        id=243583,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="TUDEP",
                        type="FIX",
                        lat=51.1667,
                        lon=-53.2333,
                        id=8423845,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                ],
                eastLevels=[],
                westLevels=["350", "370", "390"],
            ),
            validFrom=datetime.datetime(2021, 4, 28, 11, 30, tzinfo=tzutc()),
            validTo=datetime.datetime(2021, 4, 28, 19, 0, tzinfo=tzutc()),
        )
    ]

    patched_internal_get.return_value = json_response

    response = await flightplandb.nav.nats()
    # check that NavAPI method decoded data correctly for given response
    assert response == correct_response
    # check that NavAPI method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="/nav/NATS", key=None)


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.get")
async def test_pacots(patched_internal_get):
    json_response = [
        {
            "ident": 1,
            "route": {
                "nodes": [
                    {
                        "id": 8465100,
                        "ident": "RESNO",
                        "lat": 55,
                        "lon": -15,
                        "type": "FIX",
                    },
                    {
                        "id": 243738,
                        "ident": "55/20",
                        "lat": 55,
                        "lon": -20,
                        "type": "LATLON",
                    },
                    {
                        "id": 243581,
                        "ident": "54/30",
                        "lat": 54,
                        "lon": -30,
                        "type": "LATLON",
                    },
                    {
                        "id": 243584,
                        "ident": "53/40",
                        "lat": 53,
                        "lon": -40,
                        "type": "LATLON",
                    },
                    {
                        "id": 243583,
                        "ident": "52/50",
                        "lat": 52,
                        "lon": -50,
                        "type": "LATLON",
                    },
                    {
                        "id": 8423845,
                        "ident": "TUDEP",
                        "lat": 51.1667,
                        "lon": -53.2333,
                        "type": "FIX",
                    },
                ]
            },
            "validFrom": "2021-04-28T11:30:00.000Z",
            "validTo": "2021-04-28T19:00:00.000Z",
        }
    ]

    correct_response = [
        Track(
            ident=1,
            route=Route(
                nodes=[
                    RouteNode(
                        ident="RESNO",
                        type="FIX",
                        lat=55,
                        lon=-15,
                        id=8465100,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="55/20",
                        type="LATLON",
                        lat=55,
                        lon=-20,
                        id=243738,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="54/30",
                        type="LATLON",
                        lat=54,
                        lon=-30,
                        id=243581,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="53/40",
                        type="LATLON",
                        lat=53,
                        lon=-40,
                        id=243584,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="52/50",
                        type="LATLON",
                        lat=52,
                        lon=-50,
                        id=243583,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                    RouteNode(
                        ident="TUDEP",
                        type="FIX",
                        lat=51.1667,
                        lon=-53.2333,
                        id=8423845,
                        alt=None,
                        name=None,
                        via=None,
                    ),
                ]
            ),
            validFrom=datetime.datetime(2021, 4, 28, 11, 30, tzinfo=tzutc()),
            validTo=datetime.datetime(2021, 4, 28, 19, 0, tzinfo=tzutc()),
        )
    ]

    patched_internal_get.return_value = json_response

    response = await flightplandb.nav.pacots()
    # check that NavAPI method decoded data correctly for given response
    assert response == correct_response
    # check that NavAPI method made correct request of FlightPlanDB
    patched_internal_get.assert_awaited_once_with(path="/nav/PACOTS", key=None)


@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
@mock.patch("flightplandb.internal.getiter")
async def test_navaid_search(patched_internal_getiter):
    json_response = [
        {
            "airportICAO": None,
            "elevation": 1.0000000015200001,
            "ident": "SPY",
            "lat": 52.5403,
            "lon": 4.85378,
            "name": "SPIJKERBOOR",
            "runwayIdent": None,
            "type": "VOR",
        },
        {
            "airportICAO": None,
            "elevation": 26.000000039520003,
            "ident": "SPY",
            "lat": 52.5403,
            "lon": 4.85378,
            "name": "SPIJKERBOOR VOR-DME",
            "runwayIdent": None,
            "type": "DME",
        },
    ]

    correct_response_list = [
        SearchNavaid(
            ident="SPY",
            type="VOR",
            lat=52.5403,
            lon=4.85378,
            elevation=1.0000000015200001,
            runwayIdent=None,
            airportICAO=None,
            name="SPIJKERBOOR",
        ),
        SearchNavaid(
            ident="SPY",
            type="DME",
            lat=52.5403,
            lon=4.85378,
            elevation=26.000000039520003,
            runwayIdent=None,
            airportICAO=None,
            name="SPIJKERBOOR VOR-DME",
        ),
    ]

    correct_calls = [mock.call(path="/search/nav", params={"q": "SPY"}, key=None)]

    patched_internal_getiter.return_value = AsyncIter(json_response)

    response = flightplandb.nav.search("SPY")
    # check that PlanAPI method decoded data correctly for given response
    response_list = []
    async for i in response:
        response_list.append(i)
    assert response_list == correct_response_list
    # check that PlanAPI method made correct request of FlightPlanDB
    patched_internal_getiter.assert_has_calls(correct_calls)
