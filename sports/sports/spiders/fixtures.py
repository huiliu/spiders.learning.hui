# -*- coding: utf-8 -*-

# ------------------------------------------------
# 从腾讯网站
# 1.    抓取足球联赛赛程信息，对于历史赛事包含比赛结果
# 2.    提取俱乐部列表
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

PersistDb = PersistMongo.Persist(dbcfg)

class JsonQqSpider(scrapy.Spider):
    name = "fixtures"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = (
        # 英超
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2010-08-14&compid=8',
        # 德甲
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2010-08-21&compid=22',
        # 意甲
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2010-08-29&compid=21',
        # 法甲
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2010-08-08&compid=24',
        # 西甲
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2010-08-29&compid=23',
        # 中超
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2012-03-10&compid=208',
        # 欧联
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2014-09-19&compid=6',
        # 欧冠
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2010-09-15&compid=5',
        # 亚冠
        'http://soccerdata.sports.qq.com/s/fixture/list.action?time=2013-02-26&compid=605',
    )
    url_tpl = 'http://soccerdata.sports.qq.com/s/fixture/list.action?time=%s&compid=%s'

    clubs_id = list()


    def parse(self, response):
        null = None
        body = eval(response.body)
        fixture_list = list()
        club_list = list()

        # 处理赛程信息
        for item in body['fixtureList']['tlist']:
            item['date'] = body['time']
            fixture_list.append(item)

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
            yield scrapy.Request(self.url_tpl % (row['date'], body['compid']))
