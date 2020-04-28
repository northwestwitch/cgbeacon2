# -*- coding: utf-8 -*-
from cgbeacon2 import __version__

class Beacon:
    """Represents a general beacon object"""

    def __init__(self, conf_obj, api_version="1.0.0", database=None):
        self.alternativeUrl = conf_obj.get("alternative_url")
        self.apiVersion = f"v{api_version}"
        self.createDateTime = conf_obj.get("created")
        self.description = conf_obj.get("description")
        self.id = conf_obj.get("id")
        self.info = conf_obj.get("info")
        self.name = conf_obj.get("name")
        self.organisation = conf_obj.get("organisation")
        self.sampleAlleleRequests = self._sample_allele_requests()
        self.version = f"v{__version__}"
        self.welcomeUrl = conf_obj.get("welcome_url")
        self.datasets = self._datasets(database)


    def _datasets(self, database):
        """Retrieve all datasets associated to this Beacon

        Accepts:
            database(pymongo.database.Database)
        Returns:
            datasets(list)
        """
        if database is None:
            return []
        datasets = list(database["dataset"].find())
        for ds in list(datasets):
            if ds.get("samples") is not None :
                # return number of samples for each dataset, not sample names
                ds["sampleCount"] = len(ds.get("samples"))
                ds.pop("samples")
        return datasets

    def _sample_allele_requests(self):
        """Return some example allele requests"""
        return []
