# Error objects
MISSING_PARAMS_ERROR = dict(
    errorCode=400,
    errorMessage="Missing one or more mandatory parameters (referenceName, referenceBases, assemblyId)"
)

QUERY_PARAMS_API_V1 = [
    "referenceName",
    "referenceBases",
    "assemblyId",
    "start",
    "startMin",
    "startMax",
    "end",
    "endMin",
    "endMax",
    "alternateBases",
    "variantType",
    "includeDatasetResponses"
]
