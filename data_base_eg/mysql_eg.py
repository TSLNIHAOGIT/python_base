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
        self.companyName = companyName
        self.ticket = ticket
        self.db = pymysql.connect(host=host_name, user=user_name, password=password,
                                  db=database, charset=charset)
        self.cur = self.db.cursor()
        self.company_name = self.__company_name()  # 用户查询配置数据
        self.file_type = self.__file_type()
        self.key_data = self.__key_set()
        self.filed_data = self.__table_filed()
        self.airport_data = self.__dim_airport()
        self.db.close()
        cost_time = time.time() - start_time
        logger.info('[ticket:%s] company_name:%s, time cost:%ss' % (self.ticket, self.company_name, round(cost_time,3)))

    # 公司名称
    def __company_name(self):
        # start_time = time.time()
        sql = 'SELECT GROUP_CONCAT(DISTINCT company_name)as company_name from ocr_key_set_config'
        self.cur.execute(sql)
        results = self.cur.fetchall()[0][0].split(',')
        # cost_time = time.time() - start_time
        # logger.info('[ticket:%s] company_results:%s, time cost:%ss' % (self.ticket, results, round(cost_time,3)))
        if self.companyName:
            tmp = [i for i in results if i in self.companyName and i]
        else:
            tmp = ''
        company_name = tmp[0] if sorted(tmp, key=lambda x: -len(x)) else ''
        return company_name

    # 关键词对应的文件类型数据
    def __file_type(self):
        dynamic_sql = 'company_name="%s"' % self.company_name if self.company_name else 1
        sql = '''
        SELECT key_word,map_name,min(IFNULL(x_min,0))as x_min,
        max(IFNULL(x_max,9999))as x_max,min(IFNULL(y_min,0))as y_min,
        max(IFNULL(y_max,9999))as y_max
        from ocr_key_set_config
        where keyword_type=2 and %s
        group by key_word,map_name
        ''' % dynamic_sql
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results

    # 填表所需的关键词
    def __key_set(self):
        company_total = 0
        if self.company_name:
            total_sql = 'select count(*) as total from ocr_key_set_config where company_name="%s"' % self.company_name
            self.cur.execute(total_sql)
            company_total = self.cur.fetchall()[0][0]
        if company_total > 0:
            sql = '''
            SELECT company_name,file_type,file_name,key_word,map_name,regular_expression,type,
            content_position,number,start_position,aligned,x_min,x_max,y_min,
            y_max,content_max,content_rule,key_position from ocr_key_set_config
            where keyword_type=1 and company_name="{0}"
            UNION
            SELECT "{0}" as company_name,file_type,file_name,key_word,map_name,regular_expression,
            type,content_position,number,start_position,aligned,x_min,x_max,y_min,
            y_max,content_max,content_rule,key_position from ocr_key_set_config
            where keyword_type=1
            and file_type not in (
            SELECT DISTINCT file_type from ocr_key_set_config where keyword_type=1 and company_name="{0}")
            ''' .format(self.company_name)
        else:
            sql = '''
            SELECT "%s" as company_name,file_type,file_name,key_word,map_name,regular_expression,type
            ,content_position,max(number)as number,min(start_position)as start_position,
            ''as aligned,min(x_min)as x_min,max(x_max)as x_max,min(y_min)as y_min, max(y_max)as y_maxs,
            max(content_max) as content_max,GROUP_CONCAT(DISTINCT content_rule) as content_rule,
            max(key_position) as key_position
            from ocr_key_set_config
            where keyword_type=1
            GROUP BY file_type,file_name,key_word,map_name,regular_expression,type,content_position
            ''' % self.company_name
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results

    def __table_filed(self):
        sql = """SELECT DISTINCT type, map_name from ocr_key_set_config
        where keyword_type=1 and type<>'' and map_name<>''"""
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results

    def __dim_airport(self):
        sql = """SELECT DISTINCT REPLACE(three_code,' ','')as three_code from dim_airport
                UNION
                SELECT DISTINCT three_code from dim_airport_foreign
        """
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results


if __name__ == '__main__':
    rd = readData('/英业达（重庆）有限公司/1547714126018')
    print(rd.company_name)
    print(rd.key_data)
