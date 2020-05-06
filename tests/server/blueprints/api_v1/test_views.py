# -*- coding: utf-8 -*-
import json

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


################## TESTS FOR HANDLING GET REQUESTS ################


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
    """Test the query endpoint by sending a GET request. Search for SNVs, exact position, return only responses from dataset with no hits (MISS)"""

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


def test_get_request_snv_return_NONE(mock_app, test_snv, test_dataset_cli):
    """Test the query endpoint by sending a GET request. Search for SNVs, includeDatasetResponses=None"""

    # Having a database with a variant:
    database = mock_app.db
    database["variant"].insert_one(test_snv)

    # And a dataset
    database["dataset"].insert_one(test_dataset_cli)

    # when providing the required parameters in a SNV query with includeDatasetResponses=NONE (or omitting the param)
    query_string = "&".join([BASE_ARGS, "start=235826381", ALT_ARG])
    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)

    # No error should be returned
    assert response.status_code == 200
    assert data["allelRequest"]["includeDatasetResponses"] == "NONE"
    # No specific dataset response should be prensent
    assert data["datasetAlleleResponses"] == []
    # But since variant is found, beacon responds: True
    assert data["exists"] is True


def test_get_snv_query_variant_not_found(mock_app, test_dataset_cli):
    """Test a query that should return variant not found (exists=False)"""

    # Having a database with a dataset but no variant:
    database = mock_app.db
    database["dataset"].insert_one(test_dataset_cli)

    # when querying for a variant
    query_string = "&".join([BASE_ARGS, "start=235826381", ALT_ARG])
    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)

    # No error should be returned
    assert response.status_code == 200

    # AllelRequest field should reflect the original query
    assert data["allelRequest"]["referenceName"] is not None
    assert data["allelRequest"]["start"] is not None
    assert data["allelRequest"]["referenceBases"] is not None
    assert data["allelRequest"]["alternateBases"] is not None
    assert data["allelRequest"]["includeDatasetResponses"] == "NONE"

    # and response should be negative (exists=False)
    assert data["exists"] is False
    assert data["error"] is None


################## TESTS FOR HANDLING SV GET REQUESTS ################


def test_get_request_svs_range_coordinates(mock_app, test_sv, test_dataset_cli):
    """test get request providing coordinate range for querying structural variants"""

    # Having a database with a variant:
    database = mock_app.db
    database["variant"].insert_one(test_sv)

    # And a dataset
    database["dataset"].insert_one(test_dataset_cli)

    build = test_sv["assemblyId"]
    chrom = test_sv["referenceName"]
    ref = test_sv["referenceBases"]
    base_sv_coords = (
        f"query?assemblyId={build}&referenceName={chrom}&referenceBases={ref}"
    )

    type = f"variantType={test_sv['variantType']}"

    # When providing range coordinates
    start_min = test_sv["start"] - 5
    start_max = test_sv["start"] + 5
    end_min = test_sv["end"] - 5
    end_max = test_sv["end"] + 5
    range_coords = (
        f"startMin={start_min}&startMax={start_max}&endMin={end_min}&endMax={end_max}"
    )

    query_string = "&".join([base_sv_coords, range_coords, type])

    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))

    data = json.loads(response.data)
    # No error should be returned
    assert response.status_code == 200
    # And the beacon should answer exists=True (variant found)
    assert data["exists"] == True


def test_query_form_get(mock_app):
    """Test the interactive query interface page"""

    # When calling the endpoing with the GET method
    response = mock_app.test_client().get("/apiv1.0/query_form")

    # Should not return error
    assert response.status_code == 200


################## TESTS FOR HANDLING POST REQUESTS ################


def test_query_form_post_snv_exact_coords_found(mock_app, test_snv, test_dataset_cli):
    """Test the interactive query interface, snv, exact coordinates"""

    # Having a database with a variant:
    database = mock_app.db
    database["variant"].insert_one(test_snv)

    # And a dataset
    database["dataset"].insert_one(test_dataset_cli)

    form_data = dict(
        assemblyId=test_snv["assemblyId"],
        referenceName=test_snv["referenceName"],
        start=test_snv["start"],
        referenceBases=test_snv["referenceBases"],
        alternateBases=test_snv["alternateBases"],
        includeDatasetResponses="ALL",
    )

    # When calling the endpoing with the POST method
    response = mock_app.test_client().post("/apiv1.0/query_form", data=form_data)

    # Endpoint should NOT return error
    assert response.status_code == 200

    # And should display exists = true, af the dataset level
    assert "alert alert-success" in str(response.data)
    assert "exists&#39;: True" in str(response.data)


