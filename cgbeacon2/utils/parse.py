# -*- coding: utf-8 -*-
import logging
from cyvcf2 import VCF
import os
from pybedtools.bedtool import BedTool
from tempfile import NamedTemporaryFile

LOG = logging.getLogger(__name__)


def extract_variants(vcf_file, samples=None, filter=None):
    """Parse a VCF file and return its variants as cyvcf2.VCF objects

    Accepts:
        vcf_file(str): path to VCF file
        samples(tuple): samples to extract variants for
        filter(BcfTool object)
    """
    try:
        if filter is not None:
            # Genes or chromosomal intervals filter file(s) are provided
            vcf_bed = BedTool(vcf_file)
            LOG.info(
                "Extracting %s intervals from the %s total entries of the VCF file.",
                filter.count(),
                vcf_bed.count(),
            )
            intersections = vcf_bed.intersect(filter, header=True)
            intersected_vars = intersections.count()
            LOG.info("Number of variants found in the intervals:%s", intersected_vars)

            temp_intersections_file = NamedTemporaryFile("w+t", dir=os.getcwd())
            intersections.saveas(temp_intersections_file.name)
            vcf_obj = VCF(temp_intersections_file.name)

            # remove temporary file:
            temp_intersections_file.close()

        else:
            vcf_obj = VCF(vcf_file, samples=list(samples))
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


def merge_intervals(panels):
    """Create genomic intervals to filter VCF files starting from the provided panel file(s)

    Accepts:
        panels(list) : path to one or more panel bed files

    Returns:
        merged_panels(Temp BED File): a temporary file with merged panel intervals

    """
    merged_panels = BedTool(panels[0])
    if len(panels) > 1:
        merged_panels = merged_panels.cat(*panels[1:])

    return merged_panels


def variant_called(vcf_samples, gt_positions, g_types):
    """Return a list of samples where variant was called

    Accepts:
        vcf_samples(list): list of samples contained in VCF, ordered
        gt_positions(list): list of positions to check GT for, i.e [0,2]: (check first and third sample)
        g_types(list): list of GTypes, one for each sample, ordered.

    Returns:
        samples_with_call(dict): a dictionary of samples having the specific variant call with the allele count.
            Example: {sample1:1, sample2:2}
    """

    samples_with_call = {}
    allele_count = 0

    for i, g_type in enumerate(g_types):
        if i not in gt_positions:  # this sampple should not be considered, skip
            continue

        if g_type in [1, 3]:
            # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
            # Collect only samples with HET or HOM_ALT calls
            if g_type == 1:
                allele_count = 1  # HET
            else:
                allele_count = 2  # HOM_ALT

            samples_with_call[vcf_samples[i]] = {"allele_count": allele_count}

    return samples_with_call
