# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

def add_dataset(mongo_db, dataset_dict, update=False):
    """Add/modify a dataset

    Accepts:
        mongo_db(pymongo.database.Database)
        dataset_dict(dict)

    Returns:
        inserted_id(str): the _id of the added/updated dataset
    """

    inserted_id = None
    collection = "dataset"

    if update is True: # update an existing dataset
        #LOG.info(f"Updating dataset collection with dataset id: {id}..")
        old_dataset = mongo_db[collection].find_one({'_id': dataset_dict['_id']})

        if old_dataset is None:
            LOG.fatal("Couldn't find any dataset with id '{}' in the database".format(dataset_dict['_id']))
            return
        dataset_dict["created"] = old_dataset["created"]
        result = mongo_db[collection].replace_one({'_id': dataset_dict['_id']}, dataset_dict)
        if result.modified_count > 0:
            return dataset_dict['_id']
        else:
            return
    try:
        result = mongo_db[collection].insert_one(dataset_dict)

    except Exception as err:
        LOG.error(err)
        return

    return result.inserted_id
