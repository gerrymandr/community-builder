import configparser
import pymysql

# Load configuration variables
settings = configparser.ConfigParser()
settings.read(".config")


def get_db_connection():
    return pymysql.connect(host=settings['db']['host'],
                           user=settings['db']['username'],
                           password=settings['db']['password'],
                           db=settings['db']['database'])