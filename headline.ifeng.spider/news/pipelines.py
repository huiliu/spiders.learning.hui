# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import MySQLdb
from news.dbconfig import DB_CONFIG

class ifengHeadlinePipeline(object):
    def __init__(self):
        self.tblName = "%s.ifengHeadline" % DB_CONFIG['dbName']
        self.conn = MySQLdb.connect(
                                        host=DB_CONFIG['host'],
                                        user=DB_CONFIG['user'],
                                        passwd=DB_CONFIG['passwd'],
                                        db=DB_CONFIG['dbName'],
                                        charset='utf8',
                                        use_unicode=True
                                    )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        """
        """
        if not item['title']: return item
        sql_chk = """SELECT id FROM %s WHERE title = '%s'""" %\
                                                (self.tblName, item['title'])
        self.cur.execute(sql_chk)
        if self.cur.fetchone() is not None: return item

        sql = """INSERT INTO %s (
                                            title,
                                            href,
                                            uptime,
                                            pri
                                ) VALUE (
                                            '%s',
                                            '%s',
                                            '%s',
                                            %d
                                )"""
        # 使用self.execute(sql, ())时一直出错
        self.cur.execute(sql % (
                                self.tblName,
                                item['title'],
                                item['href'],
                                item['uptime'],
                                item['pri']
                                )
                        )
        self.conn.commit()
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.conn.close()
        pass
