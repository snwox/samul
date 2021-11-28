import os

class Production:
    DEBUG = False
    SECRET_KEY = os.urandom(32)
    TIMEZONE = "Asia/Seoul"
    DB_PASS = "*7FFBD13EA553B19BE959C4980AA0417D021EF52B"
    DB_NAME = "carmanager" 
    DB_HOST = "localhost"
    DB_USER = "root"

class Dev:
    DEBUG = True
    SECRET_KEY = "1234"
    TIMEZONE = "Asia/Seoul"
    DB_PASS = "*7FFBD13EA553B19BE959C4980AA0417D021EF52B"
    DB_NAME = "carmanager" 
    DB_HOST = "localhost"
    DB_USER =   "root"