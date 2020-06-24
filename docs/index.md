## What is a Beacon?
Beacons are web-based discovery services for genetic variants. They are useful to know if the dataset present at any institution connected to the beacon network contains a given allele (or genetic variant). Beacons are an efficient way to share valuable genetic information without overly expose genomic data, due to privacy or security issues.

You can find more info on the Beacon Network at this page: [ https://beacon-network.org/#/about ](https://beacon-network.org/#/about). <br>
Beacon API v.1.0 can be found at [this link].(https://github.com/ga4gh-beacon/specification/blob/develop/beacon.md)   


## Purpose
This documentation illustrates how to set up a beacon based on python (>3.6) backend, a Flask server and a Mongodb instance.


## Our idea
This project is under continuous improvement and our ultimate goal would be to update from the currently supported API 1.0 to the new API 2.0. The tool is intended to be ultimately integrated with the [ Scout VCF visualization tool ](https://github.com/Clinical-Genomics/scout) but it's meant to work as well as a standalone. So having Scout installed is not a requirement.


This software was developed by [Clinical Genomics](https://github.com/Clinical-Genomics), Science For Life Laboratory, Stockholm.
