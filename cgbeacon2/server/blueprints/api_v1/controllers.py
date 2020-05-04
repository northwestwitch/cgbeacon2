# -*- coding: utf-8 -*-
import logging
from flask import request, current_app
from cgbeacon2.constants import (
    NO_MANDATORY_PARAMS,
    NO_SECONDARY_PARAMS,
    NO_POSITION_PARAMS,
    NO_SV_END_PARAM,
    INVALID_COORDINATES,
    INVALID_COORD_RANGE,
    BUILD_MISMATCH,
    QUERY_PARAMS_API_V1,
)
from cgbeacon2.models import DatasetAlleleResponse
from cgbeacon2.utils.md5 import md5_key

RANGE_COORDINATES = ("startMin", "startMax", "endMin", "endMax")
LOG = logging.getLogger(__name__)


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

    return mongo_query


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

    # check if genome build requested corresponds to genome build of the available datasets:
    if len(customer_query["datasetIds"]) > 0:
        dset_builds = current_app.db["dataset"].find(
            {"_id": {"$in": customer_query["datasetIds"]}}, {"assembly_id": 1, "_id": 0}
        )
        dset_builds = [
            dset["assembly_id"] for dset in dset_builds if dset["assembly_id"]
        ]
        for dset in dset_builds:
            if dset != customer_query["assemblyId"]:
                # return a bad request 400 error with explanation message
                resp_obj["message"] = dict(
                    error=BUILD_MISMATCH, allelRequest=customer_query,
                )
                return

    # alternateBases OR variantType is also required
    if all(
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
    if (
        customer_query.get("start") is None
        and all([coord in customer_query.keys() for coord in RANGE_COORDINATES])
        is False
    ):
        # return a bad request 400 error with explanation message
        resp_obj["message"] = dict(
            error=NO_POSITION_PARAMS, allelRequest=customer_query,
        )
        return

    if customer_query.get("start"):  # query for exact position
        try:
            if customer_query.get("end") is None:
                if customer_query.get("variantType"):
                    # query for SVs without specifying end position, return error
                    # return a bad request 400 error with explanation message
                    resp_obj["message"] = dict(
                        error=NO_SV_END_PARAM, allelRequest=customer_query,
                    )
                    return
            else:
                mongo_query["end"] = {"$lte": int(customer_query["end"])}
            mongo_query["start"] = {"$gte": int(customer_query["start"])}
        except ValueError:
            # return a bad request 400 error with explanation message
            resp_obj["message"] = dict(
                error=INVALID_COORDINATES, allelRequest=customer_query,
            )

    elif all(
        [coord in customer_query.keys() for coord in RANGE_COORDINATES]
    ):  # range query
        # check that startMin <= startMax <= endMin <= endMax
        try:
            unsorted_coords = [
                int(customer_query[coord]) for coord in RANGE_COORDINATES
            ]
        except ValueError:
            unsorted_coords = [1, 0]
        if unsorted_coords != sorted(unsorted_coords):  # coordinates are not valid
            # return a bad request 400 error with explanation message
            resp_obj["message"] = dict(
                error=INVALID_COORD_RANGE, allelRequest=customer_query,
            )
            return

        mongo_query["start"] = {"$gte": unsorted_coords[0], "$lte": unsorted_coords[1]}
        mongo_query["end"] = {"$gte": unsorted_coords[2], "$lte": unsorted_coords[3]}

    if mongo_query.get("_id") is None:
        # perform normal query
        mongo_query["assemblyId"] = customer_query["assemblyId"]
        mongo_query["referenceName"] = customer_query["referenceName"]
        mongo_query["referenceBases"] = customer_query["referenceBases"]

        if "alternateBases" in customer_query:
            mongo_query["alternateBases"] = customer_query["alternateBases"]

        if "variantType" in customer_query:
            mongo_query["variantType"] = customer_query["variantType"]

    else:
        # use only variant _id in query
        mongo_query.pop("start")
        mongo_query.pop("end", None)


def dispatch_query(mongo_query, response_type, datasets=[]):
    """Query variant collection using a query dictionary

    Accepts:
        mongo_query(dic): a query dictionary
        response_type(str): individual dataset responses -->
            ALL means all datasets even those that don't have the queried variant
            HIT means only datasets that have the queried variant
            MISS means opposite to HIT value, only datasets that don't have the queried variant
            NONE don't return datasets response.
        datasets(list): dataset ids from request "datasetIds" field

    Returns:
        results():

    """
    variant_collection = current_app.db["variant"]

    LOG.info(f"Perform database query -----------> {mongo_query}.")
    LOG.info(f"Response level (datasetAlleleResponses) -----> {response_type}.")

    # End users are only interested in knowing which datasets have one or more specific vars, return only datasets
    variants = list(variant_collection.find(mongo_query, {"_id": 0, "datasetIds": 1}))

    if len(variants) == 0:
        False, []

    if response_type == "NONE":
        if len(variants) > 0:
            return True, []

    else:
        # request datasets:
        req_dsets = set(datasets)

        # IDs of datasets found for this variant(s)
        result = create_ds_allele_response(response_type, req_dsets, variants)
        return result

    return False, []


def create_ds_allele_response(response_type, req_dsets, variants):
    """Create a Beacon Dataset Allele Response

    Accepts:
        response_type(str): ALL, HIT or MISS
        req_dsets(set): datasets requested, could be empty
        variants(list): a list of query results (only dataset info)

    Returns:
        ds_responses(list): list of cgbeacon2.model.DatasetAlleleResponse
    """
    ds_responses = []
    exists = False

    all_dsets = current_app.db["dataset"].find()
    all_dsets = [ds["_id"] for ds in all_dsets]

    if len(req_dsets) == 0:  # if query didn't specify any dataset
        # Use all datasets present in this beacon
        req_dsets = set(all_dsets)

    for ds in req_dsets:
        # check if database contains a dataset with provided ID:
        if not ds in all_dsets:
            LOG.info(f"Provided dataset {ds} could not be found in database")
            continue
        ds_response = DatasetAlleleResponse(ds, variants).__dict__

        # collect responses according to the type of response requested
        if (
            response_type == "ALL"
            or (response_type == "HIT" and ds_response["exists"] is True)
            or (response_type == "MISS" and ds_response["exists"] is False)
        ):
            ds_responses.append(ds_response)

        if ds_response["exists"] is True:
            exists = True

    return exists, ds_responses
