# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, current_app, jsonify, request
from cgbeacon2.models import Beacon
from .controllers import set_query

LOG = logging.getLogger(__name__)
api1_bp = Blueprint("api_v1", __name__,)

@api1_bp.route("/apiv1.0/", methods=["GET"])
def info():
    """Returns Beacon info data as a json object"""

    beacon_config = current_app.config.get("BEACON_OBJ")
    beacon_obj = Beacon(beacon_config, "1.0.0")

    resp = jsonify(beacon_obj.__dict__)
    resp.status_code = 200
    return resp


@api1_bp.route("/apiv1.0/query", methods=["GET", "POST"])
def query():
    """Create a query from params provided in the request and return a response with eventual results"""

    resp_obj = {}
    # test query:  http://127.0.0.1:5000/apiv1.0/query?assemblyId=GRCh37&referenceName=1&start=1138913&alternateBases=T&includeDatasetResponses=true
    query = set_query(request)

    if "error" in query:
        # query was not valid return error response
        resp_obj["message"] = dict(query)
        resp = jsonify(resp_obj)
        resp.status_code = query["error"]["errorCode"]
        return resp

    return "HELLO THERE"
