# -*- coding: utf-8 -*-

# ------------------------------------------------
# 从腾讯看比赛网站
# 1.    2016/2017赛季足球比赛赛程
# ------------------------------------------------
import scrapy
import PersistMongo

# TODO:
#   更新数据库相关信息
dbcfg = {
            'host': '10.1.0.6',
            'port': 27017,
            'db': 'football_2017'
        }

PersistDb = PersistMongo.Persist(dbcfg)

class JsonQqSpider(scrapy.Spider):
    name = "2017"
    allowed_domains = ["matchweb.sports.qq.com"]
    start_urls = (
        # 英超
        'http://matchweb.sports.qq.com/kbs/list?columnId=8&startTime=2016-08-13&endTime=2016-12-12&_=1469062693908',
        'http://matchweb.sports.qq.com/kbs/list?columnId=8&startTime=2016-12-13&endTime=2017-03-12&_=1469062693908',
        'http://matchweb.sports.qq.com/kbs/list?columnId=8&startTime=2017-03-13&endTime=2017-06-14&_=1469062693908',
        # 法甲
        'http://matchweb.sports.qq.com/kbs/list?columnId=24&startTime=2016-08-13&endTime=2016-12-12&_=1469062693908',
        'http://matchweb.sports.qq.com/kbs/list?columnId=24&startTime=2016-12-13&endTime=2017-03-12&_=1469062693908',
        'http://matchweb.sports.qq.com/kbs/list?columnId=24&startTime=2017-03-13&endTime=2017-06-14&_=1469062693908',
        # 德甲
        'http://matchweb.sports.qq.com/kbs/list?columnId=22&startTime=2016-08-13&endTime=2016-12-12&_=1469062693908',
        'http://matchweb.sports.qq.com/kbs/list?columnId=22&startTime=2016-12-13&endTime=2017-03-12&_=1469062693908',
        'http://matchweb.sports.qq.com/kbs/list?columnId=22&startTime=2017-03-13&endTime=2017-06-14&_=1469062693908',
        # 西甲
        'http://matchweb.sports.qq.com/kbs/list?columnId=23&startTime=2016-08-13&endTime=2016-12-12&_=1469062693908',
        'http://matchweb.sports.qq.com/kbs/list?columnId=23&startTime=2016-12-13&endTime=2017-03-12&_=1469062693908',
        'http://matchweb.sports.qq.com/kbs/list?columnId=23&startTime=2017-03-13&endTime=2017-06-14&_=1469062693908',
    )

    clubs_id = list()


    def parse(self, response):
        null = None
        body = eval(response.body)

        data = body['data']

        fixtures = list()
        for k, v in data.items():
            for fixture in v:
                if fixture:
                    fixtures.append(fixture)

        if fixtures:
            PersistDb.insert_many('fixtures', fixtures)
