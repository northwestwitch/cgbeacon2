from cgbeacon2.utils.add import add_dataset


def test_add_dataset_twice(public_dataset, database):
    """Test that the add_dataset function exits when the same dataset is added twice"""

    # WHEN a dataset is first saved to database
    result = add_dataset(database, public_dataset)

    # The function should return a non-None document ID
    assert result is not None

    # WHEN the same function is called again to save the same database
    result = add_dataset(database, public_dataset)

    # THEN it should exit and return None
    assert result is None
