# -*- coding: utf-8 -*-

# ------------------------------------------------
# 抓取足球赛事直播信息
# 从中可以得到球队，球员在当前比赛中的表现，
# 进而可以算得此场赛事中球员的得分
#
#   默认抓取明后天的比赛的结果
#
# usage:
#       scrapy crawl live [-a mid=847873]
#   抓取指定比赛的直接数据
#
# ------------------------------------------------
import scrapy
import PersistMongo
import datetime
from addons import calc_core
from addons import score_rules

# TODO:
#   更新数据库相关信息
config = {
            'host': '10.1.0.6',
            'port': 27017,
            'db': 'football',
            'fixture': 'fixtures',                      # 赛程collection
            'match': 'mid',                             # 比赛详细统计collection
            'players_score': 'players_score',           # 存放球员得分
            'players_template': 'players_template'      # 球员模板表
        }

db = PersistMongo.Persist(config)

class QqLiveSpider(scrapy.Spider):
    name = "live"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = (
        'http://soccerdata.sports.qq.com/s/live.action?mid=810614',
    )
    # URL模板，%d比赛ID
    url_tpl = 'http://soccerdata.sports.qq.com/s/live.action?mid=%s'

    def __init__(self, mid=None):
        urls = []
        if mid:
            # 查询指定的比赛
            urls.append(self.url_tpl % str(mid))
            #self.start_urls = set([url])
        else:
            # 查询赛程表中昨天的比赛
            now = datetime.datetime.today()
            delta_day = datetime.timedelta(1)

            condition = dict()
            condition['date'] = (now - delta_day).strftime("%Y-%m-%d")

            Filter = {'_id': 0, 'id': 1}
            for match in db.get_record(config['fixture'], condition, Filter):
                #if match['id'] not in match_ids:
                urls.append(self.url_tpl % match['id'])

        self.start_urls = set(urls)

    def parse(self, response):
        """
        """
        null = None
        try:
            data = eval(response.body)
            db.insert_one(config['match'], data)

            Calc = calc_core.FootballCalc(score_rules.NormalScoreRule())
            players_score, players_template = Calc.calc_one_match(data)
            db.insert_many(config['players_score'], players_score)
            db.insert_many(config['players_template'], players_template)
        except Exception as e:
            print(e, data['mid'])
