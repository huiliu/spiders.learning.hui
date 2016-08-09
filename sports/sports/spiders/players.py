#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
#
# 抓取每个球队的球员列表
#
# usage:
#       scrapy crawl player [-a tid=1] [-a output=PlayerTemplate.xml]
#
# -a tid=team_id    只抓取指定球队的球员信息
# -a output=PlayerTemplate.xml  输出到文件PlayerTemplate.xml
#
# -----------------------------------------------------------------------------

from __future__ import print_function
import scrapy
from addons import player
from addons import clubs
from addons import enum


class ScrapyFootballPlayer(scrapy.Spider):
    name = "players"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = ()
    url_tpl = 'http://soccerdata.sports.qq.com/team/%d.htm'

    player_xpath = '//div[@id="player-stat-2016"]//table[@id="2016-play_stat_div_1"]/tr[@class="a2"]'
    goalkeeper_xpath = '//div[@id="player-stat-2016"]//table[@id="2016-div1"]/tr[@class="a2"]'

    def __init__(self, tid=None, output="PlayerTemplate.xml"):
        """

        :tid:           如果不为None，抓取指定球队的球员资料；否则抓取赛程表中
                        所有球队的球员信息
        :output:        输出的XML文件名
        """
        self.output = output
        self.entries = []
        urls = list()

        if tid:
            urls.append(self.url_tpl % int(tid))
        else:
            dbconfg = clubs.DBConfig()
            for cid in clubs.get_clubs_id(dbconfg):
                urls.append(self.url_tpl % int(cid)) 

        self.start_urls = set(urls)

    def close(self, reason):
        """爬虫关闭时将玩家数据写到硬盘
        """
        player.export_player_template(self.entries, self.output)
        return super(ScrapyFootballPlayer, self).close(self, reason)

    def parse(self, response):

        www = response.url
        club_id = www.split('/')[-1][:-4]
        players = []
        for row in response.xpath(self.player_xpath):
            p = dict()
            temp_url = row.xpath('./td[2]/a/@href').extract()[0]
            p['id'] = temp_url.split('/')[-1][:-4]
            p['number'] = row.xpath('./td[1]/text()').extract()[0]
            p['name'] = row.xpath('./td[2]/a/text()').extract()[0]
            p['posi'] = row.xpath('./td[3]/text()').extract()[0]

            players.append(p)

        for row in response.xpath(self.goalkeeper_xpath):
            p = dict()
            temp_url = row.xpath('./td[2]/a/@href').extract()[0]
            p['id'] = temp_url.split('/')[-1][:-4]
            p['number'] = row.xpath('./td[1]/text()').extract()[0]
            p['name'] = row.xpath('./td[2]/a/text()').extract()[0]
            p['posi'] = u'门将'

            players.append(p)
        
        # 玩家信息一直保存在内存中直到爬虫关闭才会写入至硬盘
        data = player.generate_player_template_item(players, enum.ST_FOOTBALL)
        self.entries.extend(data)
