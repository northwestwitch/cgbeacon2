# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, current_app, jsonify
from cgbeacon2.models import Beacon

LOG = logging.getLogger(__name__)

ap1_bp = Blueprint(
    "api_v1",
    __name__,
)

@ap1_bp.route('/', methods=['GET'])
def info():
    """Returns Beacon info data as a json object"""

    beacon_config = current_app.config.get("BEACON_OBJ")
    beacon_obj = Beacon(beacon_config, "1.0.0")

    resp = jsonify(beacon_obj.__dict__)
    resp.status_code = 200
    return resp
