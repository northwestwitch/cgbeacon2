# -*- coding: utf-8 -*-

from cgbeacon2.utils.update import update_dataset_samples


def test_update_dataset_samples_no_dataset(mock_app):
    """Make sure that function returns None if database is not in database"""

    # When database is empty
    database = mock_app.db

    # then the update dataset samples command will return "None"
    result = update_dataset_samples(database, "foo", [])
    assert result == None
