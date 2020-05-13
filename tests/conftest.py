# -*- coding: utf-8 -*-
from authlib.jose import jwt
import mongomock
import pytest
from cgbeacon2.server import create_app

DATABASE_NAME = "testdb"


@pytest.fixture(scope="function")
def pymongo_client(request):
    """Get a client to the mongo database"""
    mock_client = mongomock.MongoClient()

    def teardown():
        mock_client.drop_database(DATABASE_NAME)

    request.addfinalizer(teardown)
    return mock_client


@pytest.fixture(scope="function")
def database(request, pymongo_client):
    """Get an adapter connected to mongo database"""
    mongo_client = pymongo_client
    database = mongo_client[DATABASE_NAME]
    return database


@pytest.fixture
def mock_oauth2():
    """Mock OAuth2 params for the mock app"""

    mock_params = dict(
        server= "mock_public_key_jwt_server",
        issuers=["http://scilifelab.se"],
        userinfo="mock_oidc_server",
        audience=["audience"],
        verify_aud=True
    )
    return mock_params


@pytest.fixture
def mock_app(database, mock_oauth2):
    """Create a test app to be used in the tests"""
    app = create_app()
    app.db = database

    # fix test oauth2 params for the mock app
    app.config["ELIXIR_OAUTH2"] = mock_oauth2
    return app


@pytest.fixture
def test_snv():
    """A dictionary representing a snv variant as it is saved in database"""
    variant = {
        "_id": "0e331ff7e817513492852ca696588443",
        "referenceName": "1",
        "start": 235826381,
        "startMin": 235826381,
        "startMax": 235826381,
        "end": 235826383,
        "endMin": 235826383,
        "endMax": 235826383,
        "referenceBases": "TA",
        "alternateBases": "T",
        "assemblyId": "GRCh37",
        "datasetIds": {"public_ds": {"samples": ["ADM1059A1"]}},
    }
    return variant


@pytest.fixture
def test_sv():
    """A dictionary representing a sv variant as it is saved in database"""
    variant = {
        "_id": "8623a1f2d1ba887bafed174ab3eb5d41",
        "referenceName": "5",
        "start": 474601,
        "end": 474974,
        "referenceBases": "GCGGGGAGAGAGAGAGAGCGAGCCAGGTTCAGGTCCAGGGAGGAGAGAGACAGCGCGCGCGAGGCGGAGACCTGGAGGGAGAGGAGCTGCGGAGAGGGGTTAGGCGGGGAGGGAGAGAGCCAGGTTCAGGTCCAGGGAGGAGAGAGACAGCGCGCGCGAGGCGGAGACCTGGAGGGAGAGGAGCTGCGGAGAGGGGTTAGGCGGGGAGAGAGAGAGCGAGCCAGGTTCAGGTCCAGGGAGGAGAGAGACAGCGCGCGCGAGGCGGAGACCTGGAGGGAGAGGAGCTGCGGAGAGGGGTTAGGCGGGGAGGGAGAGAGACAGCGCGCGCGAGGCGGAGACCTGGAGGGAGAGGAGCTGCGGAGAGGGGTTAGGC",
        "alternateBases": "GT",
        "variantType": "DEL",
        "assemblyId": "GRCh37",
        "datasetIds": {"public_ds": {"samples": ["ADM1059A1"]}},
    }
    return variant


@pytest.fixture
def public_dataset():
    """A test public dataset dictionary"""
    dataset = dict(
        _id="public_ds",
        name="Public dataset",
        assembly_id="GRCh37",
        authlevel="public",
        description="Public dataset description",
        version=1.0,
        url="external_url.url",
        consent_code="HMB",
    )
    return dataset


@pytest.fixture
def registered_dataset():
    """A test dataset dictionary with registered authlevel"""
    dataset = dict(
        _id="registered_ds",
        name="Registered dataset",
        assembly_id="GRCh37",
        authlevel="registered",
        description="Registered dataset description",
        version=1.0,
        url="external_regostered_url.url",
        consent_code="RUO",
    )
    return dataset


@pytest.fixture
def controlled_dataset():
    """A test dataset dictionary with controlled authlevel"""
    dataset = dict(
        _id="controlled_ds",
        name="Controlled dataset",
        assembly_id="GRCh37",
        authlevel="controlled",
        description="Controlled dataset description",
        version=1.0,
        url="external_regostered_url.url",
        consent_code="IRB",
    )
    return dataset


@pytest.fixture
def public_dataset_no_variants():
    """A test dataset dictionary"""
    dataset = dict(
        _id="dataset2",
        name="Test dataset 2",
        assembly_id="GRCh37",
        authlevel="public",
        description="Test dataset 2 description",
        version=1.0,
        url="external_url2.url",
        consent_code="FOO",
    )
    return dataset


########### Security-related fixtures ###########

@pytest.fixture
def header():
    """Token header"""
    header = {
        "jku": "http://scilifelab.se/jwk",
        "kid": "018c0ae5-4d9b-471b-bfd6-eef314bc7037",
        "alg": "HS256"
    }
    return header


@pytest.fixture
def payload():
    """Token payload"""
    payload={
        "iss": "http://scilifelab.se",
        "aud": "audience",
        "exp": 99999999999,
        "sub": "someone@cgbeacon2.scilifelab.se"
    }
    return payload


@pytest.fixture
def pem():
    """Test pem to include in the key
    https://python-jose.readthedocs.io/en/latest/jwk/index.html#examples
    """
    pem = {
        "kty": "oct",
        "kid": "018c0ae5-4d9b-471b-bfd6-eef314bc7037",
        "use": "sig",
        "alg": "HS256",
        "k": "hJtXIZ2uSN5kbQfbtTNWbpdmhkV8FJG-Onbc6mxCcYg"
    }
    return pem


@pytest.fixture
def test_token(header, payload, pem):
    """Generate and return JWT based on a demo private key"""
    token = jwt.encode(header, payload, pem).decode('utf-8')
    return token
