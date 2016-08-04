# -*- coding: utf-8 -*-

# ------------------------------------------------
# 从英超官网http://www.premierleague.com
# 1.    抓取足球联赛赛程信息
# ------------------------------------------------
import scrapy
import PersistMongo

# TODO:
#   更新数据库相关信息
dbcfg = {
            'host': '10.1.0.6',
            'port': 27017,
            'db': 'football'
        }

#PersistDb = PersistMongo.Persist(dbcfg)

class JsonQqSpider(scrapy.Spider):
    name = "pulselive"
    allowed_domains = ["footballapi.pulselive.com"]
    start_urls = (
        # 英超
        'http://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=54&page=1&pageSize=40&statuses=U,L&altIds=true',
    )

    clubs_id = list()
    headers = {
            'Origin': 'http://www.premierleague.com',
            'Referer': 'http://www.premierleague.com/fixtures'
            }

    def make_requests_from_url(self, url):
        return scrapy.http.Request(url, headers=self.headers, dont_filter=True)

    def parse(self, response):
        false = False
        data = eval(response.body)
        content = data['content']
        print(content[0])
