import flightplandb
from flightplandb.datatypes import Tag


def test_tags_api(mocker):
    json_response = [
        {
            "name": "Decoded",
            "description": "Flight plans decoded",
            "planCount": 7430,
            "popularity": 0.010143822356129395
        },
        {
            "name": "Generated",
            "description": "Computer generated plans",
            "planCount": 35343,
            "popularity": 0.009036140132228622
        }
                    ]

    correct_response = [
        Tag(name='Decoded',
            description='Flight plans decoded',
            planCount=7430,
            popularity=0.010143822356129395),
        Tag(name='Generated',
            description='Computer generated plans',
            planCount=35343,
            popularity=0.009036140132228622)
        ]

    def patched_get(path, key):
        return json_response

    mocker.patch(
        target='flightplandb.internal.get',
        new=patched_get)

    spy = mocker.spy(flightplandb.internal, "get")

    response = flightplandb.tags.fetch()
    # check that TagsAPI method made correct request of FlightPlanDB
    spy.assert_called_once_with(path='/tags', key=None)
    # check that TagsAPI method decoded data correctly for given response
    assert response == correct_response