def test_query_form_post_snv_exact_coords_not_found(
    mock_app, test_snv, test_dataset_cli
):
    """Test the interactive query interface, snv, exact coordinates, allele not found"""

    # Having a database with a dataset but no variants
    database = mock_app.db
    database["dataset"].insert_one(test_dataset_cli)

    form_data = dict(
        assemblyId=test_snv["assemblyId"],
        referenceName=test_snv["referenceName"],
        start=test_snv["start"],
        referenceBases=test_snv["referenceBases"],
        alternateBases=test_snv["alternateBases"],
        includeDatasetResponses="NONE",
    )

    # When calling the endpoing with the POST method
    response = mock_app.test_client().post("/apiv1.0/query_form", data=form_data)

    # Endpoint should NOT return error
    assert response.status_code == 200

    # And should display allele NOT found message
    assert "Allele could not be found" in str(response.data)


def test_query_form_post_SV_exact_coords_found(mock_app, test_sv, test_dataset_cli):
    """Test the interactive query interface, sv, exact coordinates"""

    # Having a database with a structural variant:
    database = mock_app.db
    database["variant"].insert_one(test_sv)

    # And a dataset
    database["dataset"].insert_one(test_dataset_cli)

    form_data = dict(
        assemblyId=test_sv["assemblyId"],
        referenceName=test_sv["referenceName"],
        start=test_sv["start"],
        end=test_sv["end"],
        referenceBases=test_sv["referenceBases"],
        variantType=test_sv["variantType"],
        includeDatasetResponses="NONE",
    )

    # When calling the endpoing with the POST method,
    response = mock_app.test_client().post("/apiv1.0/query_form", data=form_data)

    # Endpoint should NOT return error
    assert response.status_code == 200

    # And Allele found message should be displayed on the page
    assert "Allele was found in this beacon" in str(response.data)


def test_query_post_range_coords_SV_found(mock_app, test_sv, test_dataset_cli):
    """Test the interactive query interface, sv, range coordinates"""

    # Having a database with a structural variant:
    database = mock_app.db
    database["variant"].insert_one(test_sv)

    # And a dataset
    database["dataset"].insert_one(test_dataset_cli)

    start_min = test_sv["start"] - 5
    start_max = test_sv["start"] + 5
    end_min = test_sv["end"] - 5
    end_max = test_sv["end"] + 5

    # providing range coordinates in the form data
    form_data = dict(
        assemblyId=test_sv["assemblyId"],
        referenceName=test_sv["referenceName"],
        startMin=start_min,
        startMax=start_max,
        endMin=end_min,
        endMax=end_max,
        referenceBases=test_sv["referenceBases"],
        variantType=test_sv["variantType"],
        includeDatasetResponses="NONE",
    )

    # When calling the endpoing with the POST method,
    response = mock_app.test_client().post("/apiv1.0/query_form", data=form_data)

    # Endpoint should NOT return error
    assert response.status_code == 200

    # And Allele found message should be displayed on the page
    assert "Allele was found in this beacon" in str(response.data)


def test_post_query_error(mock_app, test_snv, test_dataset_cli):
    """Test posting a query with errors, the servers should restuen error"""

    # Example, form data is missing wither alt base or variant type (one of them is mandatory)
    form_data = dict(
        assemblyId=test_snv["assemblyId"],
        referenceName=test_snv["referenceName"],
        start=test_snv["start"],
        end=test_snv["end"],
    )

    # When calling the endpoing with the POST method,
    response = mock_app.test_client().post("/apiv1.0/query_form", data=form_data)

    # Endpoint should retun a page
    assert response.status_code == 200

    # that displays the error
    assert "alert alert-danger" in str(response.data)
    assert "errorCode&#39;: 400" in str(response.data)
