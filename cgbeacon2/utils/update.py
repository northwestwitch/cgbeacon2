# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

def update_dataset_samples(database, dataset_id, samples, add=True):
    """Update the list of samples for a dataset

    Accepts:
        database(pymongo.database.Database)
        dataset_id(str): id of dataset to be udated
        samples(list): list of samples to be added to/removed from dataset
        add(bool): whether the samples should be added or removed from dataset

    Returns:
        updates_dataset(obj): the updated dataset

    """
    dataset_obj = database["dataset"].find_one({"_id":dataset_id})

    if dataset_obj is None:
        LOG.warning(f"Couldn't find any dataset with ID {dataset_id} in database!")
        return

    datasets_samples = set(dataset_obj.get("samples", []))
    datasets_samples_size = len(datasets_samples)

    for sample in samples: # add new samples to dataset
        datasets_samples.add(sample)

    if len(datasets_samples) > datasets_samples_size:
        # update dataset with new samples
        result = database["dataset"].find_one_and_update(
            {"_id":dataset_id},
            {"$set" : {"samples" : list(datasets_samples)}}
        )
        return result
