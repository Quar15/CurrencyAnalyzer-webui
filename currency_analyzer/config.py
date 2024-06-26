import os
from dotenv import find_dotenv, load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Try to load .env
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['CURRENCY_ANALYZER_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['CURRENCY_ANALYZER_DATABASE_URL']
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True