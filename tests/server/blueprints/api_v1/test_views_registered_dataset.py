# -*- coding: utf-8 -*-
import json

def test_cassivari(mock_app):




"""
def test_post_query_registered(mock_app, test_snv, registered_dataset):
    Test receiving classical POST json request and returning a response



    # Having a database with a variant:
    test_snv["datasetIds"] = {"registered_ds" : {"samples": ["ADM1059A1"]}}
    database = mock_app.db
    database["variant"].insert_one(test_snv)

    # And a registered dataset
    database["dataset"].insert_one(registered_dataset)

    data = json.dumps(
        {
            "referenceName": test_snv["referenceName"],
            "start": test_snv["start"],
            "referenceBases": test_snv["referenceBases"],
            "alternateBases": test_snv["alternateBases"],
            "assemblyId": test_snv["assemblyId"],
            "datasetIds": [registered_dataset["_id"]],
            "includeDatasetResponses": "ALL",
        }
    )

    # When calling the endpoing with the POST method
    response = mock_app.test_client().post("/apiv1.0/query", data=data, headers=HEADERS)

    # Should not return error
    assert response.status_code == 200
    resp_data = json.loads(response.data)

    assert resp_data
    """
    """
    # And all the expected fields should be present in the response
    assert resp_data["allelRequest"]["referenceName"] == test_snv["referenceName"]
    assert resp_data["allelRequest"]["start"] == test_snv["start"]
    assert resp_data["allelRequest"]["referenceBases"] == test_snv["referenceBases"]
    assert resp_data["allelRequest"]["alternateBases"] == test_snv["alternateBases"]
    assert resp_data["allelRequest"]["assemblyId"] == test_snv["assemblyId"]
    assert resp_data["allelRequest"]["includeDatasetResponses"] == "HIT"

    # Including the hit result
    assert resp_data["datasetAlleleResponses"][0]["datasetId"] == public_dataset["_id"]
    assert resp_data["datasetAlleleResponses"][0]["exists"] == True
    """
