# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from spider.spider import subject


def closeConn(cursor, conn):
    # 关闭游标
    if cursor:
        cursor.close()
    # 关闭数据库连接
    if conn:
        conn.close()


def getDbConn():
    conn = MySQLdb.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='a123',
        db='bs',
        charset='utf8'
    )
    return conn


class QuestionPipeline(object):
    def __init__(self):
        self.create()
        self.ids_seen = set()

    def process_item(self, item, spider):

        self.insert(item)
        return item

    def create(self):
        # 根据subject名字来创建表
        conn = getDbConn()
        cursor = conn.cursor()
        sqlD = "DROP TABLE IF EXISTS " + subject
        cursor.execute(sqlD)
        sqlC = "CREATE TABLE " + subject + "(`ques` varchar(2000),`quesImage` varchar(2000),`answer_url` varchar(200)," \
            "`answer` varchar(2000),`analyze` varchar(2000),`awImage` varchar(200))"
        cursor.execute(sqlC)
        conn.commit()
        closeConn(cursor, conn)

    def insert(self, item):

        # 获取连接
        conn = getDbConn()
        # 获取游标
        cursor = conn.cursor()
        # 插入数据库
        # 加入`反引号才不报1064语法错误

        sql = "INSERT INTO " + subject + \
            "(`ques`,`quesImage`,`answer_url`,`answer`,`analyze`,`awImage`)VALUES(%s,%s,%s,%s,%s,%s)"
        print("SQLInsert:" + sql)
        params = (
            item['ques'],
            item['quesImage'],
            item['answer_url'],
            item['answer'],
            item['analyze'],
            item['awImage'])
        cursor.execute(sql, params)

        conn.commit()
        closeConn(cursor, conn)
        # except Exception as e:
        #     # 事务回滚
        #     conn.rollback()
        #     print 'except:', e.message
        # finally:
        #     # 关闭游标和数据库连接
        #     closeConn(cursor, conn)
