# -*- coding: utf-8 -*-
import logging
import requests

from authlib.jose import jwt
from cgbeacon2.constants import MISSING_TOKEN, WRONG_SCHEME, MISSING_PUBLIC_KEY


LOG = logging.getLogger(__name__)

# Authentication code is based on:
# https://elixir-europe.org/services/compute/aai

def authlevel(request, elixir_settings):
    """Returns auth level from a request object

    Accepts:
        request(flask.request) request received by server
        elixir_settings(dict) Elixie AAI Oauth2 settings (server, issuers, userinfo)

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
    auth_level = True  # public access is always True

    if "Authorization" in request.headers:
        try:
            scheme, token = request.headers.get("Authorization").split(" ")
        except ValueError:
            return MISSING_TOKEN
        if scheme != "Bearer":
            return WRONG_SCHEME
        elif token == "":
            return MISSING_TOKEN

    public_key = elixir_key(elixir_settings["server"])
    if public_key == MISSING_PUBLIC_KEY:
        return MISSING_PUBLIC_KEY

    

    return True  # Return only public access


def elixir_key(server):
    """Retrieves Elixir AAI public key from Elixir JWK server

    Accepts:
        server(str). HTTP address to an Elixir server providing public key

    Returns:
        key(json) json content of the server response
    """
    try:
        r = requests.get(server)
        return r.json()

    except Exception as ex:
        return MISSING_PUBLIC_KEY
