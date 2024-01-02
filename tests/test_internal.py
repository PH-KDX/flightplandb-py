from flightplandb.internal import _auth_str


def test_auth_str():
    input_key = "test123!"
    expected_output_encoding = "Basic dGVzdDEyMyE6"
    assert _auth_str(input_key) == expected_output_encoding
