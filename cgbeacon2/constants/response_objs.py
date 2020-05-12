####### WRONG REQUEST PARAMS #######
NO_MANDATORY_PARAMS = dict(
    errorCode=400,
    errorMessage="Missing one or more mandatory parameters (referenceName, referenceBases, assemblyId)",
)

NO_SECONDARY_PARAMS = dict(
    errorCode=400,
    errorMessage="Either 'alternateBases' or 'variantType' param is required",
)

NO_POSITION_PARAMS = dict(
    errorCode=400,
    errorMessage="Start coordinate or range coordinate params are required",
)

NO_SV_END_PARAM = dict(
    errorCode=400,
    errorMessage="Structural variants query requires an 'end' coordinate param",
)

INVALID_COORDINATES = dict(
    errorCode=400,
    errorMessage="invalid coordinates. Variant start and stop positions must be numbers",
)

INVALID_COORD_RANGE = dict(
    errorCode=400,
    errorMessage="invalid coordinate range: startMin <= startMax <= endMin <= endMax",
)

BUILD_MISMATCH = dict(
    errorCode=400,
    errorMessage="Requested genome assembly is in conflict with the assembly of one or more requested datasets",
)

####### WRONG HEADERS OBJS #######
MISSING_TOKEN = dict(errorCode=401, errorMessage="Missing authentication token")

WRONG_SCHEME = dict(errorCode=401, errorMessage="Bearer token scheme required")

####### QUERY PARAMS #######
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
    "includeDatasetResponses",
]
