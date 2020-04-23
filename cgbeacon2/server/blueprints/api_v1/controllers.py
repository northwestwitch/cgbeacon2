# -*- coding: utf-8 -*-
import logging
from flask import request
from cgbeacon2.constants import MISSING_PARAMS_ERROR, QUERY_PARAMS_API_V1

LOG = logging.getLogger(__name__)

def create_allele_request(resp_obj, req):
    """Populates a dictionary with the parameters provided in the request<<

    Accepts:
        resp_obj(dictionary): response data that will be returned by server
        req(flask.request): request received by server

    """
    allele_query = {}
    error = None

    if request.method == "GET":
        data = dict(req.args)
    else: # POST method
        data = dict(req.data)

    # loop over all available query params
    for param in QUERY_PARAMS_API_V1:
        if data.get(param):
            allele_query[param] = data[param]

    # check if the minimal required params were provided in query
    if None in [data.get("referenceName"), data.get("referenceBases"), data.get("assemblyId")]:
        # return a bad request 400 error with explanation message
        resp_obj["message"] = dict(
            error = MISSING_PARAMS_ERROR,
            allelRequest = allele_query,
        )
    else:
        resp_obj["alleleRequest"] = allele_query


def set_query(req):
    """Create a a query dictionary from GET or POST requests sent to the query endpoint.

    Accepts:
        req(flask.request)

    Returns:
        query(dict)
    """
    data = None
    query = {}
    query = {}

    return data
