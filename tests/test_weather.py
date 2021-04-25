from unittest import TestCase, main
from unittest.mock import patch, call
from flightplandb.submodules.tags import TagsAPI
from flightplandb.datatypes import Tag


class TagsTest(TestCase):
    def test_tags_api(self):

        with patch("flightplandb.flightplandb.FlightPlanDB",
                   autospec=True) as MockClass:
            instance = MockClass.return_value
            instance._get.return_value = [
                {"name": "Decoded",
                 "description": "Flight plans decoded",
                 "planCount": 7430,
                 "popularity": 0.010143822356129395},
                {"name": "Generated",
                 "description": "Computer generated plans",
                 "planCount": 35343,
                 "popularity": 0.009036140132228622}
            ]
            sub_instance = TagsAPI(instance)
            response = sub_instance.fetch()
            # check that TagsAPI method made the correct request of FlightPlanDB
            instance.assert_has_calls([call._get('/tags')])
            correct_response = [
                Tag(name='Decoded',
                    description='Flight plans decoded',
                    planCount=7430,
                    popularity=0.010143822356129395),
                Tag(name='Generated',
                    description='Computer generated plans',
                    planCount=35343,
                    popularity=0.009036140132228622)]
            # check TagsAPI method decoded the data correctly for given response
            assert response == correct_response


if __name__ == "__main__":
    main()
