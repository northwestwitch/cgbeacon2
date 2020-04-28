# -*- coding: utf-8 -*-

class DatasetAlleleResponse:
    """Create a Beacon Dataset Allele Response object to be returned by Beacon Response"""

    def __init__(self, dataset_id, variant_obj):
        datasetId = dataset_id
        sampleCount = self._sample_count(variant_obj, datasetId)
        exists = True if sampleCount>0 else False

    def _sample_count(self, variant_obj, datasetId):
        """Count in how many samples of a dataset a variant is found

        Accepts:
            variant_obj(dict)
            datasetId(str)

        """
        if datasetId in variant_obj.get("datasetIds"):
            n_samples = len(variant_obj["datasetIds"][datasetId].get("samples"))
        return 0
