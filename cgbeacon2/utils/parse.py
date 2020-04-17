# -*- coding: utf-8 -*-
import logging
from cyvcf2 import VCF

LOG = logging.getLogger(__name__)


def extract_variants(vcf_file):
    """Parse a VCF file and return its variants as cyvcf2.VCF objects

    Accepts:
        vcf_file(str): path to VCF file

    """
    try:
        vcf_obj = VCF(vcf_file)
    except Exception as err:
        LOG.error(f"Error while creating VCF iterator from variant file:{err}")
        return

    return vcf_obj


def count_variants(vcf_obj):
    """Count how many variants are contained in a VCF object

    Accepts:
        vcf_obj(cyvcf2.VCF): a VCF object

    Returns:
        nr_variants(int): number of variants
    """
    nr_variants = 0
    for vcf_variant in vcf_obj:
        nr_variants += 1

    return nr_variants


def variant_called(vcf_samples, gt_positions, g_types):
    """Return a list of samples where variant was called

    Accepts:
        vcf_samples(list): list of samples contained in VCF, ordered
        gt_positions(list): list of positions to check GT for, i.e [0,2]: (check first and third sample)
        g_types(list): list of GTypes, one for each sample, ordered.

    Returns:
        samples_with_call(list): a list of samples having the specific variant call
    """

    samples_with_call = []

    for i, g_type in enumerate(g_types):
        if i not in gt_positions:  # this sampple should not be considered, skip
            continue

        if g_type in [1, 3]:
            # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
            # Collect only samples with HET or HOM_ALT calls
            samples_with_call.append(vcf_samples[i])

    return samples_with_call
