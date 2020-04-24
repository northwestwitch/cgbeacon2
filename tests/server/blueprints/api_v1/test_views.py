# -*- coding: utf-8 -*-
import json
from cgbeacon2.constants import (
    NO_MANDATORY_PARAMS,
    NO_SECONDARY_PARAMS,
    NO_POSITION_PARAMS,
    NO_SV_END_PARAM,
    INVALID_COORD_RANGE,
)

BASE_ARGS = "query?assemblyId=GRCh37&referenceName=1&referenceBases=A"


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


def test_query_get_request_missing_mandatory_params(mock_app):
    """Test the query endpoint by sending a request without mandatory params:
    referenceName, referenceBases, assemblyId
    """

    # When a request missing one or more required params is sent to the server
    response = mock_app.test_client().get("/apiv1.0/query?")

    # Then it should return error
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["message"]["error"] == NO_MANDATORY_PARAMS
    assert data["message"]["exists"] == None
    assert data["message"]["datasetAlleleResponses"] == []
    assert data["message"]["beaconId"]
    assert data["message"]["apiVersion"] == "1.0.0"


def test_query_get_request_missing_secondary_params(mock_app):
    """Test the query endpoint by sending a request without secondary params:
    alternateBases, variantType
    """
    # When a request missing alternateBases or variantType params is sent to the server
    query_string = BASE_ARGS
    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))

    # Then it should return error
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["message"]["error"] == NO_SECONDARY_PARAMS


def test_query_get_request_missing_positions_params(mock_app):
    """Test the query endpoint by sending a request missing coordinate params:
        Either stat or startMin + startMax + endMin + endMax

    """
    # When a request missing start position and all the 4 range position coordinates (startMin, startMax, endMin, endMax)
    query_string = "&".join(
        [BASE_ARGS, "alternateBases=T&startMin=2&startMax=6&endMin=4"]
    )
    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)
    # Then it should return error
    assert response.status_code == 400
    assert data["message"]["error"] == NO_POSITION_PARAMS


def test_query_get_request_non_numerical_sv_coordinates(mock_app):
    """Test the query endpoint by sending a request missing SV coordinates params:
        provide only start but no end param

    """
    query_string = "&".join([BASE_ARGS, "start=4&variantType=DUP"])
    # When a request for SV variants is missing stop position parameter
    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)
    # Then it should return error
    assert response.status_code == 400
    assert data["message"]["error"] == NO_SV_END_PARAM


def test_query_get_request_non_increasing_sv_coordinates(mock_app):
    """Test the query endpoint by sending a request with non-ordered range coordinates"""

    range_coords = "&variantType=DUP&startMin=2&startMax=4&endMin=7&endMax=5"
    query_string = "&".join([BASE_ARGS, range_coords])

    # When a request for range coordinates doesn't contain ordered coordinates
    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)
    # Then it should return error
    assert response.status_code == 400
    assert data["message"]["error"] == INVALID_COORD_RANGE


def test_query_get_request_non_numerical_range_coordinates(mock_app):
    """Test the query endpoint by sending a request with non-numerical range coordinates"""

    range_coords = "&variantType=DUP&startMin=2&startMax=3&endMin=6&endMax=FOO"
    query_string = "&".join([BASE_ARGS, range_coords])

    # When a request for range coordinates doesn't contain integers
    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    data = json.loads(response.data)
    # Then it should return error
    assert response.status_code == 400
    assert data["message"]["error"] == INVALID_COORD_RANGE


def test_get_request_exact_position_snvs(mock_app):
    """Test the query endpoint by sending a GET request. Search for SNVs, exact position"""

    # when providing the required parameters in a SNV query for exact positions
    query_string = "&".join([BASE_ARGS, "start=4&alternateBases=T"])

    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))

    # No error should be returned
    assert response.status_code == 200
