# -*- coding: utf-8 -*-

# ------------------------------------------------
# 从腾讯网站
# 1.    抓取足球联赛赛程信息，对于历史赛事包含比赛结果
# 2.    提取俱乐部列表
# 3.    抓取指定日期之后的某联赛赛程
#       scrapy crawl fixtures -a start_date=2016-07-31 -a match_type=208
# ------------------------------------------------
import scrapy
import PersistMongo
import datetime

# TODO:
#   更新数据库相关信息
dbcfg = {
            'host': '10.1.0.6',
            'port': 27017,
            'db': 'football'
        }

PersistDb = PersistMongo.Persist(dbcfg)

class JsonQqSpider(scrapy.Spider):
    name = "fixtures"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = ()
    url_tpl = 'http://soccerdata.sports.qq.com/s/fixture/list.action?time=%s&compid=%s'
    season_kickoff_date = None
    clubs_id = list()

    def __init__(self, start_date, match_type):
        self.season_kickoff_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        init_url = self.generate_url(start_date, match_type)
        self.start_urls = set([init_url])

    def generate_url(self, start_date, compid):
        d = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        assert self.season_kickoff_date
        # 过虑掉指定日期之前的赛程
        if self.season_kickoff_date and d < self.season_kickoff_date:
            return None
        else:
            return self.url_tpl % (start_date, compid)

    def parse(self, response):
        null = None
        body = eval(response.body)
        fixture_list = list()
        club_list = list()

        # 处理赛程信息
        for item in body['fixtureList']['tlist']:
            item['date'] = body['time']
            fixture_list.append(item)

        # 某天的赛事列表
        if fixture_list:
            PersistDb.insert_many("fixtures", fixture_list)

        # 对于欧冠、欧联、亚冠不记录club
        if body['compid'] not in ('5', '6', '605'):
            
            # 处理俱乐部信息
            for item in body['fixtureList']['tlist']:
                # 只记主场，因为一个赛季所有的球队都会坐阵主场
                tid = item['homeid'].lstrip('t')
                tname = item['homename'].lstrip('t')
                season = item['season']

                if tid not in self.clubs_id:
                    self.clubs_id.append(tid)

                    club_data = dict()
                    club_data['id'] = tid
                    club_data['name'] = tname
                    club_data['season'] = season            #   赛季
                    club_data['compid'] = body['compid']    #   所属联赛
                    club_list.append(club_data)

        if club_list:
            PersistDb.insert_many("clubs", club_list)

        # 迭代其它日期的比赛
        for row in body['fixtureTimeList']['timelist']:
            url = self.generate_url(row['date'], body['compid'])
            if url:
                yield scrapy.Request(url)
