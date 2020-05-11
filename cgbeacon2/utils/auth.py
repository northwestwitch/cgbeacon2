# -*- coding: utf-8 -*-
import logging


LOG = logging.getLogger(__name__)

# Authentication code is based on:
# https://elixir-europe.org/services/compute/aai

def authlevels(request):
    """Returns auth level from a request object

    Accepts:
        request(flask.request) request received by server

    Returns:
        auth_level(tuple): (bool,bool,bool) == (public_access, registered_access, controlled_access)
    """
    auth_level = (True) # public access is always True

    headers = request.headers
    if headers.get("token"):
        LOG.info(f"---------------->TOKENNNNNNNN: {headers['token']}")

    LOG.info(f"---------------->HEADERS: {headers}")
    return headers
