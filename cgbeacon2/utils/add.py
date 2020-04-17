# -*- coding: utf-8 -*-
import logging
from progress.bar import Bar

from cgbeacon2.constants import CHROMOSOMES
from cgbeacon2.models.variant import Variant

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


def add_variants(vcf_obj, samples, assembly, dataset_id, nr_variants):
    """Build variant objects from a cyvcf2 VCF iterator

    Accepts:
        vcf_obj(cyvcf2.VCF): a VCF object
        samples(set): set of samples to add variants for
        assembly(str): chromosome build
        dataset_id(str): dataset id
        nr_variant(int): number of variants contained in VCF file
    Returns:

    """
    LOG.info("Parsing variants..\n")

    with Bar('Processing', max=nr_variants) as bar:

        for vcf_variant in vcf_obj:
            if vcf_variant.CHROM not in CHROMOSOMES:
                LOG.warning(f"chromosome '{vcf_variant.CHROM}' not included in canonical chromosome list, skipping it.")
                continue

            parsed_variant = dict(
                chromosome = vcf_variant.CHROM,
                start = vcf_variant.start,
                end = vcf_variant.end,
                reference_bases = vcf_variant.REF,
                alternate_bases = vcf_variant.ALT,
            )
            if vcf_variant.var_type == "sv": #otherwise snp or indel
                parsed_variant["variant_type"] = "sv" #fix later

            # Create standard variant object with specific _id
            variant = Variant(parsed_variant, [dataset_id], assembly)
            bar.next()

    return nr_variants
