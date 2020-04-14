# -*- coding: utf-8 -*-
import mongomock
import pytest
from cgbeacon2.server import create_app

DATABASE_NAME = "testdb"

@pytest.fixture(scope='function')
def pymongo_client(request):
    """Get a client to the mongo database"""
    mock_client = mongomock.MongoClient()
    def teardown():
        mock_client.drop_database(DATABASE_NAME)
    request.addfinalizer(teardown)
    return mock_client

@pytest.fixture(scope='function')
def database(request, pymongo_client):
    """Get an adapter connected to mongo database"""
    mongo_client = pymongo_client
    database = mongo_client[DATABASE_NAME]
    return database

@pytest.fixture
def mock_app():
    """Create a test app to be used in the tests"""
    app = create_app()
    return app

@pytest.fixture
def test_dataset():
    """A test dataset dictionary"""
    dataset = dict(
        _id = "test-dataset",
        name = "Test dataset",
        description = "Test dataset description",
        version = 1.0,
        external_url = "external_url.url",
        info = {
            "bar" : 6,
            "foo" : "b"
        },
        consent_code = "HMB"
    )
    return dataset
