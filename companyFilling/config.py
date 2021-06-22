import os


class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')  # WvGFY145LzM2lu7dP70Xb15kdh8I68lL
    SECRET_KEY = "WvGFY145LzM2lu7dP70Xb15kdh8I68lL"
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # change to other sql database later

    import urllib.parse

    servername = "hspector"
    database = "HSpector"
    username = "hspector"
    password = "Daniel02raptors"

    server = f"{servername}.database.windows.net"

    driver = '{ODBC Driver 13 for SQL Server}'

    #params = urllib.parse.quote_plus(f'DRIVER={driver};SERVER={server}-{password};DATABASE={database};Trusted_Connection=yes;')
    SQLALCHEMY_DATABASE_URI = f"mssql+pymssql://{username}:{password}@{server}/{database}"


    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'danielsplash10'  # change to other a json file later
    MAIL_PASSWORD = 'Daniel02raptors'
