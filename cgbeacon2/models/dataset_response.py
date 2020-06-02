# -*- coding: utf-8 -*-


class DatasetAlleleResponse:
    """Create a Beacon Dataset Allele Response object to be returned by Beacon Response"""

    def __init__(self, dataset_id, variants):
        self.datasetId = dataset_id
        samples, alleles = self._sample_allele_count(dataset_id, variants)
        self.sampleCount = samples
        self.callCount = alleles
        self.exists = True if self.sampleCount > 0 else False

    def _sample_allele_count(self, dataset_id, variants):
        """Counts samples and allelic calls for one or more variants

        Accepts:
            dataset_id(str)
            variants(list)

        Returns:
            n_samples(int), n_calls(int)
        """
        n_samples = 0
        n_calls = 0
        for variant_obj in variants:
            if dataset_id in variant_obj.get("datasetIds"):
                if variant_obj["datasetIds"][dataset_id].get("samples"):
                    n_samples += len(variant_obj["datasetIds"][dataset_id]["samples"])
                n_calls += variant_obj["call_count"]
        return n_samples, n_calls
