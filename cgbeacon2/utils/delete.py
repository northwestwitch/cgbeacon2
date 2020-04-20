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
    n_removed = 0
    sample_list = list(samples)
    query = {
        ".".join(["datasetIds", ds_id, "samples"]) :{
            "$in" : [sample_list]
        }
    }
    results = database["variant"].find(query)

    for res in results:
        updated_item = delete_variant(database, ds_id, res, sample_list)
        if updated_item is not None:
            n_removed += 1

    return n_removed


def delete_variant(database, dataset_id, variant, samples):
    """Delete one variant from database or just update the samples having it

    Accepts:
        database(pymongo.database.Database)
        dataset_id(str): dataset id
        variant(dict): one variant
        samples(list) : list of samples to remove this variant for

    """
    updated = None
    dataset_samples = variant["datasetIds"][dataset_id].get("samples", [])
    for sample in samples: #loop over the samples to remove
        dataset_samples.remove(sample)

    # If there are still samples in database with this variant
    # Keep variant and update the list of samples
    if len(dataset_samples)>0:
        updated = database["variant"].find_one_and_update(
            {"_id" : dataset_id},
            {"$set": {
                ".".join("datasetIds", dataset_id, "samples") : dataset_samples
            }}
        )
        return updated.modified_count
    else: # No samples in database with this variant, remove it
        updated = database["variant"].find_one_and_delete({
            "_id" : dataset_id
        })
        return updated
    return
