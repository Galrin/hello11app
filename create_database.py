import pymysql
from config import Config

conn = pymysql.connect(host=Config.DATABASE_HOST,
                       user=Config.DATABASE_USER,
                       password=Config.DATABASE_PASSWORD)
conn.cursor().execute('CREATE DATABASE ' + Config.DATABASE_NAME)
conn.close()
