# -*- coding: utf-8 -*-
import hashlib

class Variant:
    """A variant object"""

    def __init__(self, parsed_variant, datasetIds, genome_assembly="GRCh37"):
        self.referenceName = parsed_variant["chromosome"] # Accepting values 1-22, X, Y, MT
        self.start = parsed_variant["start"] # int, Precise start coordinate position, allele locus (0-based, inclusive)
        self.startMin =  parsed_variant["start"] # int, for for querying imprecise positions
        self.startMax = parsed_variant["start"] # int, for for querying imprecise positions
        self.end = parsed_variant["end"] # int
        self.endMin = parsed_variant["end"]  # int, for for querying imprecise positions
        self.endMax = parsed_variant["end"] # int, for for querying imprecise positions
        self.referenceBases = parsed_variant["reference_bases"] # str, '^([ACGT]+|N)$'
        self.alternateBases = parsed_variant["alternate_bases"] # str, '^([ACGT]+|N)$'
        if parsed_variant.get("variant_type"):
            self.variantType = parsed_variant["variant_type"] # is used to denote structural variants: 'INS', 'DUP', 'DEL', 'INV'
        self.assemblyId = genome_assembly # str
        self.datasetIds = datasetIds # list
        self.sampleIds = parsed_variant["sample_ids"]
        self._id = self._md5_key(self.referenceName, self.start, self.end, self.referenceBases, self.alternateBases, genome_assembly)


    def _md5_key(self, chrom, start, end, ref, alt, assembly):
        """Generate a md5 key representing uniquely the variant

        Accepts:
            chrom(str): chromosome
            start(int): variant start
            end(int): variant end
            ref(str): references bases
            alt(str): alternative bases
            assembly(str) genome assembly (GRCh37 or GRCh38)

        Returns:
            md5_key(str): md5 unique key

        """
        hash = hashlib.md5()
        hash.update((" ".join([chrom, str(start), str(end), str(ref), str(alt), assembly])).encode("utf-8"))
        md5_key = hash.hexdigest()
        return md5_key
