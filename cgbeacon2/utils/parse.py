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
        # Check if there are any variants in file
        var = next(vcf_obj)
    except Exception as err:
        LOG.error(f"Error while creating VCF iterator from variant file:{err}")
        return

    return vcf_obj
