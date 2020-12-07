import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # WvGFY145LzM2lu7dP70Xb15kdh8I68lL
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # change to other sql database later
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'danielsplash10'  # change to other a json file later
    MAIL_PASSWORD = 'Daniel02raptors'
