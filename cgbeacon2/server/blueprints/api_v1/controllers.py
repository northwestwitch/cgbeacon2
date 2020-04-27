# -*- coding: utf-8 -*-
import logging
from flask import request, current_app
from cgbeacon2.constants import (
    NO_MANDATORY_PARAMS,
    NO_SECONDARY_PARAMS,
    NO_POSITION_PARAMS,
    NO_SV_END_PARAM,
    INVALID_COORD_RANGE,
    QUERY_PARAMS_API_V1,
)

LOG = logging.getLogger(__name__)


def check_allele_request(resp_obj, customer_query, mongo_query):
    """Check that the query to the server is valid

    Accepts:
        resp_obj(dict): response data that will be returned by server
        customer_query(dict): a dictionary with all the key/values provided in the external request
        mongo_query(dict): the query to collect variants from this server
    """
    # If customer asks for a classical SNV
    if customer_query.get("variantType") is None and all(
        [
            customer_query.get("referenceName"),
            customer_query.get("start",),
            customer_query.get("end"),
            customer_query.get("referenceBases"),
            customer_query.get("alternateBases"),
            customer_query.get("assemblyId"),
        ]
    ):
        # generate md5_key to compare with our database
        mongo_query["_id"] = md5_key(
            customer_query["referenceName"],
            customer_query["start"],
            customer_query.get("end"),
            customer_query["referenceBases"],
            customer_query["alternateBases"],
            customer_query["assemblyId"],
        )

    # Check that the 3 mandatory parameters are present in the query
    if None in [
        customer_query.get("referenceName"),
        customer_query.get("referenceBases"),
        customer_query.get("assemblyId"),
    ]:
        # return a bad request 400 error with explanation message
        resp_obj["message"] = dict(
            error=NO_MANDATORY_PARAMS, allelRequest=customer_query,
        )
        return
    # alternateBases OR variantType is also required
    elif all(
        param is None
        for param in [
            customer_query.get("alternateBases"),
            customer_query.get("variantType"),
        ]
    ):
        # return a bad request 400 error with explanation message
        resp_obj["message"] = dict(
            error=NO_SECONDARY_PARAMS, allelRequest=customer_query,
        )
        return
    # Check that genomic coordinates are provided (even rough)
    elif (
        customer_query.get("start") is None
        and all([coord in customer_query.keys() for coord in range_coordinates])
        is False
    ):
        # return a bad request 400 error with explanation message
        resp_obj["message"] = dict(
            error=NO_POSITION_PARAMS, allelRequest=customer_query,
        )
        return

    elif customer_query.get("start"):  # query for exact position
        if customer_query.get("end") is None:
            if customer_query.get("variantType"):
                # query for SVs without specifying end position, return error
                # return a bad request 400 error with explanation message
                resp_obj["message"] = dict(
                    error=NO_SV_END_PARAM, allelRequest=customer_query,
                )
                return
        else:
            mongo_query["end"] = {"$lte": customer_query["end"]}
        mongo_query["start"] = {"$gte": customer_query["start"]}

    elif all(
        [coord in customer_query.keys() for coord in range_coordinates]
    ):  # range query
        # check that startMin <= startMax <= endMin <= endMax
        range_coordinates = ("startMin", "startMax", "endMin", "endMax")
        try:
            unsorted_coords = [
                int(customer_query[coord]) for coord in range_coordinates
            ]
        except ValueError:
            unsorted_coords = [1, 0]
        sorted_coords = unsorted_coords.sort()
        if sorted_coords != unsorted_coords:  # coordinates are not valid
            # return a bad request 400 error with explanation message
            resp_obj["message"] = dict(
                error=INVALID_COORD_RANGE, allelRequest=customer_query,
            )
            return

        mongo_query["start"] = {"$gte": sorted_coords[0], "$lte": sorted_coords[1]}
        mongo_query["end"] = {"$gte": sorted_coords[2], "$lte": sorted_coords[3]}

    if mongo_query.get("_id") is None:
        # perform variant query using only variant _id and eventual
        mongo_query["assemblyId"] = customer_query["assemblyId"]
        mongo_query["referenceName"] = customer_query["referenceName"]
        mongo_query["referenceBases"] = customer_query["referenceBases"]

        if "alternateBases" in customer_query:
            mongo_query["alternateBases"] = customer_query["alternateBases"]

        if "variantType" in customer_query:
            mongo_query["variantType"] = customer_query["variantType"]
    else:
        mongo_query.pop("start")
        mongo_query.pop("end", None)

    if customer_query.get("datasetIds"):
        mongo_query["datasetIds"] = {"$in": customer_query["datasetIds"]}


def create_allele_query(resp_obj, req):
    """Populates a dictionary with the parameters provided in the request<<

    Accepts:
        resp_obj(dictionary): response data that will be returned by server
        req(flask.request): request received by server

    """
    customer_query = {}
    mongo_query = {}
    exists = False

    if request.method == "GET":
        data = dict(req.args)
        customer_query["datasetIds"] = req.args.getlist("datasetIds")
    else:  # POST method
        data = dict(req.data)
        customer_query["datasetIds"] = req.form.getlist("datasetIds")

    # loop over all available query params
    for param in QUERY_PARAMS_API_V1:
        if data.get(param):
            customer_query[param] = data[param]
    if "includeDatasetResponses" not in customer_query:
        customer_query["includeDatasetResponses"] = "NONE"

    # check if the minimal required params were provided in query
    check_allele_request(resp_obj, customer_query, mongo_query)

    # if an error occurred, do not query database and return error
    if resp_obj.get("message") is not None:
        resp_obj["message"]["allelRequest"] = customer_query
        resp_obj["message"]["exists"] = None
        resp_obj["message"]["datasetAlleleResponses"] = []
        return

    resp_obj["allelRequest"] = customer_query

    # query database
    hits = query_db(mongo_query)


def query_db(mongo_query):
    """Query variant collection using a query dictionary

    Accepts:
        mongo_query(dic): a query dictionary

    Returns.
        results():

    """
    variant_collection = current_app.db["variant"]
    LOG.info(f"DATABASE QUERY IS---------------->{mongo_query}")

    results = variant_collection.find(mongo_query)

    for variant in variants:
        LOG.info(f"FOUND VARIANT---------------->{variant}")
