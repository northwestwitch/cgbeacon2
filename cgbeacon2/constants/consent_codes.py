CONSENT_CODES = dict(
    NRES = dict(
        abbr = "NRES",
        name = "No restrictions",
        description = "No restrictions on data use",
        free_text = False
    ),
    GRU = dict(
        abbr = "GRU(CC)",
        name = "general research use and clinical care",
        description = "For health/medical/biomedical purposes and other biological research, including the study of population origins or ancestry.",
        free_text = False
    ),
    HMB = dict(
        abbr = "HMB(CC)",
        name = "health/medical/biomedical research and clinical care",
        description = "Use of the data is limited to health/medical/biomedical purposes, does not include the study of population origins or ancestry.",
        free_text = False
    ),
    DS = dict(
        abbr = "DS-[XX](CC)",
        name = "disease-specific research and clinical care",
        description = "Use of the data is limited to health/medical/biomedical purposes, does not include the study of population origins or ancestry.",
        free_text = True
    ),
    POA = dict(
        abbr = "POA",
        name = "population origins/ancestry research",
        description = "Use of the data is limited to the study of population origins or ancestry.",
        free_text = False
    ),
    RS = dict(
        abbr = "RS-[XX]",
        name = "other research-specific restrictions",
        description = "Use of the data is limited to studies of [research type] (e.g., pediatric research).",
        free_text = True
    ),
    RUO = dict(
        abbr = "RUO",
        name = "research use only",
        description = "Use of data is limited to research purposes (e.g., does not include its use in clinical care).",
        free_text = False
    ),
    NMDS = dict(
        abbr = "NMDS",
        name = "no 'general methods' research",
        description = "Use of the data includes methods development research (e.g., development of software or algorithms) ONLY within the bounds of other data use limitations.",
        free_text = False
    ),
    GSO = dict(
        abbr = "GSO",
        name = "genetic studies only",
        description = "Use of the data is limited to genetic studies only (i.e., no research using only the phenotype data).",
        free_text = False
    ),
    NPU = dict(
        abbr = "NPU",
        name = "not-for-profit use only",
        description = "Use of the data is limited to not-for-profit organizations.",
        free_text = False
    ),
    PUB = dict(
        abbr = "PUB",
        name = "publication required",
        description = "Requestor agrees to make results of studies using the data available to the larger scientific community.",
        free_text = False
    ),
    COL = dict(
        abbr = "COL-[XX]",
        name = "collaboration required",
        description = "Requestor must agree to collaboration with the primary study investigator(s).",
        free_text = True
    ),
    RTN = dict(
        abbr = "RTN",
        name = "return data to database/resource",
        description = "Requestor must return derived/enriched data to the database/resource.",
        free_text = False
    ),
    IRB = dict(
        abbr = "IRB",
        name = "ethics approval required",
        description = "Requestor must provide documentation of local IRB/REC approval.",
        free_text = False
    ),
    GS = dict(
        abbr = "GS-[XX]",
        name = "geographical restrictions",
        description = "Use of the data is limited to within [geographic region].",
        free_text = True
    ),
    MOR = dict(
        abbr = "MOR-[XX]",
        name = "publication moratorium/embargo",
        description = "Requestor agrees not to publish results of studies until [date].",
        free_text = True
    ),
    TS = dict(
        abbr = "TS-[XX]",
        name = "time limits on use",
        description = "Use of data is approved for [x months].",
        free_text = True
    ),
    US = dict(
        abbr = "US",
        name = "user-specific restrictions",
        description = "Use of data is limited to use by approved users.",
        free_text = False
    ),
    PS = dict(
        abbr = "PS",
        name = "project-specific restrictions",
        description = "Use of data is limited to use within an approved project.",
        free_text = False
    ),
    IS = dict(
        abbr = "IS",
        name = "institution-specific restrictions",
        description = "Use of data is limited to use within an approved institution.",
        free_text = False
    ),
)
