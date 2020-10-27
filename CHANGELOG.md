## [] -

### Fixed
- Broken githut actions test
### Added
- Codecov and CodeFactor github actions
- Created deployment WSGI file
- Cython requirement


## [1.2] - 2020.10.19

### Fixed
- Added an init file inside the demo resources folder
- Accept variants annotated with build GRCh37 and GRCh38 (`chrN`) instead of just `N` (as in hg19)
- Improved calculation of structural variants end coordinates

### Changed
- Renamed SNV and SV demo VCF files
- Coordinate Range queries allowing fuzzy positions

### Added
- Demo VCF file containing BND SV variants
- Save BND variants to database (introduced additional mateName key/values)
- Query BND variants using mateName
- Documentation using `MkDocs`.
- Populate database with genes downloaded from Ensembl Biomart
- Function to create a VCF Bedtool filter from a list of genes HGNC ids or Ensembl ids
- API endpoint to add variants using a POST request
- API endpoint to remove variants using POST request


## [1.1] - 2020.06.17

### Fixed
- Revert to previous code, since cyvcf2 returns 0-based coordinates
- Updated README
- Added missing `requests` lib in requests
- Freezes pysam in requirements file
- Sets pytest requirement to >4.6 because of lack of backward compatibility of new version of pytest-cov
- Remove redundant text from cli docstrings
- Modified colors of 2 big checkboxes in the query form html page

### Added
- Check that all requested samples are in VCF samples before uploading any variant
- Registering events whenever datasets and/or variants are added or removed
- Beacon info endpoint now returns beacon createDateTime and updateDateTime


## [1] - 2020.06.05

### Added
- Info endpoint (/) for API v1
- Add new datasets using the command line
- Update existing datasets using the command line
- Delete a dataset using the command line
- Code to parse VCF files (SNVs) and create Variant objects
- Save SNV variants from parsed VCF files
- Update SNV variants for one or more VCF samples
- Remove variants by providing dataset id and sample name(s)
- Filter VCF files using bed files with genomic intervals
- Query endpoint returns basic response
- Created error messages to handle wrong server requests
- Return responses for SNV queries with datasetAlleleResponses == ALL, HIT, MISS
- Added repository codeowners
- Added tests for queries with datasetAlleleResponses == HIT and MISS
- No conflicts between queried assembly and the assembly or queried datasets
- Parse SVs and save them to database
- Fixed code for range queries and without end position, with tests
- Added test for negative response and introduce error=None if response status code is 200 (success)
- Added simple query interface
- Run queries and display results on the web interface
- Add 3 level of authentication when creating datasets and fix tests accordingly
- Important request/response syntax fixes
- Included OAuth2 JWT validation layer
- Included tests for non-valid auth JWTs
- Stratify returned results by user auth level
- Fixed code that handles POST request content
- Added a function to load demo data into demo database
- Added a short description of the Beacon command and functionalities in the readme file
- Return query examples in the info endpoint
- Do not enforce check of end position in structural variants query
- Zero-based coordinates
- Save variant allele count and return it in datasetAlleleResponses result objects
- Return variantCount in datasetAlleleResponses
- Return dataset access level info in datasetAlleleResponses
- Return datasets callCount and variantCount in info endpoint response
