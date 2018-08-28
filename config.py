"""Configuration file."""


class Config(object):
    """Main config class for the project."""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DATABASE_USER = "interview"
    DATABASE_PWD = "uo4uu3AeF3"
    POSTGRES = {
        'user': DATABASE_USER,
        'pw': DATABASE_PWD,
        'db': 'suade',
        'host': 'candidate.suade.org',
        'port': '5432',
    }
    CONN_STRING = "host='%(host)s' dbname='%(db)s' user='%(user)s' password='%(pw)s'" % POSTGRES
    # CONN_STRING = CONN_STRING
    SUPPORTED_FORMAT = ['xml', 'pdf', 'json']
    SUPPORTED_CONTENT_TYPE = ['text/xml', 'application/pdf', 'application/json']


class ProductionConfig(Config):
    """Production config."""

    DEBUG = False


class StagingConfig(Config):
    """Staging config."""

    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Dev config."""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Test config."""

    TESTING = True
    # # Default timeout is 5 seconds
    # LIVESERVER_TIMEOUT = 10
    # # Set to 0 to have the OS pick the port
    # LIVESERVER_PORT = 8943
