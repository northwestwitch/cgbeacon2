# -*- coding: utf-8 -*-
import logging
import requests

from authlib.jose import jwt
from authlib.jose.errors import (
    MissingClaimError,
    InvalidClaimError,
    ExpiredTokenError,
    InvalidTokenError,
)

from cgbeacon2.constants import (
    MISSING_TOKEN,
    WRONG_SCHEME,
    MISSING_PUBLIC_KEY,
    MISSING_TOKEN_CLAIMS,
    INVALID_TOKEN_CLAIMS,
    EXPIRED_TOKEN_SIGNATURE,
    INVALID_TOKEN_AUTH,
)


LOG = logging.getLogger(__name__)

# Authentication code is based on:
# https://elixir-europe.org/services/compute/aai


def authlevel(request, oauth2_settings):
    """Returns auth level from a request object

    Accepts:
        request(flask.request) request received by server
        oauth2_settings(dict) Elixie AAI Oauth2 settings (server, issuers, userinfo)

    Returns:
        auth_level(tuple): (bool,bool,bool) == (public_access, registered_access, controlled_access)

    curl -X POST \
    localhost:5000/apiv1.0/query \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -H 'Authorization: Bearer ' \
    -d '{"referenceName": "1",
    "start": 156146085,
    "referenceBases": "C",
    "alternateBases": "A",
    "assemblyId": "GRCh37",
    "includeDatasetResponses": "HIT"}'

    """
    token = None

    if "Authorization" not in request.headers:
        return (True, False, False)

    try:
        scheme, token = request.headers.get("Authorization").split(" ")
    except ValueError:
        return MISSING_TOKEN
    if scheme != "Bearer":
        return WRONG_SCHEME
    elif token == "":
        return MISSING_TOKEN

    public_key = elixir_key(oauth2_settings["server"])
    if public_key == MISSING_PUBLIC_KEY:
        return MISSING_PUBLIC_KEY

    claims_options = claims(oauth2_settings)
    LOG.info(f"----------------------->CLAIM OPTIONS IS {claims_options}")

    # try decoding the token and getting query permissions
    try:
        decoded_token = jwt.decode(token, public_key, claims_options=claims_options)
        decoded_token.validate()  # validate the token contents
        LOG.info("Auth Token validated.")
        LOG.info(
            f'Identified as {decoded_token["sub"]} user by {decoded_token["iss"]}.'
        )
    except MissingClaimError as ex:
        return MISSING_TOKEN_CLAIMS
    except InvalidClaimError as ex:
        return INVALID_TOKEN_CLAIMS
    except InvalidTokenError as ex:
        return INVALID_TOKEN_AUTH
    except ExpiredTokenError as ex:
        EXPIRED_TOKEN_SIGNATURE

    return True, True, True  # Return only public access


def elixir_key(server):
    """Retrieves Elixir AAI public key from Elixir JWK server

    Accepts:
        server(str). HTTP address to an Elixir server providing public key

    Returns:
        key(json) json content of the server response or Error
    """
    try:
        r = requests.get(server)
        return r.json()

    except Exception as ex:
        return MISSING_PUBLIC_KEY


def claims(oauth2_settings):
    """Set up web tokens claims options

    Accepts:
        oauth2_settings(dict): dictionary of OAuth2 settings

    Returns:
        claims(dict): a dictionary describing json token web claims
    """

    claims = dict(
        iss=dict(essential=True, values=",".join(oauth2_settings.get("issuers", []))),
        aud=dict(
            essential=oauth2_settings.get("verify_aud", False),
            values=",".join(oauth2_settings.get("audience", [])),
        ),
        exp=dict(essential=True),
    )
    return claims
