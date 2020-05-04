# -*- coding: utf-8 -*-
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
def mock_app(database):
    """Create a test app to be used in the tests"""
    app = create_app()
    app.db = database
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
        "datasetIds": {"dataset1": {"samples": ["ADM1059A1"]}},
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
        "datasetIds": {"test_ds": {"samples": ["ADM1059A1"]}},
    }
    return variant


@pytest.fixture
def test_dataset_cli():
    """A test dataset dictionary"""
    dataset = dict(
        _id="dataset1",
        name="Test dataset",
        assembly_id="GRCh37",
        description="Test dataset description",
        version=1.0,
        url="external_url.url",
        consent_code="HMB",
    )
    return dataset


@pytest.fixture
def test_dataset_no_variants():
    """A test dataset dictionary"""
    dataset = dict(
        _id="dataset2",
        name="Test dataset 2",
        assembly_id="GRCh37",
        description="Test dataset 2 description",
        version=1.0,
        url="external_url2.url",
        consent_code="FOO",
    )
    return dataset
