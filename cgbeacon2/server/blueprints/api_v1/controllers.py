# -*- coding: utf-8 -*-
import logging
from flask import request, current_app, jsonify
from cgbeacon2.constants import (
    NO_MANDATORY_PARAMS,
    NO_SECONDARY_PARAMS,
    NO_POSITION_PARAMS,
    INVALID_COORDINATES,
    BUILD_MISMATCH,
    QUERY_PARAMS_API_V1,
)
from cgbeacon2.models import DatasetAlleleResponse
from cgbeacon2.utils.add import add_variants as variants_loader
from cgbeacon2.utils.delete import delete_variants as variant_deleter
from cgbeacon2.utils.update import update_dataset
from cgbeacon2.utils.parse import (
    get_vcf_samples,
    genes_to_bedtool,
    extract_variants,
    count_variants,
)
from cgbeacon2.utils.md5 import md5_key

RANGE_COORDINATES = ("startMin", "startMax", "endMin", "endMax")
LOG = logging.getLogger(__name__)


def overlapping_samples(dataset_samples, request_samples):
    """Check that at least one sample in a list is contained in a dataset

    Accepts:
        dataset_samples(list): the list of samples contained in the dataset
        request_samples(list): the list of samples provided by user

    Returns:
        bool: True if there is at least a shared samples in the 2 lists, else False
    """
    ds_sampleset = set(dataset_samples)
    sampleset = set(request_samples)
    return bool(sampleset.intersection(ds_sampleset))


