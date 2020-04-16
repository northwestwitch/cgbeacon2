# -*- coding: utf-8 -*-
import logging
from cyvcf2 import VCF
from cgbeacon2.models.variant import Variant
from cgbeacon2.constants import CHROMOSOMES

LOG = logging.getLogger(__name__)

def extract_variants(vcf_file):
    """Parse a VCF file and return its variants as cyvcf2.VCF objects

    Accepts:
        vcf_file(str): path to VCF file

    """
    try:
        vcf_obj = VCF(vcf_file)
        # Check if there are any variants in file
        var = next(vcf_obj)
    except Exception as err:
        LOG.error(f"Error while creating VCF iterator from variant file:{err}")
        return

    return vcf_obj


def parse_variants(vcf_obj, type, assembly):
    """Build variant objects from a cyvcf2 VCF iterator

    Accepts:
        vcf_obj(cyvcf2.VCF): a VCF object
        type(str): snv or sv
        assembly(str): chromosome build

    Returns:

    """

    #for variant in vcf_obj:
    #    chrom = variant.CHROM
