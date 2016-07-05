# -*- coding: utf-8 -*-
from __future__ import print_function
import scrapy
from sports.items import SeasonData
import uuid
from .persist import PersistentObj
import sys

Persist = PersistentObj()

extract_data = lambda response, xpath : [x.strip() for x in
        response.xpath(xpath).extract() if x.strip()]

iCount = 0

class QqSpider(scrapy.Spider):
    name = "team"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = (
        'http://soccerdata.sports.qq.com/team/1.htm',
        'http://soccerdata.sports.qq.com/player/13017.htm',
        'http://soccerdata.sports.qq.com/player/51940.htm',
    )

    # {url : status}
    teams_url = {
            'http://soccerdata.sports.qq.com/team/1.htm': True
            }
    players_url = {
            'http://soccerdata.sports.qq.com/player/13017.htm' : True,
            'http://soccerdata.sports.qq.com/player/51940.htm' : True,
            }
    def parse(self, response):

        URL = response.url
        print(URL)
        if URL in self.teams_url:
            self.teams_url[URL] = True
        elif URL in self.players_url:
            self.players_url[URL] = True
        else:
            print(URL)
            print(self.teams_url)
            print(self.players_url)
            assert False

        name_xpath = '//div[@class="mLeftTop"]/h2/text()'
        name = ' '.join(extract_data(response, name_xpath))
        season_xpath = '//div[@class="set-t"]/span/text()'

        info = None
        if URL.find('player') != -1:
                info = self.parse_player_info(response)

        for season in response.xpath(season_xpath).extract():
            if response.url.find('team') != -1:
                # 分析球队数据
                #print(u'-------------------------------%s赛季球队信息 -------------------'% season)
                summary = self.parse_team_season_sum_data(response, name, season)
                team_data = self.parse_team_season_detail_data(response, name, season)
                self.parse_player_url(response, season)
            elif response.url.find('player') != -1:
                # 分析球员数据
                #print(u'-------------------------------%s赛季球员信息 -------------------'% season)
                if info[1]:
                    # 守门员
                    #print('守门员！')
                    summary = self.parse_goalkeeper_season_summary(response, info, int(season))
                    team_data = self.parse_goalkeeper_season_detail_data(response, info, int(season))
                else:
                    # 非守门员
                    #print('非守门员！')
                    summary = self.parse_player_season_sum_data(response, info, int(season))
                    team_data = self.parse_player_season_detail_data(response, info, int(season))
            else:
                print(URL)
                assert False

        for url, status in self.teams_url.items():
            if not status:
                print(url)
                yield scrapy.Request(url)

        for url, status in self.players_url.items():
            if not status:
                print(url)
                yield scrapy.Request(url)

    def parse_team_season_sum_data(self, response, name, season):
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
            #print(' '.join(normal + attack[1:] + defense[1:]))
            summary.append(normal + attack[1:] + defense[1:])

        Persist.InsertTeamSeasonSummary(name, season, summary, response.url)

        return summary

    def parse_team_season_detail_data(self, response, host_name, season):
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
        #print("结果：")
        host_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="t_right"]//a'%season)
        #host_team_name = host_team_a.xpath('./text()').extract()
        host_team_href = host_team_a.xpath('./@href').extract()

        for href in host_team_href:
            if href not in self.teams_url:
                self.teams_url[href] = False

        result_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="a3"]//a'%season)
        result_team_name = result_team_a.xpath('./text()').extract()
        result_team_href = result_team_a.xpath('./@href').extract()
        #print(result_team_name)

        guest_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="t_left"]//a'%season)
        #guest_team_name = guest_team_a.xpath('./text()').extract()
        guest_team_href = guest_team_a.xpath('./@href').extract()

        for href in guest_team_href:
            if href not in self.teams_url:
                self.teams_url[href] = False

        # 球队赛季每场比赛的表现
        competitions = []
        for normal, attack, defense in zip(normal_data, attack_data, defense_data):
            #print(' '.join(normal + attack[5:] + defense[5:]))
            competitions.append(normal + attack[5:] + defense[5:])

        Persist.InsertTeamSeasonDetailData(host_name, season, competitions, response.url)

        return competitions


    def parse_player_url(self, response, season):
        """
        """
        player_name_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_1"]/tr[@class="a2"]/td[2]/a/text()' % (season, season)
        player_href_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_1"]/tr[@class="a2"]/td[2]/a/@href' % (season, season)

        goalkeeper_name_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]/td[2]/a/text()' % (season, season)
        goalkeeper_href_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]/td[2]/a/@href' % (season, season)
        #player_name = extract_data(response, player_name_xpath)
        player_href = extract_data(response, player_href_xpath)
        goalkeeper_href = extract_data(response, goalkeeper_href_xpath)

        for href in player_href:
            if href not in self.players_url:
                self.players_url[href] = False
        for href in goalkeeper_href:
            if href not in self.players_url:
                self.players_url[href] = False

    def parse_player_season_sum_data(self, response, info, season):
        """
        解析球员赛季总数据

        球队常规数据11列；进攻数据9列；防守数据9列
        """
        text_xpath = './/td/text()'
        team_normal_tr_xpath = '//table[@id="%s-al1"]/tr[@class="a2"]' % season
        normal_data = []
        for tr in response.xpath(team_normal_tr_xpath):
            normal_data.append(extract_data(tr, text_xpath))

        team_attack_tr_xpath = '//table[@id="%s-al2"]/tr[@class="a2"]' % season
        attack_data = []
        for tr in response.xpath(team_attack_tr_xpath):
            attack_data.append(extract_data(tr, text_xpath))

        team_defense_tr_xpath = '//table[@id="%s-al3"]/tr[@class="a2"]' % season
        defense_data = []
        for tr in response.xpath(team_defense_tr_xpath):
            defense_data.append(extract_data(tr, text_xpath))

        # 球员赛季数据
        summary = []
        for normal, attack, defense in zip(normal_data, attack_data, defense_data):
            #print(' '.join(normal + attack[1:] + defense[1:]))
            summary.append(normal + attack[1:] + defense[1:])

        other_data = {
                'uuid' : info[0],
                'season': season,
                'url': response.url
                }

        Persist.InsertPlayerSeasonSummary(other_data, summary)

        return summary

    def parse_player_season_detail_data(self, response, info, season):
        """
        解析球员赛季单场数据

        赛季单场数据：常规12列；进攻10列；防守10列
        """
        teams = dict()

        team_normal_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]' % (season, season)
        text_xpath = './/td//text()'

        normal_data = []
        for tr in response.xpath(team_normal_tr_xpath):
            normal_data.append(extract_data(tr, text_xpath))

        team_attack_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div2"]/tr[@class="a2"]' % (season, season)
        attack_data = []
        for tr in response.xpath(team_attack_tr_xpath):
            attack_data.append(extract_data(tr, text_xpath))

        team_defense_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="%s-div3"]/tr[@class="a2"]' % (season, season)
        defense_data = []
        for tr in response.xpath(team_defense_tr_xpath):
            defense_data.append(extract_data(tr, text_xpath))

        # 赛季每场比赛的表现
        competitions = []
        for normal, attack, defense in zip(normal_data, attack_data, defense_data):
            #print(' '.join(normal + attack[5:] + defense[5:]))
            competitions.append(normal + attack[5:] + defense[5:])


        other_data = {
                'uuid' : info[0],
                'season': season,
                'url': response.url
                }

        Persist.InsertPlayerSeasonDetailData(other_data, competitions)

        return competitions


    def parse_player_info(self, response):
        """
        解析角色的基本信息
        """
        player_name_xpath = '//div[@class="mLeftTop"]/h2/text()'
        player_number_xpath = '//div[@class="club_pho"]/span/text()'
        player_info_xpath = '//div[@class="aCont"]//table/tr/td//text()'

        data = dict()
        data['uuid'] = uuid.uuid4()
        data['name'] = ''.join(extract_data(response, player_name_xpath))
        num = ''.join(extract_data(response, player_number_xpath))
        data['number'] = int(num) if num else -1
        data['position'] = ""
        data['club']     = ""
        data['heigh']    = ""
        data['birthday'] = ""
        data['weight']   = ""
        data['country']  = ""
        data['url'] = response.url
        player_info = extract_data(response, player_info_xpath)
        if len(player_info) == 12:
            data['position'] = player_info[1]
            data['club']     = player_info[3]
            data['heigh']    = player_info[5]
            data['birthday'] = player_info[7]
            data['weight']   = player_info[9]
            data['country']  = player_info[11]

        Persist.InsertPlayerInfo(data)

        return (data['uuid'], data['position'] == u'门将')

    def parse_goalkeeper_season_summary(self, response, info, season):
        """
            解析守门员赛季总数据
        """
        text_xpath = './/text()'
        goalkeeper_summary_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="al1"]/tr[@class="a2"]' % season

        other_data = {
                'uuid' : info[0],
                'season': season,
                'url': response.url
                }
        sum_data = []
        for tr in response.xpath(goalkeeper_summary_tr_xpath):
            sum_data.append(extract_data(tr, text_xpath))

        Persist.InsertGoalkeeperSeasonSummary(other_data, sum_data)


    def parse_goalkeeper_season_detail_data(self, response, info, season):
        """
            解析守门员赛季详细数据
        """
        text_xpath = './/text()'
        goalkeeper_detail_tr_xpath = '//div[@id="team-stat-%s"]//table[@id="div1"]/tr[@class="a2"]' % season

        other_data = {
                'uuid' : info[0],
                'season': season,
                'url': response.url
                }
        detail_data = []
        for tr in response.xpath(goalkeeper_detail_tr_xpath):
            detail_data.append(extract_data(tr, text_xpath))

        Persist.InsertGoalkeeperSeasonDetailData(other_data, detail_data)
