# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import MySQLdb

class EnviromentPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
                                        host='localhost',
                                        user='spider',
                                        passwd='spider',
                                        db='spider',
                                        charset='utf8',
                                        use_unicode=True
                                    )
        self.cur = self.conn.cursor()
    def process_item(self, item, spider):
        """
        """
        sql = """INSERT INTO spider.airq VALUE (
                                                            %d,
                                                            '%s',
                                                            '%s',
                                                            %d,
                                                            '%s',
                                                            '%s',
                                                            '%s'
                                                            )"""
        # 使用self.execute(sql, ())时一直出错
        self.cur.execute(sql % (item['id'],
                                item['city_name'],
                                item['date'],
                                item['pollution_id'],
                                item['contamination'],
                                item['qLevel'],
                                item['qState']
                                )
                        )
        self.conn.commit()
        return item
    def open_spider(self, spider):
        pass
    def close_spider(self, spider):
        self.conn.close()
        pass
