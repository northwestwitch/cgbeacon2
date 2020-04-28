# -*- coding: utf-8 -*-
from cgbeacon2.utils.md5 import md5_key


class Variant:
    """A variant object"""

    def __init__(self, parsed_variant, dataset_ids, genome_assembly="GRCh37"):
        self.referenceName = parsed_variant[
            "chromosome"
        ]  # Accepting values 1-22, X, Y, MT
        self.start = parsed_variant[
            "start"
        ]  # int, Precise start coordinate position, allele locus (0-based, inclusive)
        self.startMin = parsed_variant[
            "start"
        ]  # int, for for querying imprecise positions
        self.startMax = parsed_variant[
            "start"
        ]  # int, for for querying imprecise positions
        self.end = parsed_variant["end"]  # int
        self.endMin = parsed_variant["end"]  # int, for for querying imprecise positions
        self.endMax = parsed_variant["end"]  # int, for for querying imprecise positions
        self.referenceBases = "".join(
            parsed_variant["reference_bases"]
        )  # str, '^([ACGT]+|N)$'
        self.alternateBases = "".join(
            parsed_variant["alternate_bases"]
        )  # str, '^([ACGT]+|N)$'
        if parsed_variant.get("variant_type"):
            self.variantType = parsed_variant[
                "variant_type"
            ]  # is used to denote structural variants: 'INS', 'DUP', 'DEL', 'INV'
        self.assemblyId = genome_assembly  # str
        self.datasetIds = dataset_ids  # list of dictionaries, i.e. [{ dataset_id: { samples : [list of samples]}  }]
        self._id = md5_key(
            self.referenceName,
            self.start,
            self.end,
            self.referenceBases,
            self.alternateBases,
            genome_assembly,
        )
