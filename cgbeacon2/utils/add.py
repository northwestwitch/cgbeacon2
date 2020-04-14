# -*- coding: utf-8 -*-

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
        inserted_id = mongo_db[collection].insert_one(obj).inserted_id
    except Exception as err:
        LOG.fatal('Error while inserting a new client/server node to database:{}'.format(err))

    return inserted_id, collection
