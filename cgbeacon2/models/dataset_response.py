# -*- coding: utf-8 -*-


class DatasetAlleleResponse:
    """Create a Beacon Dataset Allele Response object to be returned by Beacon Response"""

    def __init__(self, dataset_id, variants):
        self.datasetId = dataset_id
        self.sampleCount = self._sample_count(dataset_id, variants)
        self.exists = True if self.sampleCount > 0 else False

    def _sample_count(self, dataset_id, variants):
        """Count in how many samples of a dataset a variant is found

        Accepts:
            dataset_id(str)
            variants(list)

        Returns:
            n_samples
        """
        n_samples = 0
        for variant_obj in variants:
            if dataset_id in variant_obj.get("datasetIds"):
                if variant_obj["datasetIds"][dataset_id].get("samples"):

                    n_samples += len(variant_obj["datasetIds"][dataset_id]["samples"])
                    return n_samples
        return n_samples
