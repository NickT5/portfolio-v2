import os


class Config(object):
    FLASK_APP = "run.py"
    FLASK_ENV = "development"
    DEBUG = True

    # Define the application directory.
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Define secret key.
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x955\x7f\x07\xe7\x00\xf7{\x0f\x9a\xafdW\xc7\xdcS'
    
    # Define the database connection.
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/portfolio'  # 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
