# -*- coding: utf-8 -*-
import logging
from progress.bar import Bar

from cgbeacon2.constants import CHROMOSOMES
from cgbeacon2.models.variant import Variant
from cgbeacon2.utils.parse import variant_called

LOG = logging.getLogger(__name__)


def add_dataset(database, dataset_dict, update=False):
    """Add/modify a dataset

    Accepts:
        database(pymongo.database.Database)
        dataset_dict(dict)

    Returns:
        inserted_id(str): the _id of the added/updated dataset
    """

    inserted_id = None
    collection = "dataset"

    if update is True:  # update an existing dataset
        # LOG.info(f"Updating dataset collection with dataset id: {id}..")
        old_dataset = database[collection].find_one({"_id": dataset_dict["_id"]})

        if old_dataset is None:
            LOG.fatal(
                "Couldn't find any dataset with id '{}' in the database".format(
                    dataset_dict["_id"]
                )
            )
            return
        dataset_dict["created"] = old_dataset["created"]
        result = database[collection].replace_one(
            {"_id": dataset_dict["_id"]}, dataset_dict
        )
        if result.modified_count > 0:
            return dataset_dict["_id"]
        else:
            return
    try:
        result = database[collection].insert_one(dataset_dict)

    except Exception as err:
        LOG.error(err)
        return

    return result.inserted_id


def add_variants(database, vcf_obj, samples, assembly, dataset_id, nr_variants):
    """Build variant objects from a cyvcf2 VCF iterator

    Accepts:
        database(pymongo.database.Database)
        vcf_obj(cyvcf2.VCF): a VCF object
        samples(set): set of samples to add variants for
        assembly(str): chromosome build
        dataset_id(str): dataset id
        nr_variant(int): number of variants contained in VCF file
    Returns:

    """
    LOG.info("Parsing variants..\n")

    # Collect position to check genotypes for (only samples provided by user)
    gt_positions = []
    for i, sample in enumerate(vcf_obj.samples):
        if sample in samples:
            gt_positions.append(i)

    vcf_samples = vcf_obj.samples

    inserted_vars = 0
    with Bar("Processing", max=nr_variants) as bar:
        for vcf_variant in vcf_obj:
            if vcf_variant.CHROM not in CHROMOSOMES:
                LOG.warning(
                    f"chromosome '{vcf_variant.CHROM}' not included in canonical chromosome list, skipping it."
                )
                continue

            # Check if variant was called in provided samples
            sample_calls = variant_called(
                vcf_samples, gt_positions, vcf_variant.gt_types
            )

            if len(sample_calls) == 0:
                continue  # variant was not called in samples of interest

            if vcf_variant.var_type == "sv":  # otherwise snp or indel
                parsed_variant["variant_type"] = "sv"  # fix later, this is not OK yet

            parsed_variant = dict(
                chromosome=vcf_variant.CHROM,
                start=vcf_variant.start,
                end=vcf_variant.end,
                reference_bases=vcf_variant.REF,
                alternate_bases=vcf_variant.ALT,
            )
            dataset_dict = {dataset_id: {"samples": sample_calls}}
            # Create standard variant object with specific _id
            variant = Variant(parsed_variant, dataset_dict, assembly)

            # Load variant into database or update an existing one with new samples and dataset
            result = add_variant(database=database, variant=variant, dataset_id=dataset_id)
            if result is not None:
                inserted_vars += 1

            bar.next()

    return inserted_vars


def add_variant(database, variant, dataset_id):
    """Check if a variant is already in database and update it, otherwise add a new one

    Accepts:
        database(pymongo.database.Database)
        variant(cgbeacon2.models.Variant)
        dataset_id(str): current dataset in use

    Returns:
        result.inserted_id or id of updated variant

    """
    # check if variant already exists
    old_variant = database["variant"].find_one({"_id": variant._id})
    if old_variant is None:  # if it doesn't exist
        # insert variant into database
        result = database["variant"].insert_one(variant.__dict__)
        return result.inserted_id

    else:  # update pre-existing variant
        current_samples = variant.__dict__["datasetIds"][dataset_id]["samples"] # list of current samples
        updated_samples = []

        old_datasets_dict = old_variant["datasetIds"] # dictionary where dataset ids are keys
        if dataset_id in old_datasets_dict: # variant was already found in this dataset

            # check if any sample should be added to the dataset list of samples
            datasets_samples = set(old_datasets_dict[dataset_id]["samples"]) # old samples
            datasets_samples_size = len(datasets_samples) # length of old samples list

            for sample in current_samples:
                datasets_samples.add(sample)

            # if any sample should be added to the dataset sample list
            if len(datasets_samples) > datasets_samples_size:
                # populate thie updated sample list
                updated_samples = list(datasets_samples)

        else:
            # update at the dataset level
            updated_samples = current_samples

        if len(updated_samples) > 0:
            old_datasets_dict[dataset_id] = updated_samples
            # update variant with new samples
            result = database["variant"].update_one(
                {"_id" : old_variant["_id"]},
                {"$set" :
                    {
                        "datasetIds" : old_datasets_dict

                    }
                }
            )
            return result.modified_count
