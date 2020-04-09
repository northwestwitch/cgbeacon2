# -*- coding: utf-8 -*-

class Variant:
    """A variant object"""

    def __init__(self, parsed_variant, datasetIds, genome_assembly="GRCh37"):
        self.referenceName = parsed_variant["chromosome"] # Accepting values 1-22, X, Y, MT
        self.start = parsed_variant["start"] # int, Precise start coordinate position, allele locus (0-based, inclusive)
        self.startMin =  parsed_variant["startMin"] # int, for for querying imprecise positions
        self.startMax = parsed_variant["startMax"] # int, for for querying imprecise positions
        self.end = parsed_variant["end"] # int
        self.endMin = parsed_variant["endMin"]  # int, for for querying imprecise positions
        self.endMax = parsed_variant["endMax"] # int, for for querying imprecise positions
        self.referenceBases = parsed_variant["referenceBases"] # str, '^([ACGT]+|N)$'
        self.alternateBases = parsed_variant["alternateBases"] # str, '^([ACGT]+|N)$'
        self.variantType = parsed_variant["variantType"] # is used to denote e.g. structural variants.
        self.assemblyId = genome_assembly # str
        self.datasetIds = datasetIds # list

        
