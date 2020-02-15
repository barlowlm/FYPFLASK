import os


class Config:
    SECRET_KEY = 'ff588184fb63243128123f8b5b89e49b'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
 
    """Use bash config with this"""
    """SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')"""
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')