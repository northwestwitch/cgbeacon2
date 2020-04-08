#Turns on debugging features in Flask
DEBUG = True

#secret key:
SECRET_KEY = 'MySuperSecretKey'

ORGANISATION = dict(
    id = "scilifelab", # mandatory
    name = "Clinical Genomics, SciLifeLab", # mandatory
    description = "A science lab",
    address = "",
    contactUrl = "",
    info = [],
    logoUrl = "",
    welcomeUrl = "",
)

BEACON_OBJ = dict(
    id = "sciLifeLab-beacon", # mandatory
    name = "SciLifeLab Stockholm Beacon", # mandatory
    organisation = ORGANISATION, # mandatory
    alternativeUrl = "http//scilifelab.beacon_alt.se",
    createDateTime = "2015-06-15T00:00.000Z",
    description = "Beacon description",
    info = [],
    welcomeUrl = "http//scilifelab.beacon.se",
)
