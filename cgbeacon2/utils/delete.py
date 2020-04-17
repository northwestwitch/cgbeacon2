# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)


def delete_dataset(mongo_db, id):
    """Delete a dataset from dataset collection

    Accepts:
        id(str): dataset id

    Returns:
        result.deleted(int): number of deleted documents
    """

    collection = "dataset"

    try:
        result = mongo_db[collection].delete_one({"_id": id})
    except Exception as err:
        LOG.error(err)
        return
    return result.deleted_count
