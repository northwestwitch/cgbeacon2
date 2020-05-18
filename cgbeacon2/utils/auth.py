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
    NO_GA4GH_USERDATA,
)

LOG = logging.getLogger(__name__)
GA4GH_SCOPES = ["openid", "ga4gh_passport_v1"]

# Authentication code is based on:
# https://elixir-europe.org/services/compute/aai


def authlevel(request, oauth2_settings):
    """Returns auth level from a request object

    Accepts:
        request(flask.request) request received by server
        oauth2_settings(dict) Elixie AAI Oauth2 settings (server, issuers, userinfo)

    Returns:
        auth_level(tuple): (bool,bool,bool) == (public_access, registered_access, controlled_access)

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

    # try decoding the token and getting query permissions
    try:
        decoded_token = jwt.decode(token, public_key, claims_options=claims_options)
        decoded_token.validate()  # validate the token contents

        LOG.info("Auth Token validated.")
        LOG.info(
            f'Identified as {decoded_token["sub"]} user by {decoded_token["iss"]}.'
        )

        # Check the bona fide status against ELIXIR AAI by default or the URL from config
        # dataset_permissions = set()
        # bona_fide = False

        # retrieve Elixir AAI passports associated to the user described by the auth token
        g44gh_passports = ga4gh_passports(decoded_token, token, oauth2_settings)
        if g44gh_passports == NO_GA4GH_USERDATA:
            return NO_GA4GH_USERDATA

        LOG.info(
            f"------------------>DS PERMISSIONS:{dataset_permissions, bona_fide}----BONA FIDE:{bona_fide}"
        )

    except MissingClaimError as ex:
        return MISSING_TOKEN_CLAIMS
    except InvalidClaimError as ex:
        return INVALID_TOKEN_CLAIMS
    except InvalidTokenError as ex:
        return INVALID_TOKEN_AUTH
    except ExpiredTokenError as ex:
        return EXPIRED_TOKEN_SIGNATURE
    except Exception as ex:
        return {"errorCode": 403, "errorMessage": str(ex)}

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


def ga4gh_passports(decoded_token, token, oauth2_settings):
    """Check dataset permissions and bona fide status from ga4gh token payload info

    Auth system is described by this document: https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md

    Accepts:
        decoded_token(dict): A JWT token's payload
        token(str): Token provided by request to this beacon
        oauth2_settings(dict): Elixir Oauth2 settings

    Returns:
        passports(dict):


    """
    passports = None

    if "scope" not in decoded_token:
        return passports

    token_scopes = decoded_token["scope"].split(" ")

    # If token scopes does overlap with GA4GH scopes, return
    if not all(scope in token_scopes for scope in GA4GH_SCOPES):
        return passports

    # Send a GET request to Elixir userifo endpoint, with token
    passports = ga4gh_userdata(token, oauth2_settings.get("userinfo"))
    if passports == NO_GA4GH_USERDATA:
        return NO_GA4GH_USERDATA

    return passports


def ga4gh_userdata(token, elixir_oidc):
    """Sends a request to the Elixir OIDC Broker to retrieve user info (permissions)


    Accepts:
        token(str): token provided by initial request
        elixir_oidc(str): url to Elixir OIDC broker

    Returns:
        passport_info()

    """
    LOG.info("Sending a request to Elixir AAI to get userinfo associated to token")
    headers = {"Authorization": f"Bearer {token}"}
    passport_info = None
    try:
        resp = requests.get(elixir_oidc, headers=headers)
        data = resp.json()
        passport_info = data.get("ga4gh_passport_v1")
    except Exception as ex:
        return NO_GA4GH_USERDATA

    return passport_info
