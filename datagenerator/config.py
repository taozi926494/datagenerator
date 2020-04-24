import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'mysql://root:1030617785@127.0.0.1:3306/datagenerator'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@172.16.119.6:3306/datagenerator'
SQLALCHEMY_POOL_RECYCLE = -1
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 2
CSRF_ENABLED = True
