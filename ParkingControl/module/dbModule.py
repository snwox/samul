import pymysql
import os

if os.getenv("env") == "Dev":
    from config import Dev as CONF
else:
    from config import Production as CONF

class Database():
    def __init__(self):
        self.db = pymysql.connect(host=CONF.DB_HOST,
                                  user=CONF.DB_USER,
                                  password=CONF.DB_PASS,
                                  db=CONF.DB_NAME,
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
 
    def execute(self, query, args={}):
        self.cursor.execute(query, args) 
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
 
    def commit():
        self.db.commit()

