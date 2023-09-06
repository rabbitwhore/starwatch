# Development configuration
DEBUG = True
SECRET_KEY = 'AcezuxSystemsDev'
SQLALCHEMY_DATABASE_URI = 'sqlite:///domains.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# config.py

# Flask-Mail Configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'danzpunkten@gmail.com'
MAIL_PASSWORD = 'vwpeporymqdvrkgu'
MAIL_DEFAULT_SENDER = 'danzpunkten@gmail.com'
