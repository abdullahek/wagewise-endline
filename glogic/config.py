import os
import urllib.parse
import pyodbc
# noinspection PyUnresolvedReferences


server = os.environ.get('SERVER')
database = os.environ.get('DATABASE')
username = os.environ.get('NAME')
password = os.environ.get('PASSWORD')


params = urllib.parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};'
                                  'Server=tcp:gbot-euro-server.database.windows.net,1433;'
                                  'Database=test;'
                                  # 'Trusted_Connection=yes;'
                                  ';UID=myadmin;'
                                  'PWD=pipQe8-sadjej-covcaf')


class MSSQLConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                               os.path.join(basedir, 'test.sqlite'))
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True


config_env_files = {
    'ms': 'glogic.config.MSSQLConfig',
    'test': 'glogic.config.TestConfig'
}
