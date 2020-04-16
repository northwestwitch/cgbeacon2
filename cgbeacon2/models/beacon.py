# -*- coding: utf-8 -*-
from cgbeacon2 import __version__

class Beacon:
    """Represents a general beacon object"""

    def __init__(self, conf_obj, api_version="1.0.0"):
        self.alternativeUrl = conf_obj.get("alternative_url")
        self.apiVersion = f"v{api_version}"
        self.createDateTime = conf_obj.get("created")
        self.datasets = self._datasets()
        self.description = conf_obj.get("description")
        self.id = conf_obj.get("id")
        self.info = conf_obj.get("info")
        self.name = conf_obj.get("name")
        self.organisation = conf_obj.get("organisation")
        self.sampleAlleleRequests = self._sample_allele_requests()
        self.version = f"v{__version__}"
        self.welcomeUrl = conf_obj.get("welcome_url")

    def _datasets(self):
        """Retrieve all datasets associated to this Beacon"""
        return []

    def _sample_allele_requests(self):
        """Return some example allele requests"""
        return []
