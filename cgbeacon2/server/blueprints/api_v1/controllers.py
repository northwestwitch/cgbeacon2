# -*- coding: utf-8 -*-
import logging
from flask import request
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

    range_coordinates = ("startMin", "startMax", "endMin", "endMax")

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
                # it never enters in the condition where variantType is None and also alternateBases is none

    elif all(
        [coord in customer_query.keys() for coord in range_coordinates]
    ):  # range query
        # check that startMin <= startMax <= endMin <= endMax
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


def create_allele_query(resp_obj, req):
    """Populates a dictionary with the parameters provided in the request<<

    Accepts:
        resp_obj(dictionary): response data that will be returned by server
        req(flask.request): request received by server

    """
    customer_query = {}
    mongo_query = {}

    if request.method == "GET":
        data = dict(req.args)
    else:  # POST method
        data = dict(req.data)

    # loop over all available query params
    for param in QUERY_PARAMS_API_V1:
        if data.get(param):
            customer_query[param] = data[param]

    # check if the minimal required params were provided in query
    check_allele_request(resp_obj, customer_query, mongo_query)
