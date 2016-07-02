# -*- coding: utf-8 -*-
from __future__ import print_function
import scrapy
from sports.items import SeasonData
import copy


extract_data = lambda response, xpath : [x.strip() for x in
        response.xpath(xpath).extract() if x.strip()]

class QqSpider(scrapy.Spider):
    name = "player"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = (
        'http://soccerdata.sports.qq.com/player/13017.htm',
        #'http://soccerdata.sports.qq.com/team/1.htm',
        #'http://soccerdata.sports.qq.com/team/164.htm',
    )

    def parse(self, response):
        name_xpath = '//div[@class="mLeftTop"]/h2/text()'
        name = ' '.join(extract_data(response, name_xpath)).strip()
        season_xpath = '//div[@class="set-t"]/span/text()'
        teams = dict()
        for season in response.xpath(season_xpath).extract():
            print(u"====================%s赛季总数据=====================" % season)
            summary = self.parse_season_sum_data(response, season)
            print(u"===================%s赛季单场数据====================" % season)
            detail_data = self.parse_season_detail_data(response, season, teams)

            file_name = '%s_%s.dat' % (name, season)
            with open(file_name.encode('utf-8'), 'a+') as fd:
                for t in summary:
                    temp = ' '.join(t) + '\n'
                    fd.write(temp.encode('utf-8'))
                fd.write('\n')
                # 单场数据
                for competition in detail_data:
                    temp = ' '.join(competition) + '\n'
                    fd.write(temp.encode('utf-8'))

    def parse_season_sum_data(self, response, season):
        """
        解析球队赛季总数据

        球队常规数据11列；进攻数据9列；防守数据9列
        """
        text_xpath = './/td/text()'
        team_normal_title_xpath = '//table[@id="%s-al1"]/tr[@class="a1"]/td/text()' % season
        team_normal_tr_xpath = '//table[@id="%s-al1"]/tr[@class="a2"]' % season
        normal_data = []
        for tr in response.xpath(team_normal_tr_xpath):
            normal_data.append(extract_data(tr, text_xpath))

        team_attack_title_xpath = '//table[@id="%s-al2"]/tr[@class="a1"]/td/text()' % season
        team_attack_tr_xpath = '//table[@id="%s-al2"]/tr[@class="a2"]' % season
        attack_data = []
        for tr in response.xpath(team_attack_tr_xpath):
            attack_data.append(extract_data(tr, text_xpath))

        team_defense_title_xpath = '//table[@id="%s-al3"]/tr[@class="a1"]/td/text()' % season
        team_defense_tr_xpath = '//table[@id="%s-al3"]/tr[@class="a2"]' % season
        defense_data = []
        for tr in response.xpath(team_defense_tr_xpath):
            defense_data.append(extract_data(tr, text_xpath))

        # 球队赛季数据
        summary = []
        for normal, attack, defense in zip(normal_data, attack_data, defense_data):
            print(' '.join(normal + attack[1:] + defense[1:]))
            summary.append(normal + attack[1:] + defense[1:])

        return summary

    def parse_season_detail_data(self, response, season, teams):
        """
        解析球队赛季单场数据

        赛季单场数据：常规12列；进攻10列；防守10列
        """
        team_normal_title_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div1"]/tr[@class="a1"]/td/text()' % (season, season)

        team_normal_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]' % (season, season)
        text_xpath = './/td//text()'

        normal_data = []
        for tr in response.xpath(team_normal_tr_xpath):
            normal_data.append(extract_data(tr, text_xpath))

        team_attack_title_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div2"]/tr[@class="a1"]/td/text()' % (season, season)
        team_attack_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div2"]/tr[@class="a2"]' % (season, season)
        attack_data = []
        for tr in response.xpath(team_attack_tr_xpath):
            attack_data.append(extract_data(tr, text_xpath))

        team_defense_title_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div3"]/tr[@class="a1"]/td/text()' % (season, season)
        team_defense_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div3"]/tr[@class="a2"]' % (season, season)
        defense_data = []
        for tr in response.xpath(team_defense_tr_xpath):
            defense_data.append(extract_data(tr, text_xpath))

        # 其它球队信息
        print("结果：")
        host_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="t_right"]//a'%season)
        host_team_name = host_team_a.xpath('./text()').extract()
        host_team_href = host_team_a.xpath('./@href').extract()

        for name, href in zip(host_team_name, host_team_href):
            if name not in teams:
                teams[name] = href

        result_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="a3"]//a'%season)
        result_team_name = result_team_a.xpath('./text()').extract()
        result_team_href = result_team_a.xpath('./@href').extract()
        #print(result_team_name)

        guest_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="t_left"]//a'%season)
        guest_team_name = guest_team_a.xpath('./text()').extract()
        guest_team_href = guest_team_a.xpath('./@href').extract()

        for name, href in zip(guest_team_name, guest_team_href):
            if name not in teams:
                teams[name] = href

        # 赛季每场比赛的表现
        competitions = []
        for normal, attack, defense in zip(normal_data, attack_data, defense_data):
            print(' '.join(normal + attack[5:] + defense[5:]))
            competitions.append(normal + attack[5:] + defense[5:])

        return competitions

