# -*- coding: utf-8 -*-

# ------------------------------------------------
# 抓取足球赛事直播信息
# 从中可以得到球队，球员在当前比赛中的表现，
# 进而可以算得此场赛事中球员的得分
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

    def get_fixture_match_id(self):
        cur = self.client['football']['fixtures'].find({}, {'_id': 0, 'id': 1})

        return cur

    def get_downloaded_match_id(self):
        # 赛事实况
        ret = self.live_collection.find({}, {'_id': 0, 'mid': 1})
        matchids = list()
        for item in ret:
            matchids.append(item['mid'])
        return matchids

db = DB()

class JsonQqSpider(scrapy.Spider):
    name = "live"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = (
        'http://soccerdata.sports.qq.com/s/live.action?mid=810614',
    )
    # URL模板，%d比赛ID
    url_tpl = 'http://soccerdata.sports.qq.com/s/live.action?mid=%s'

    def __init__(self):
        urls = []
        match_ids = db.get_downloaded_match_id()
        for match in db.get_fixture_match_id():
            if match['id'] not in match_ids:
                urls.append(self.url_tpl % match['id'])

        return
        self.start_urls = set(urls)

    def parse(self, response):
        """
        """
        null = None
        try:
            data = eval(response.body)
            db.InsertLive(data)
        except Exception as e:
            print(e, data['mid'])