def delete_variants(req):
    """Delete variants for one or more sample according to parameters specified in request data.

    Accepts:
        req(flask.request): request received by server

    Returns:
        resp(json object): A json response from the server, containing a message and a status_code
    """
    resp = None
    message = None
    db = current_app.db
    req_data = req.json
    dataset_id = req_data.get("dataset_id")
    dataset = db["dataset"].find_one({"_id": dataset_id})
    samples = req_data.get("samples")

    # Check that request params contain a valid dataset id
    if dataset_id is None or dataset_id == "":
        message = {"message": "Invalid request. Please specify a valid dataset ID"}
    # Check that dataset exists on the server
    elif dataset is None:
        message = {"message": f"Provided dataset '{dataset_id}' was not found on the server"}
    # Check that request params contain a valid list of samples
    elif isinstance(samples, list) is False or samples == []:
        message = {"message": "Please provide a valid list of samples"}
    elif overlapping_samples(dataset.get("samples", []), samples) is False:
        message = {"message": "None of the provided samples was found in the dataset"}
    if message:
        resp = jsonify(message)
        resp.status_code = 422
        return resp

    updated, removed = variant_deleter(current_app.db, dataset_id, samples)
    if updated + removed > 0:
        result = update_dataset(
            database=current_app.db, dataset_id=dataset_id, samples=samples, add=False
        )
    message = {
        "message": f"Number of updated variants:{updated}. Number of deleted variants:{removed}"
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


def add_variants(req):
    """Add variants from a VCF file according to parameters specified in request data.

    Accepts:
        req(flask.request): request received by server

    Returns:
        resp(json object): A json response from the server, containing a message and a status_code
    """
    resp = None
    message = None
    req_data = req.json
    assembly = req_data.get("assemblyId")
    dataset_id = req_data.get("dataset_id")
    vcf_samples = get_vcf_samples(req_data.get("vcf_path"))
    samples = req_data.get("samples")
    # Check if provided dataset exists on the server
    db = current_app.db
    dataset = db["dataset"].find_one({"_id": dataset_id, "assembly_id": assembly})
    if dataset is None:
        message = {"message": f"Provided dataset '{dataset_id}' was not found on the server"}
    # Check if provided file can be parsed
    elif vcf_samples == []:
        message = {"message": f"Error extracting info from VCF file, please check path to VCF"}
    # Chech that eventual samples provided by user are present in the VCF file
    elif samples and all(samplen in vcf_samples for samplen in samples) is False:
        message = {
            "message": f"One or more provided samples were not found in VCF. VCF samples:{vcf_samples}"
        }
    if message:
        resp = jsonify(message)
        resp.status_code = 422
        return resp

    filter_intervals = None
    if req_data.get("genes"):
        hgnc_ids = None
        ensembl_ids = None
        if req_data["genes"].get("id_type") not in ["HGNC", "Ensembl"]:
            message = {
                "message": "Please provide id_type (HGNC or Ensembl) for the given list of genes"
            }
            resp = jsonify(message)
            resp.status_code = 422
            return resp
        if req_data["genes"]["id_type"] == "HGNC":
            hgnc_ids = req_data["genes"]["ids"]
        else:
            ensembl_ids = req_data["genes"]["ids"]
        # retrieve gene intervals in BedTool format
        filter_intervals = genes_to_bedtool(db["gene"], hgnc_ids, ensembl_ids, assembly)
        if (
            filter_intervals is None
        ):  # No valid genes genes for filtering the VCF, do not insert any variant
            message = {"message": f"Could not create a gene filter using the provided gene list"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp

    vcf_obj = extract_variants(
        vcf_file=req_data.get("vcf_path"), samples=samples, filter=filter_intervals
    )
    nr_variants = count_variants(vcf_obj)
    vcf_obj = extract_variants(
        vcf_file=req_data.get("vcf_path"), samples=samples, filter=filter_intervals
    )
    added = variants_loader(
        database=db,
        vcf_obj=vcf_obj,
        samples=set(samples),
        assembly=assembly,
        dataset_id=dataset_id,
        nr_variants=nr_variants,
    )

    if added > 0:
        # Update dataset object accordingly
        update_dataset(database=db, dataset_id=dataset_id, samples=samples, add=True)

    message = {"message": f"Number of inserted variants for samples:{samples}:{added}"}
    resp = jsonify(message)
    resp.status_code = 200
    return resp


def create_allele_query(resp_obj, req):
    """Populates a dictionary with the parameters provided in the request<<

    Accepts:
        resp_obj(dictionary): response data that will be returned by server
        req(flask.request): request received by server

    """
    customer_query = {}
    mongo_query = {}
    exists = False
    data = None

    if req.method == "GET":
        data = dict(req.args)
        customer_query["datasetIds"] = req.args.getlist("datasetIds")
    else:  # POST method
        if req.headers.get("Content-type") == "application/x-www-form-urlencoded":
            data = dict(req.form)
            customer_query["datasetIds"] = req.form.getlist("datasetIds")

        else:  # application/json, This should be default
            data = req.json
            customer_query["datasetIds"] = data.get("datasetIds", [])

        # Remove null parameters from the query
        remove_keys = []
        for key, value in data.items():
            if value == "":
                remove_keys.append(key)
        for key in remove_keys:
            data.pop(key)

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
            customer_query.get(
                "start",
            ),
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
            error=NO_MANDATORY_PARAMS,
            allelRequest=customer_query,
        )
        return

    # check if genome build requested corresponds to genome build of the available datasets:
    if len(customer_query.get("datasetIds", [])) > 0:
        dset_builds = current_app.db["dataset"].find(
            {"_id": {"$in": customer_query["datasetIds"]}}, {"assembly_id": 1, "_id": 0}
        )
        dset_builds = [dset["assembly_id"] for dset in dset_builds if dset["assembly_id"]]
        for dset in dset_builds:
            if dset != customer_query["assemblyId"]:
                # return a bad request 400 error with explanation message
                resp_obj["message"] = dict(
                    error=BUILD_MISMATCH,
                    allelRequest=customer_query,
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
            error=NO_SECONDARY_PARAMS,
            allelRequest=customer_query,
        )
        return
    # Check that genomic coordinates are provided (even rough)
    if (
        customer_query.get("start") is None
        and any([coord in customer_query.keys() for coord in RANGE_COORDINATES]) is False
    ):
        # return a bad request 400 error with explanation message
        resp_obj["message"] = dict(
            error=NO_POSITION_PARAMS,
            allelRequest=customer_query,
        )
        return

    if customer_query.get("start"):  # query for exact position
        try:
            if customer_query.get("end") is not None:
                mongo_query["end"] = int(customer_query["end"])

            mongo_query["start"] = int(customer_query["start"])

        except ValueError:
            # return a bad request 400 error with explanation message
            resp_obj["message"] = dict(
                error=INVALID_COORDINATES,
                allelRequest=customer_query,
            )

    # Range query
    elif any([coord in customer_query.keys() for coord in RANGE_COORDINATES]):  # range query
        # In general startMin <= startMax <= endMin <= endMax, but allow fuzzy ends query

        fuzzy_start_query = {}
        fuzzy_end_query = {}
        try:
            if "startMin" in customer_query:
                fuzzy_start_query["$gte"] = int(customer_query["startMin"])
            if "startMax" in customer_query:
                fuzzy_start_query["$lte"] = int(customer_query["startMax"])
            if "endMin" in customer_query:
                fuzzy_end_query["$gte"] = int(customer_query["endMin"])
            if "endMax" in customer_query:
                fuzzy_end_query["$lte"] = int(customer_query["endMax"])
        except ValueError:
            # return a bad request 400 error with explanation message
            resp_obj["message"] = dict(
                error=INVALID_COORDINATES,
                allelRequest=customer_query,
            )

        if fuzzy_start_query:
            mongo_query["start"] = fuzzy_start_query
        if fuzzy_end_query:
            mongo_query["end"] = fuzzy_end_query

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


def dispatch_query(mongo_query, response_type, datasets=[], auth_levels=([], False)):
    """Query variant collection using a query dictionary

    Accepts:
        mongo_query(dic): a query dictionary
        response_type(str): individual dataset responses -->
            ALL means all datasets even those that don't have the queried variant
            HIT means only datasets that have the queried variant
            MISS means opposite to HIT value, only datasets that don't have the queried variant
            NONE don't return datasets response.
        datasets(list): dataset ids from request "datasetIds" field
        auth_levels(tuple): (registered access datasets(list), bona_fide_status(bool))

    Returns:
        tuple(bool, list): (allele_exists(bool), datasetAlleleResponses(list))

    """
    variant_collection = current_app.db["variant"]

    LOG.info(f"Perform database query -----------> {mongo_query}.")
    LOG.info(f"Response level (datasetAlleleResponses) -----> {response_type}.")

    # End users are only interested in knowing which datasets have one or more specific vars, return only datasets and callCount
    variants = list(
        variant_collection.find(mongo_query, {"_id": 0, "datasetIds": 1, "call_count": 1})
    )

    if len(variants) == 0:
        return False, []

    # Filter variants by auth level specified by user token (or lack of it)
    variants = results_filter_by_auth(variants, auth_levels)

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


def results_filter_by_auth(variants, auth_levels):
    """Filter variants returned by query using auth levels (specified by token, if present, otherwise public access only datasets)

    Accepts:
        variants(list): a list of variants returned by database query
        auth_levels(tuple): (registered access datasets(list), bona_fide_status(bool))

    Return:
        filtered_variants(list): Variants filtered using authlevel criteria
    """

    # Filter variants by auth level (specified by token, if present, otherwise public access only datasets)
    ds_collection = current_app.db["dataset"]
    public_ds = ds_collection.find({"authlevel": "public"})
    pyblic_ds_ids = [ds["_id"] for ds in public_ds]

    LOG.info(f"The following public dataset were found in database:{public_ds}")

    registered_access_ds_ids = auth_levels[0]
    controlled_access_ds_ids = []

    if auth_levels[1] is True:  # user has access to controlled access datasets
        controlled_access_ds = ds_collection.find({"authlevel": "controlled"})
        controlled_access_ds_ids = [ds["_id"] for ds in controlled_access_ds]

    dataset_filter = pyblic_ds_ids + registered_access_ds_ids + controlled_access_ds_ids

    # Filter results
    LOG.info(f"Filtering out results with datasets different from :{dataset_filter}")
    filtered_variants = []

    for variant in variants:
        for key in variant.get("datasetIds", []):
            if key in dataset_filter:
                filtered_variants.append(variant)

    return filtered_variants


def create_ds_allele_response(response_type, req_dsets, variants):
    """Create a Beacon Dataset Allele Response

    Accepts:
        response_type(str): ALL, HIT or MISS
        req_dsets(set): datasets requested, could be empty
        variants(list): a list of query results

    Returns:
        ds_responses(list): list of cgbeacon2.model.DatasetAlleleResponse
    """
    ds_responses = []
    exists = False

    all_dsets = current_app.db["dataset"].find()
    all_dsets = {ds["_id"]: ds for ds in all_dsets}

    if len(req_dsets) == 0:  # if query didn't specify any dataset
        # Use all datasets present in this beacon
        req_dsets = set(all_dsets)

    for ds in req_dsets:
        # check if database contains a dataset with provided ID:
        if not ds in all_dsets:
            LOG.info(f"Provided dataset {ds} could not be found in database")
            continue

        ds_response = DatasetAlleleResponse(all_dsets[ds], variants).__dict__

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
