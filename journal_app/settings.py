import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
mail_server = os.environ.get('MAIL_SERVER')
mail_port = os.environ.get('MAIL_PORT')
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
MAIL_USE_TSL = os.environ.get('MAIL_USE_TSL')
mail_username = os.environ.get('MAIL_USERNAME')
mail_password = os.environ.get('MAIL_PASSWORD')
mail_receipt = os.environ.get('MAIL_RECEIPT')
