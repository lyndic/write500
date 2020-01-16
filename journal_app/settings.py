import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
MAIL_USE_TSL = os.environ.get('MAIL_USE_TSL')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
