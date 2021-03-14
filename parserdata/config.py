import os
from dotenv import load_dotenv

load_dotenv()


class Test:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('secret_key')
    USE_RELOADER = False
