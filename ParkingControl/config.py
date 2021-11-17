import os

class Production:
    DEBUG = False
    SECRET_KEY = os.urandom(32)
    TIMEZONE = "Asia/Seoul"
    DB_PASS = "1121"
    DB_NAME = "CAR_STAT" 
    DB_HOST = "localhost"
    DB_USER = "root"

class Dev:
    DEBUG = True
    SECRET_KEY = "1234"
    TIMEZONE = "Asia/Seoul"
    DB_PASS = "1121"
    DB_NAME = "CAR_STAT" 
    DB_HOST = "localhost"
    DB_USER = "root"