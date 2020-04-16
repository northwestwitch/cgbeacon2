# -*- coding: utf-8 -*-

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
