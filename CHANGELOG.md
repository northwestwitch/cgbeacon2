## [x.x.x] -

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
