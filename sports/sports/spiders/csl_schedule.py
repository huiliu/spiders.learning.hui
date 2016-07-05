# -*- coding: utf-8 -*-
# ---------------------------------------------
# 抓取sina.com.cn上的中超赛程
# ---------------------------------------------
import scrapy
import re
import uuid
import datetime
from .persist import PersistentObj

Persist = PersistentObj()

class SinaSpider(scrapy.Spider):
    name = "csl"
    allowed_domains = ["match.sports.sina.com.cn"]
    start_urls = (
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=1&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=2&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=3&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=4&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=5&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=6&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=7&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=8&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=9&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=10&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=11&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=12&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=13&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=14&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=15&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=16&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=17&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=18&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=19&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=20&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=21&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=22&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=23&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=24&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=25&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=26&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=27&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=28&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=29&dpc=1',
            'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_type=208&rnd=30&dpc=1'
    )
    regx = re.compile('.*rnd=([0-9]+)')
    competition_type = u'中超'

    def parse(self, response):
        self.parse_csl_schedules(response)
        pass

    def parse_csl_schedules(self, response):
        """
        抓取中超赛程
        """
        # 开赛时间
        times_xpath = '//p[@class="gl-hd"]/em/text()'
        times = [int(
                datetime.datetime.strptime(record, '%Y-%m-%d %H:%M').strftime('%s')
                    ) for record in response.xpath(times_xpath).extract()
                ]

        address_xpath = '//p[@class="gl-info"]/text()'
        addrs = response.xpath(address_xpath).extract()
        # 球场
        fields = []
        for i in range(0, len(addrs)/2):
            football_field = addrs[2*i + 1].strip().lstrip(u'球场：')
            fields.append(football_field)

        teams_xpath = '//p[@class="gl-teams"]'

        host_team_xpath = './/a[@class="gl-host"]/span/text()'
        guest_team_xpath = './/a[@class="gl-guest"]/span/text()'
        score_xpath = './/span[@class="gl-score"]/a//text()'

        host_team = []
        guest_team = []
        score = []
        for teams in response.xpath(teams_xpath):
            host = ''.join(teams.xpath(host_team_xpath).extract()).strip()
            host_team.append(host)

            guest = ''.join(teams.xpath(guest_team_xpath).extract()).strip()
            guest_team.append(guest)

            s = ''.join(teams.xpath(score_xpath).extract()).strip()
            score.append(s)

        # 轮数
        rand = int(''.join(self.regx.match(response.url).groups()))
        data = []
        for t, host, s, guest, addr in zip(times, host_team, score,
                guest_team, fields):
            uid = uuid.uuid1()
            data.append([
                    uid,
                    self.competition_type,
                    rand,
                    t,
                    host,
                    s,
                    guest,
                    "",
                    response.url
                ])
        Persist.InsertComptitionSchedules(data)
