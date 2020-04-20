# -*- coding: utf-8 -*-

from cgbeacon2.utils.delete import delete_dataset


def test_delete_dataset_none_id():
    """Test trigger error in delete_dataset"""

    result = delete_dataset(None, "dataset_id")
    assert result is None
