# -*- coding: utf-8 -*-
import json
from authlib.jose import jwt
from cgbeacon2.constants import MISSING_TOKEN,WRONG_SCHEME

HEADERS = {"Content-type": "application/json", "Accept": "application/json"}


def test_post_request_wrong_token_no_token(mock_app):
    """test receiving a post request with Auth headers but not token"""

    headers = HEADERS
    headers["Authorization"] = ""

    # When a POST request Authorization="" is sent
    response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)

    # Then it should return unauthorized error 401
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data["errorMessage"] == MISSING_TOKEN["errorMessage"]


def test_post_request_wrong_token_null_token(mock_app):
    """test receiving a post request with Auth headers and wrong scheme"""

    headers = HEADERS
    headers["Authorization"] = "Bearer "

    # When a POST request Authorization="" is sent
    response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)

    # Then it should return unauthorized error 401
    assert response.status_code == 401
    data = json.loads(response.data)

    assert data["errorMessage"] == MISSING_TOKEN["errorMessage"]


def test_post_request_wrong_token_wrong_scheme(mock_app, test_token):
    """test receiving a post request with Auth headers and wrong scheme"""

    headers = HEADERS
    headers["Authorization"] = "Basic "+test_token

    # When a POST request Authorization="" is sent
    response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)

    # Then it should return unauthorized error 401
    assert response.status_code == 401
    data = json.loads(response.data)

    assert data["errorMessage"] == WRONG_SCHEME["errorMessage"]


def test_verify_test_token(test_token, payload, pem):
    """Test validate demo token"""

    # Having a test token
    assert test_token

    # Decoding it
    decoded_token = jwt.decode(test_token, pem, claims_options=payload)

    # Should return stated claims
    assert decoded_token == payload


def test_post_request_valid_token(mock_app, test_token):
    """Test receiving a get request with valid token"""

    headers = HEADERS
    headers["Authorization"] = "Bearer "+test_token

    # When a POST request with Authorization Bearer token is sent
    #response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)

    # Then it should return a valid response
    #assert response.status_code == 200
