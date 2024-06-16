import pymysql
from config import Config

conn = pymysql.connect(host=Config.DATABASE_HOST,
                       user=Config.DATABASE_USER,
                       password=Config.DATABASE_PASSWORD)
conn.cursor().execute('CREATE DATABASE ' + Config.DATABASE_NAME + ' CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
conn.close()
