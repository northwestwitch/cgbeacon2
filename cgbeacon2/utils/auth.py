# -*- coding: utf-8 -*-
import logging

from cgbeacon2.constants import MISSING_TOKEN, WRONG_SCHEME

LOG = logging.getLogger(__name__)

# Authentication code is based on:
# https://elixir-europe.org/services/compute/aai


def authlevel(request):
    """Returns auth level from a request object

    Accepts:
        request(flask.request) request received by server

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

    return True  # Return only public access
