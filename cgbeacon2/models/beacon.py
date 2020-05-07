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
        self.datasets_by_auth_level = self._datasets_by_access_level(database)

    def introduce(self):
        """Returns a the description of this beacon, with the fields required by the / endpoint"""

        beacon_obj = self.__dict__
        beacon_obj.pop("datasets_by_auth_level")
        return beacon_obj

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
        for ds in datasets:
            if ds.get("samples") is not None:
                # return number of samples for each dataset, not sample names
                ds["sampleCount"] = len(ds.get("samples"))
            ds.pop("samples", None)
            ds["info"] = {"accessType": ds["authlevel"].upper()},
            ds.pop("authlevel")
            ds["id"] = ds["_id"]

            ds.pop("_id")
        return datasets

    def _datasets_by_access_level(self, database):
        """Retrieve all datasets associated to this Beacon, by access level

        Accepts:
            database(pymongo.database.Database)
        Returns:
            datasets_by_level(dict): the keys are "public", "registered", "controlled"
        """
        datasets_by_level = dict(public={}, registered={}, controlled={})

        if database is None:
            return datasets_by_level

        datasets = database["dataset"].find()
        for ds in list(datasets):
            # add dataset as id=dataset_id, value=dataset to the dataset category
            datasets_by_level[ds["authlevel"]][ds["_id"]] = ds

        return datasets_by_level

    def _sample_allele_requests(self):
        """Returns a list of example allele requests"""

        return []
