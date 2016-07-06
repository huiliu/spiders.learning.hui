# -*- coding: utf-8 -*-

# ------------------------------------------------
# 抓取赛事直播信息
# ------------------------------------------------
import scrapy
import pymongo
import MySQLdb


class DB:
    def __init__(self):
        self.client = pymongo.MongoClient('10.1.0.6', 27017)
        self.live_collection = self.client['football'].get_collection('mid')

    def InsertLive(self, data):
        """
            插入赛程信息
        """
        if isinstance(data, dict):
            self.live_collection.insert_one(data)

    def check_downloaded(self, mid):
        result = self.live_collection.find_one({'mid': str(mid)}, {'mid': 1})
        if result:
            # 已经下载
            return True
        else:
            return False
        pass

db = DB()

class JsonQqSpider(scrapy.Spider):
    name = "live"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = (
        'http://soccerdata.sports.qq.com/s/live.action?mid=810614',
    )
    url_tpl = 'http://soccerdata.sports.qq.com/s/live.action?mid=%d'

    def __init__(self):
        conn = MySQLdb.connect(
                    host='10.1.0.6',
                    user='viivgame',
                    passwd='viivgame',
                    db='football',
                    charset='utf8'
                )
        sql = "SELECT id FROM fixtures"
        cursor = conn.cursor()
        cursor.execute(sql)
        urls = []
        for compid in cursor.fetchall():
            url = self.url_tpl % compid[0]
            if db.check_downloaded(compid[0]):
                urls.append(url)

        self.start_urls = set(urls)

        conn.close()

    def parse(self, response):
        """
        """
        if 200 != response.status:
            return

        null = None
        try:
            data = eval(response.body)
            db.InsertLive(data)
        except Exception as e:
            print(e)
            print(data)
