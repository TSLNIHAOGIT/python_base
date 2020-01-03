# encoding: utf-8
import sys
import time
from os.path import abspath, dirname
sys.path.insert(0, abspath(dirname(__file__)))
import config
import pymysql
from app_logging import logger


"""SQLsetting"""
host_name = config.MYSQL_IP
user_name = config.MYSQL_USER
password = config.MYSQL_PASS
database = config.MYSQL_DB
charset = 'utf8'


class readData():
    def __init__(self, companyName=None, ticket=None):
        start_time = time.time()

        self.db = pymysql.connect(host=host_name, user=user_name, password=password,
                                  db=database, charset=charset)
        self.cur = self.db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        self.cur.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = self.cur.fetchall()

        print("Database version : %s " % data)


        self.db.close()
        cost_time = time.time() - start_time
        logger.info(' time cost:%ss' % ( round(cost_time,3)))



if __name__ == '__main__':
    rd = readData('/英业达（重庆）有限公司/1547714126018')

