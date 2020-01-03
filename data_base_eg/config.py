# configuration file
# -*- coding:utf8 -*-

# db logs
MYSQL_IP = 'ci.amiintellect.com'
MYSQL_USER = 'test'
MYSQL_PASS = 'test#6305'
MYSQL_DB = 'ami_ocr_core_dev'
SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASS + '@' \
                          + MYSQL_IP + '/' + MYSQL_DB
# 'sqlite:///cidashboard.db'   # Use SQLite for developing mode only
SQLALCHEMY_TRACK_MODIFICATIONS = False

# debugging
# DEBUG = False
# FLASK_DEBUG = 0

# host IP port
# APP_HOST = 'localhost'
#APP_PORT = 28095

# key for token
# SECRET_KEY = '3d1515ab-c760-4282-953a-31211aa7e2c5'

# 语义模型路径
# SEMANTICS_MODELS_PATH = 'models/'

# OCR数据路径
# OCR_DATA_PATH = './data'
