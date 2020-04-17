# Turns on debugging features in Flask
DEBUG = True

# secret key:
SECRET_KEY = "MySuperSecretKey"

# Database connection parameters
DB_USERNAME = "testuser"
DB_PASSWORD = "testpassw"
DB_HOST = "127.0.0.1"
DB_PORT = 27017
DB_NAME = "cgbeacon2"
DB_URI = f"mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}"


ORGANISATION = dict(
    id="scilifelab",  # mandatory
    name="Clinical Genomics, SciLifeLab",  # mandatory
    description="A science lab",
    address="",
    contactUrl="",
    info=[],
    logoUrl="",
    welcomeUrl="",
)

BEACON_OBJ = dict(
    id="sciLifeLab-beacon",  # mandatory
    name="SciLifeLab Stockholm Beacon",  # mandatory
    organisation=ORGANISATION,  # mandatory
    alternativeUrl="http//scilifelab.beacon_alt.se",
    createDateTime="2015-06-15T00:00.000Z",
    description="Beacon description",
    info=[],
    welcomeUrl="http//scilifelab.beacon.se",
)
