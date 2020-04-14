# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

def add_dataset(mongo_db, dataset_dict):
    """Add/modify a dataset

    Accepts:
        mongo_db(pymongo.database.Database)
        dataset_dict(dict)

    Returns:
        inserted_id(str), collection(str): a tuple with values inserted_id and collection name
    """

    inserted_id = None
    collection = "dataset"

    try:
        result = mongo_db[collection].insert_one(dataset_dict)

    except Exception as err:
        LOG.fatal('Error while inserting a new dataset to database:{}'.format(err))
        quit()

    return result.inserted_id, collection
