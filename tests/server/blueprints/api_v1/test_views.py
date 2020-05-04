# -*- coding: utf-8 -*-
import json
from cgbeacon2.constants import (
    NO_MANDATORY_PARAMS,
    NO_SECONDARY_PARAMS,
    NO_POSITION_PARAMS,
    NO_SV_END_PARAM,
    INVALID_COORD_RANGE,
    BUILD_MISMATCH,
)

BASE_ARGS = "query?assemblyId=GRCh37&referenceName=1&referenceBases=TA"
COORDS_ARGS = "start=235826381&end=235826383"
ALT_ARG = "alternateBases=T"


def test_info(mock_app):
    """Test the endpoint that returns the beacon info"""

    # When calling the endpoing with the GET method
    response = mock_app.test_client().get("/apiv1.0/")
    assert response.status_code == 200

    # The returned data should contain all the mandatory fields
    data = json.loads(response.data)
    fields = ["id", "name", "apiVersion", "organisation", "datasets"]
    for field in fields:
        assert data[field] is not None


################## TESTS FOR HANDLING SNV REQUESTS ################


def test_get_request_exact_position_snv_return_ALL(
    mock_app, test_snv, test_dataset_cli, test_dataset_no_variants
):
    """Test the query endpoint by sending a GET request. Search for SNVs, exact position, return responses from ALL datasets"""

    # Having a dataset with a variant:
    database = mock_app.db
    database["variant"].insert_one(test_snv)

    # And 2 datasets
    test_dataset_cli["samples"] = ["ADM1059A1"]
    for ds in [test_dataset_cli, test_dataset_no_variants]:
        database["dataset"].insert_one(ds)

    # when providing the required parameters in a SNV query for exact positions
    ds_reponse_type = "includeDatasetResponses=ALL"
    query_string = "&".join([BASE_ARGS, COORDS_ARGS, ALT_ARG, ds_reponse_type])

    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)

    # No error should be returned
    assert response.status_code == 200

    # AllelRequest field should reflect the original query
    assert data["allelRequest"]["referenceName"] == "1"
    assert data["allelRequest"]["start"]
    assert data["allelRequest"]["end"]
    assert data["allelRequest"]["referenceBases"] == "TA"
    assert data["allelRequest"]["alternateBases"] == "T"
    assert data["allelRequest"]["includeDatasetResponses"] == "ALL"

    assert data.get("message") is None

    # Beacon info should be returned
    assert data["beaconId"]
    assert data["apiVersion"] == "1.0.0"

    # And both types of responses should be returned (exists=True and exists=False)
    assert len(data["datasetAlleleResponses"]) == 2


def test_get_request_exact_position_snv_return_HIT(
    mock_app, test_snv, test_dataset_cli, test_dataset_no_variants
):
    """Test the query endpoint by sending a GET request. Search for SNVs, exact position, return only responses from dataset with variant (HIT)"""

    # Having a dataset with a variant:
    database = mock_app.db
    database["variant"].insert_one(test_snv)

    # And 2 datasets
    test_dataset_cli["samples"] = ["ADM1059A1"]
    for ds in [test_dataset_cli, test_dataset_no_variants]:
        database["dataset"].insert_one(ds)

    # when providing the required parameters in a SNV query for exact positions
    ds_reponse_type = "includeDatasetResponses=HIT"
    query_string = "&".join([BASE_ARGS, COORDS_ARGS, ALT_ARG, ds_reponse_type])

    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)

    # No error should be returned
    assert response.status_code == 200
    assert data.get("message") is None

    # And only the dataset with hits should be returned
    assert len(data["datasetAlleleResponses"]) == 1
    assert data["datasetAlleleResponses"][0]["datasetId"] == test_dataset_cli["_id"]
    assert data["datasetAlleleResponses"][0]["exists"] == True


def test_get_request_exact_position_snv_return_MISS(
    mock_app, test_snv, test_dataset_cli, test_dataset_no_variants
):
    """Test the query endpoint by sending a GET request. Search for SNVs, exact position, return only responses from dataset with no hots (MISS)"""

    # Having a dataset with a variant:
    database = mock_app.db
    database["variant"].insert_one(test_snv)

    # And 2 datasets
    test_dataset_cli["samples"] = ["ADM1059A1"]
    for ds in [test_dataset_cli, test_dataset_no_variants]:
        database["dataset"].insert_one(ds)

    # when providing the required parameters in a SNV query for exact positions
    ds_reponse_type = "includeDatasetResponses=MISS"
    query_string = "&".join([BASE_ARGS, COORDS_ARGS, ALT_ARG, ds_reponse_type])

    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)

    # No error should be returned
    assert response.status_code == 200
    assert data.get("message") is None

    # And only the dataset with NO hits should be returned
    assert len(data["datasetAlleleResponses"]) == 1
    assert (
        data["datasetAlleleResponses"][0]["datasetId"]
        == test_dataset_no_variants["_id"]
    )
    assert data["datasetAlleleResponses"][0]["exists"] == False


################## TESTS FOR HANDLING SV REQUESTS ################
