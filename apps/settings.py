# from secret_keys import CSRF_SECRET_KEY, SESSION_KEY
from datetime import timedelta

class Config(object):	
    # Set secret keys for CSRF protection
    SECRET_KEY = "skadbs123"
    # CSRF_SESSION_KEY = SESSION_KEY
    debug = False
    PERMANENT_SESSION_LIFETIME = timedelta(days = 30)


class Production(Config):
    DEBUG = True
    CSRF_ENABLED = False
    ADMIN = "seafalcon323@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///youngnak?instance=yns-project:project1'
    migration_directory = 'migrations'
