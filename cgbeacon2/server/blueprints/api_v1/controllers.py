# -*- coding: utf-8 -*-
import logging
from flask import request
from cgbeacon2.constants import MISSING_PARAMS_ERROR

LOG = logging.getLogger(__name__)

def set_query(req):
    """Create a a query dictionary from GET or POST requests sent to the query endpoint.

    Accepts:
        req(flask.request)

    Returns:
        query(dict)
    """
    data = None
    query = {}
    if request.method == "GET":
        data = req.args
    else: # POST method
        data = req.data

    # check if the minimal required params were provided in query
    if None in [data.get("referenceName"), data.get("referenceBases"), data.get("assemblyId")]:
        # return a bad request 400 error with explanation message
        return MISSING_PARAMS_ERROR


    query = dict(

    )

    return data
