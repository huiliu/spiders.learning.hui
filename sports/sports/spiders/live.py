# -*- coding: utf-8 -*-

# ------------------------------------------------
# 抓取足球赛事直播信息
# 从中可以得到球队，球员在当前比赛中的表现，
# 进而可以算得此场赛事中球员的得分
# ------------------------------------------------
import scrapy
import PersistMongo

# TODO:
#   更新数据库相关信息
config = {
            'host': '10.1.0.6',
            'port': 27017,
            'db': 'football',
            'fixture': 'fixtures',  # 赛程collection
            'match': 'mid'          # 比赛详细统计collection
        }

db = PersistMongo.PersistLiveData(config)

class QqLiveSpider(scrapy.Spider):
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
        for match in db.get_fixture_match_id({}):
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
