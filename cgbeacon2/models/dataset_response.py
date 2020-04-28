# -*- coding: utf-8 -*-


class DatasetAlleleResponse:
    """Create a Beacon Dataset Allele Response object to be returned by Beacon Response"""

    def __init__(self, dataset_id, variant_obj):
        self.datasetId = dataset_id
        self.sampleCount = self._sample_count(dataset_id, variant_obj)
        self.exists = True if self.sampleCount > 0 else False

    def _sample_count(self, dataset_id, variant_obj):
        """Count in how many samples of a dataset a variant is found

        Accepts:
            dataset_id(str)
            variant_obj(dict)

        Returns:
            n_samples
        """
        if dataset_id in variant_obj.get("datasetIds"):
            if variant_obj["datasetIds"][dataset_id].get("samples"):

                n_samples = len(variant_obj["datasetIds"][dataset_id]["samples"])
                return n_samples
        return 0
