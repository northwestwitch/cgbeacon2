# -*- coding: utf-8 -*-
import json
from cgbeacon2.constants import MISSING_PARAMS_ERROR


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


def test_query_get_request_missing_params(mock_app):
    """Test the query endpoint by sending a request without required params"""

    # When a request missing one or more required params is sent to the server
    response = mock_app.test_client().get("/apiv1.0/query?")

    # Then it should return error
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["message"]["error"] == MISSING_PARAMS_ERROR



"""
def test_query_get_request(mock_app, query_snv):
    Test the query endpoint by sending a GET request

    query_string = f'query?assemblyId={query_snv["assembly"]}&referenceName={query_snv["chrom"]}&start={query_snv["start"]}&alternateBases={query_snv["alt"]}&includeDatasetResponses={query_snv["include_ds_resp"]}'

    response = mock_app.test_client().get("".join(["/apiv1.0/", query_string]))
    assert response.status_code == 200

"""
