__author__ = "stefanotuv"

import os


class Config:
    SECRET_KEY = 'stefanotuv'

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://stefano:stefano@localhost/DTSOPS'
    SQLALCHEMY_DATABASE_URI = ''
    user_table = ''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
