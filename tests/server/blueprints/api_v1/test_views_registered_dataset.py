# -*- coding: utf-8 -*-
import json

def test_post_query_auth_token(mock_app, auth_headers, registered_dataset, test_snv):
    """Test receiving classical POST json request with auth token
        curl -X POST \
        localhost:5000/apiv1.0/query \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json' \
        -H 'Authorization: Bearer asaklSJKlajsISJIJDwqjKjskjSajskK' \
        -d '{"referenceName": "1",
        "start": 156146085,
        "referenceBases": "C",
        "alternateBases": "A",
        "assemblyId": "GRCh37",
        "includeDatasetResponses": "HIT"}'
    """

    # Having a database
    database = mock_app.db
    # with a REGISTERED dataset
    database["dataset"].insert_one(registered_dataset)

    data = json.dumps(
        {
            "referenceName": test_snv["referenceName"],
            "start": test_snv["start"],
            "referenceBases": test_snv["referenceBases"],
            "alternateBases": test_snv["alternateBases"],
            "assemblyId": test_snv["assemblyId"],
            "datasetIds": [registered_dataset["_id"]],
            "includeDatasetResponses": "HIT",
        }
    )

    # When calling the endpoing with the POST method
    response = mock_app.test_client().post("/apiv1.0/query", data=data, headers=auth_headers)

    # Should not return error
    assert response.status_code == 200
    resp_data = json.loads(response.data)
