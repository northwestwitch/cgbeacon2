# -*- coding: utf-8 -*-
import json
import pytest
from authlib.jose import jwt
from authlib.jose.errors import ExpiredTokenError
from cgbeacon2.constants import (
    MISSING_TOKEN,
    WRONG_SCHEME,
    EXPIRED_TOKEN_SIGNATURE,
    INVALID_TOKEN_CLAIMS,
    MISSING_TOKEN_CLAIMS,
    MISSING_PUBLIC_KEY,
    NO_GA4GH_USERDATA,
)
from cgbeacon2.utils import auth

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
    headers["Authorization"] = "Basic " + test_token

    # When a POST request Authorization="" is sent
    response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)

    # Then it should return unauthorized error 401
    assert response.status_code == 401
    data = json.loads(response.data)

    assert data["errorMessage"] == WRONG_SCHEME["errorMessage"]


def test_validate_test_token(test_token, pem):
    """Test validate demo token"""

    # Having a test token
    assert test_token

    # Decoding it
    claims = jwt.decode(test_token, pem)
    claims.validate()


def test_validate_expired_token(expired_token, pem):
    """Perform validation on an expired token"""

    # When a token is expired
    assert expired_token
    claims = jwt.decode(expired_token, pem)

    # Validate token should raise specific
    with pytest.raises(ExpiredTokenError) as excinfo:
        claims.validate()
    assert excinfo.match(r"The token is expired")


def test_post_request_expired_token(mock_app, expired_token, pem, monkeypatch):
    """test receiving a POST request containing an expired token"""

    # Monkeypatch Elixir JWT server public key
    def mock_public_server(*args, **kwargs):
        return pem

    # Elixir key is not collected from elixir server, but mocked
    monkeypatch.setattr(auth, "elixir_key", mock_public_server)

    headers = HEADERS
    headers["Authorization"] = "Bearer " + expired_token

    # When the beacon receives a request with this token
    response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)
    data = json.loads(response.data)

    # Should return expired token error
    assert response.status_code == 403
    assert data == EXPIRED_TOKEN_SIGNATURE


def test_post_request_wrong_issuers_token(
    mock_app, wrong_issuers_token, pem, monkeypatch
):
    """test receiving a POST request containing a token with wrong issuers"""

    # Monkeypatch Elixir JWT server public key
    def mock_public_server(*args, **kwargs):
        return pem

    # Elixir key is not collected from elixir server, but mocked
    monkeypatch.setattr(auth, "elixir_key", mock_public_server)

    headers = HEADERS
    headers["Authorization"] = "Bearer " + wrong_issuers_token

    # When a POST request with a token with wrong issuers is sent
    response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)
    data = json.loads(response.data)
    # it should return invalid token claims error
    assert response.status_code == 403
    assert data == INVALID_TOKEN_CLAIMS


def test_post_request_missing_claims_token(mock_app, no_claims_token, pem, monkeypatch):
    """test receiving a POST request containing a token with no claims"""

    # Monkeypatch Elixir JWT server public key
    def mock_public_server(*args, **kwargs):
        return pem

    # Elixir key is not collected from elixir server, but mocked
    monkeypatch.setattr(auth, "elixir_key", mock_public_server)

    headers = HEADERS
    headers["Authorization"] = "Bearer " + no_claims_token

    # When a POST request with a token with missing claims
    response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)
    data = json.loads(response.data)

    # it should return missing claims error
    assert response.status_code == 403
    assert data == MISSING_TOKEN_CLAIMS


def test_post_request_missing_public_key(
    mock_app, test_token, monkeypatch, mock_oauth2
):
    """test receiving a post request with a token when the public key to decode it is available"""

    headers = HEADERS
    headers["Authorization"] = "Bearer " + test_token

    mock_app.config["ELIXIR_OAUTH2"] = mock_oauth2

    # When a POST request with token is sent, but public key is not available
    response = mock_app.test_client().post("/apiv1.0/query?", headers=headers)
    data = json.loads(response.data)

    # it should return missing public key error
    assert response.status_code == 403
    assert data == MISSING_PUBLIC_KEY


def test_post_request_invalid_token_signature(mock_app, pem, monkeypatch, basic_query):
    """test receiving a POST request containing a token that triggers the InvalidTokenError"""

    # generate a random token not using the test public key
    wrong_token = jwt.encode({"alg": "HS256"}, {"aud": ["foo", "bar"]}, "k").decode(
        "utf-8"
    )
    assert wrong_token

    # Monkeypatch Elixir JWT server public key
    def mock_public_server(*args, **kwargs):
        return pem

    # Elixir key is not collected from elixir server, but mocked
    monkeypatch.setattr(auth, "elixir_key", mock_public_server)

    headers = HEADERS
    headers["Authorization"] = "Bearer " + wrong_token

    # When a POST request with the wrong token is sent
    response = mock_app.test_client().post(
        "/apiv1.0/query?", headers=headers, data=json.dumps(basic_query)
    )
    data = json.loads(response.data)

    # it should return bad signature error
    assert response.status_code == 403
    assert "bad_signature" in data["errorMessage"]


def test_post_request_token_no_oidc(
    mock_app, test_token, pem, monkeypatch, basic_query, mock_oauth2
):
    """Test receiving a POST request with valid token, but a non-valid OIDC is set"""

    # Monkeypatch Elixir JWT server public key
    def mock_public_server(*args, **kwargs):
        return pem

    # Elixir key is not collected from elixir server, but mocked
    monkeypatch.setattr(auth, "elixir_key", mock_public_server)

    headers = HEADERS
    headers["Authorization"] = "Bearer " + test_token

    mock_app.config["ELIXIR_OAUTH2"]["userinfo"] = mock_oauth2["userinfo"]

    # When a POST request with a valid token, but in absence of OIDC provider is sent
    response = mock_app.test_client().post(
        "/apiv1.0/query?", headers=headers, data=json.dumps(basic_query)
    )
    data = json.loads(response.data)

    # it should return a 403 error
    assert response.status_code == 403
    # With OIDC unreachable error
    assert data == NO_GA4GH_USERDATA


def test_post_request_token_ok_passports(mock_app, test_token, pem, monkeypatch, basic_query, mock_oauth2):
    """Test receiving a POST request with valid token, valid userdata passports"""

    # Monkeypatch Elixir JWT server public key
    def mock_public_server(*args, **kwargs):
        return pem

    def mock_ga4gh_userdata(*args, **kwargs):
        pass

    # Elixir key is not collected from elixir server, but mocked
    monkeypatch.setattr(auth, "elixir_key", mock_public_server)
    # And OIDC provider is mocked
    monkeypatch.setattr(auth, "ga4gh_userdata", mock_ga4gh_userdata)

    headers = HEADERS
    headers["Authorization"] = "Bearer " + test_token

    mock_app.config["ELIXIR_OAUTH2"]["userinfo"] = mock_oauth2["userinfo"]

    # When a POST request with a valid token, but in absence of OIDC provider is sent
    response = mock_app.test_client().post(
        "/apiv1.0/query?", headers=headers, data=json.dumps(basic_query)
    )
    data = json.loads(response.data)

    # it should return a valid response
    assert response.status_code ==200

    assert data == "asks"
