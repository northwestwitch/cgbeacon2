# -*- coding: utf-8 -*-
import logging
from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    render_template,
    flash,
    redirect,
)
from cgbeacon2.constants import CHROMOSOMES
from cgbeacon2.models import Beacon
from .controllers import create_allele_query, dispatch_query

API_VERSION = "1.0.0"
LOG = logging.getLogger(__name__)
api1_bp = Blueprint(
    "api_v1",
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/api_v1/static",
)


@api1_bp.route("/apiv1.0/", methods=["GET"])
def info():
    """Returns Beacon info data as a json object"""

    beacon_config = current_app.config.get("BEACON_OBJ")
    beacon_obj = Beacon(beacon_config, API_VERSION, current_app.db)

    resp = jsonify(beacon_obj.__dict__)
    resp.status_code = 200
    return resp


@api1_bp.route("/apiv1.0/query_form", methods=["GET", "POST"])
def query_form():
    """The endpoint to a super simple query form to interrogate this beacon"""

    all_dsets = current_app.db["dataset"].find()
    all_dsets = [ds["_id"] for ds in all_dsets]
    resp_obj = {}

    if request.method == "POST":
        # Create database query object
        flash(str(dict(request.form)))

        query = create_allele_query(resp_obj, request)

        if resp_obj.get("message") is not None:  # an error must have occurred
            flash(resp_obj["message"]["error"], "danger")

        else:  # query database
            # query database (it should return a datasetAlleleResponses object)
            response_type = resp_obj["allelRequest"].get(
                "includeDatasetResponses", "NONE"
            )
            query_datasets = resp_obj["allelRequest"].get("datasetIds", [])
            exists, ds_allele_responses = dispatch_query(
                query, response_type, query_datasets
            )
            resp_obj["exists"] = exists
            resp_obj["error"] = None
            resp_obj["datasetAlleleResponses"] = ds_allele_responses

            if resp_obj["exists"] == False:
                flash_color = "secondary"

            if len(resp_obj.get("datasetAlleleResponses", [])) > 0:
                # flash response from single datasets:
                for resp in resp_obj["datasetAlleleResponses"]:
                    if resp["exists"] is True:
                        flash(resp, "success")
                    else:
                        flash(resp, "secondary")
            elif resp_obj["exists"] is True:
                flash("Allele was found in this beacon", "success")
            else:
                flash("Allele could not be found", "secondary")

    return render_template(
        "queryform.html",
        chromosomes=CHROMOSOMES,
        dsets=all_dsets,
        form=dict(request.form),
    )


@api1_bp.route("/apiv1.0/query", methods=["GET", "POST"])
def query():
    """Create a query from params provided in the request and return a response with eventual results"""

    beacon_config = current_app.config.get("BEACON_OBJ")
    beacon_obj = Beacon(beacon_config, API_VERSION, current_app.db)

    resp_obj = {}
    resp_status = 200

    # Create database query object
    query = create_allele_query(resp_obj, request)

    if resp_obj.get("message") is not None:
        # an error must have occurred
        resp_status = resp_obj["message"]["error"]["errorCode"]
        resp_obj["message"]["beaconId"] = beacon_obj.id
        resp_obj["message"]["apiVersion"] = API_VERSION

    else:
        resp_obj["beaconId"] = beacon_obj.id
        resp_obj["apiVersion"] = API_VERSION

        # query database (it should return a datasetAlleleResponses object)
        response_type = resp_obj["allelRequest"].get("includeDatasetResponses", "NONE")
        query_datasets = resp_obj["allelRequest"].get("datasetIds", [])
        exists, ds_allele_responses = dispatch_query(
            query, response_type, query_datasets
        )

        resp_obj["exists"] = exists
        resp_obj["error"] = None
        resp_obj["datasetAlleleResponses"] = ds_allele_responses

    resp = jsonify(resp_obj)
    resp.status_code = resp_status
    return resp
