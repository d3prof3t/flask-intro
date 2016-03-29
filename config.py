# config.py

# Core Python Imports
import os

# get the absolute path of the current script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """
    DocString
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = '"\xd9\xba\xfcL7+\x13F\xca'
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    """
    DocString
    """

    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    DocString
    """

    DEBUG = False
