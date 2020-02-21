import os

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# Flask and some of its extensions use the value of the secret key as a cryptographic key,
# useful to generate signatures or tokens.


class Config(object):
    FLASK_APP = "app"
    FLASK_ENV = "development"
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x955\x7f\x07\xe7\x00\xf7{\x0f\x9a\xafdW\xc7\xdcS'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    DEBUG = 1
