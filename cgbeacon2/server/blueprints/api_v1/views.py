# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, current_app, jsonify, request
from cgbeacon2.models import Beacon
from .controllers import create_allele_request

API_VERSION = "1.0.0"
LOG = logging.getLogger(__name__)
api1_bp = Blueprint("api_v1", __name__,)


@api1_bp.route("/apiv1.0/", methods=["GET"])
def info():
    """Returns Beacon info data as a json object"""

    beacon_config = current_app.config.get("BEACON_OBJ")
    beacon_obj = Beacon(beacon_config, API_VERSION)

    resp = jsonify(beacon_obj.__dict__)
    resp.status_code = 200
    return resp


@api1_bp.route("/apiv1.0/query", methods=["GET", "POST"])
def query():
    """Create a query from params provided in the request and return a response with eventual results"""
    # test query:  http://127.0.0.1:5000/apiv1.0/query?assemblyId=GRCh37&referenceName=1&start=1138913&alternateBases=T&includeDatasetResponses=true

    beacon_config = current_app.config.get("BEACON_OBJ")
    beacon_obj = Beacon(beacon_config, API_VERSION)

    resp_obj = {}
    resp_status = 200

    # Create allele request object and eventual error
    create_allele_request(resp_obj, request)

    if resp_obj.get("message"):  # an error must have occurred
        resp_obj["message"]["exists"] = None
        resp_obj["message"]["datasetAlleleResponses"] = []
        resp_obj["message"]["beaconId"] = beacon_obj.id
        resp_obj["message"]["apiVersion"] = API_VERSION
        resp_status = resp_obj["message"]["error"]["errorCode"]

    resp = jsonify(resp_obj)
    resp.status_code = resp_status
    return resp
