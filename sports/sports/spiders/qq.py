# -*- coding: utf-8 -*-
from __future__ import print_function
import scrapy
from sports.items import SeasonData
import copy


extract_data = lambda response, xpath : [x.strip() for x in response.xpath(xpath).extract()]

class QqSpider(scrapy.Spider):
    name = "qq"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = (
        'http://soccerdata.sports.qq.com/team/1.htm',
    )

    def parse(self, response):
        season_xpath = '//div[@class="set-t"]/span/text()'

        for season in response.xpath(season_xpath).extract():
            #print(u"====================%s赛季球队总数据=====================" % season)
            #self.parse_team_season_sum_data(response, season)
            #print(u"===================%s赛季球队单场数据====================" % season)
            #self.parse_team_season_detail_data(response, season)
            print(u"===================%s赛季个人总数据====================" % season)
            self.parse_player_season_sum_data(response, season)

    def parse_team_season_sum_data(self, response, season):
        """
        解析球队赛季总数据

        球队常规数据11列；进攻数据9列；防守数据9列
        """
        team_normal_title_xpath = '//table[@id="%s-al1"]/tr[@class="a1"]/td/text()' % season
        team_normal_xpath = '//table[@id="%s-al1"]/tr[@class="a2"]/td/text()' % season
        team_attack_title_xpath = '//table[@id="%s-al2"]/tr[@class="a1"]/td/text()' % season
        team_attack_xpath = '//table[@id="%s-al2"]/tr[@class="a2"]/td/text()' % season
        team_defense_title_xpath = '//table[@id="%s-al3"]/tr[@class="a1"]/td/text()' % season
        team_defense_xpath = '//table[@id="%s-al3"]/tr[@class="a2"]/td/text()' % season

        #print("XPATH:\t", team_normal_xpath)
        data = SeasonData()

        normal_title = extract_data(response, team_normal_title_xpath)
        normal_data = extract_data(response, team_normal_xpath)
        attack_title = extract_data(response, team_attack_title_xpath)
        attack_data = extract_data(response, team_attack_xpath)
        defense_title = extract_data(response, team_defense_title_xpath)
        defense_data = extract_data(response, team_defense_xpath)

        L = len(normal_data)
        normal_len = len(normal_title)
        attack_len = len(attack_title)
        defense_len = len(defense_title)
        result = []
        title = normal_title + attack_title + defense_title
        print('\t'.join(title))
        for i in range(L/normal_len):
            temp = [normal_data[i*normal_len]]
            temp.extend(normal_data[normal_len*i+1: normal_len*(i+1)])
            temp.extend(attack_data[attack_len*i+1 : attack_len*(i+1)])
            temp.extend(defense_data[defense_len*i+1 : defense_len*(i+1)])
            print('\t'.join(temp))
            #result.append('\t'.join(temp))
        pass

    def parse_team_season_detail_data(self, response, season):
        """
        解析球队赛季单场数据

        赛季单场数据：常规12列；进攻10列；防守10列
        """
        team_normal_title_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div1"]/tr[@class="a1"]/td/text()' % (season, season)

        team_normal_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]' % (season, season)
        text_xpath = './/text()'

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

        for normal, attack, defense in zip(normal_data, attack_data, defense_data):
            print(' '.join(normal + attack[10:] + defense[10:]))

        return

        # 其它球队信息
        print("结果：")
        host_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="t_right"]//a'%season)
        host_team_name = host_team_a.xpath('./text()').extract()
        host_team_href = host_team_a.xpath('./@href').extract()

        print(host_team_name)
        print(host_team_href)

        result_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="a3"]//a'%season)
        result_team_name = result_team_a.xpath('./text()').extract()
        result_team_href = result_team_a.xpath('./@href').extract()
        print(result_team_name)

        guest_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="t_left"]//a'%season)
        guest_team_name = guest_team_a.xpath('./text()').extract()
        guest_team_href = guest_team_a.xpath('./@href').extract()
        print(guest_team_name)

        pass

    def parse_player_season_sum_data(self, response, season):
        """
        解析个人赛季总体数据

        个人赛季汇总数据：常规10；进攻10；防守9
        """
        player_name_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_1"]/tr[@class="a2"]/td[2]/a/text()' % (season, season)
        player_href_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_1"]/tr[@class="a2"]/td[2]/a/@href' % (season, season)

        player_normal_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_1"]/tr[@class="a2"]' % (season, season)
        player_attack_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_2"]/tr[@class="a2"]' % (season, season)
        player_defense_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_3"]/tr[@class="a2"]' % (season, season)

        player_name = extract_data(response, player_name_xpath)
        player_href = extract_data(response, player_href_xpath)
        player_normal_data = []
        for tr in response.xpath(player_normal_xpath):
            player_normal_data.append(extract_data(tr, './/text()'))

        player_attack_data = []
        for tr in response.xpath(player_attack_xpath):
            player_attack_data.append(extract_data(tr, './/text()'))

        player_defense_data = []
        for tr in response.xpath(player_defense_xpath):
            player_defense_data.append(extract_data(tr, './/text()'))

        for normal, attack, defense in zip(player_normal_data, player_attack_data, player_defense_data):
            print(' '.join(normal + attack[8:] + defense[8:]))

        return

        print("球员名字：")
        print('\t'.join(player_name))

        print("球员链接：")
        print('\t'.join(player_href))


        # 守门员数据
        # 12
        goalkeeper_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]/td/text()' % (season, season)
        goalkeeper_name_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]/td[2]/a/text()' % (season, season)
        goalkeeper_href_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]/td[2]/a/@href' % (season, season)

        goalkeeper_data = extract_data(response, goalkeeper_xpath)
        goalkeeper_name = extract_data(response, goalkeeper_name_xpath)
        goalkeeper_href = extract_data(response, goalkeeper_href_xpath)

        print("守门员数据：")
        print('\t'.join(goalkeeper_name))
        print('\t'.join(goalkeeper_href))
        print('\t'.join(goalkeeper_data))
        pass

    def parse_player_season_detail_data(self, response, season):
        """
        解析个人赛季单场数据
        """
