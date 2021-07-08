import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    servername = os.environ.get("servername")#"hspector"
    database = os.environ.get("database")
    username = os.environ.get("database_username")
    password = os.environ.get("sql_password")

    server = f"{servername}.database.windows.net"

    driver = '{ODBC Driver 13 for SQL Server}'

    SQLALCHEMY_DATABASE_URI = f"mssql+pymssql://{username}:{password}@{server}/{database}"

    MAIL_SERVER = 'smtp.zoho.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'daniel@hspector.com'
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
