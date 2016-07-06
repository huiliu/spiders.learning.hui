# -*- coding: utf-8 -*-

# ------------------------------------------------
# 抓取联赛赛程信息
# ------------------------------------------------
import scrapy
import MySQLdb
import datetime
import re


class CleanDb:
    def __init__(self):
        self.connection = MySQLdb.connect(
                    host='10.1.0.6',
                    user='viivgame',
                    passwd='viivgame',
                    db='football',
                    charset='utf8'
                )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def InsertFixtures(self, data, dt, url):
        """
            插入赛程信息
        """
        SQL_Template = """INSERT INTO fixtures (
                            id,
                            type,
                            season,
                            round,
                            start_time,
                            home_id,
                            away_id,
                            ground,
                            url
                        ) VALUES (
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            '%s',
                            '%s'
                        )"""

        sql = ""
        for row in data:
            try:
                kickoff = datetime.datetime.strptime("%s %s" % (dt, row['time']), '%Y-%m-%d %H:%M').strftime("%s")
                sql = SQL_Template % (
                            int(row['id']),
                            int(row['compid']),
                            int(row['season']),
                            int(row['round']),
                            int(kickoff),
                            int(row['homeid'].lstrip('t')),
                            int(row['awayid'].lstrip('t')),
                            "",
                            url
                        )
                self.cursor.execute(sql)
            except Exception as e:
                print(e)
                print(sql)

        self.connection.commit()

    def InsertClubInfo(self, team_id, team_name, compid):
        """
            插入俱乐部信息
        """
        SQL_Template = """
                        INSERT INTO clubs (
                            id,
                            name,
                            union_type
                        ) VALUES (
                            %d,
                            '%s',
                            %d
                        )
                       """
        sql = ""
        try:
            sql = SQL_Template % (int(team_id.lstrip('t')), team_name, int(compid))
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            print(sql)
        self.connection.commit()

db = CleanDb()

class JsonQqSpider(scrapy.Spider):
    name = "json.qq"
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
    url_tpl = 'http://soccerdata.sports.qq.com/s/fixture/list.action?time=%s&compid=%d'

    clubs = dict()

    def parse(self, response):
        null = None
        data = eval(response.body)

        compid = int(data['compid'])

        file_name = "%s_%d" % (data['time'], compid)
        with open(file_name, 'a') as fd:
            fd.write(response.body)

        fixtures = data['fixtureList']['tlist']
        db.InsertFixtures(fixtures, data['time'], response.url)

        if compid not in (5,6,605):
            self.parse_club_info(fixtures)

        for row in data['fixtureTimeList']['timelist']:
            yield scrapy.Request(self.url_tpl % (row['date'], compid))

    def parse_club_info(self, data):
        for row in data:
            tid = row['homeid']
            tname = row['homename']
            if tid not in self.clubs:
                db.InsertClubInfo(tid, tname, row['compid'])
                self.clubs[tid] = tname
