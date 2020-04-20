# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)


def delete_dataset(database, id):
    """Delete a dataset from dataset collection

    Accepts:
        database(pymongo.database.Database)
        id(str): dataset id

    Returns:
        result.deleted(int): number of deleted documents
    """

    collection = "dataset"

    try:
        result = database[collection].delete_one({"_id": id})
    except Exception as err:
        LOG.error(err)
        return
    return result.deleted_count


def delete_variants(database, ds_id, samples):
    """Delete variants for one or more samples

    Accepts:
        database(pymongo.database.Database)
        ds_id(str): dataset id
        samples(tuple): name of samples in this dataset

    Returns:
        n_removed(int): number of variants removed from database
    """
    n_removed = None
    sample_list = list(samples)
    query = {
        ".".join(["datasetIds", ds_id, "samples"]) :{
            "$in" : [sample_list]
        }
    }
    results = database["variant"].find(query)

    for res in results:
        LOG.info(f"Found variant:{res}")
        n_removed += 1

    return n_removed
