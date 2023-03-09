import os
import re
from datetime import timedelta
from decouple import config

base_dir = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config("SECRET_KEY", "secret")
    JWT_SECRET_KEY = config("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)

    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_ECHO = True

    DEFAULT_PASSWORD = config("DEFAULT_PASSWORD")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "db.sqlite3")
    DEBUG = True  


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # for in-memory database


class ProductionConfig(Config):
    
    # uri = config("DATABASE_URL")
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)

    # SQLALCHEMY_DATABASE_URI = uri
    # DEBUG = config("DEBUG", False, cast=bool)
    # SQLALCHEMY_ECHO = False

    pass
    
    

config_dict = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
