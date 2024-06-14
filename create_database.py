import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='qwerty')
conn.cursor().execute('CREATE DATABASE web11')
conn.close()