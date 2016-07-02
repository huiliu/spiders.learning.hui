# -*- coding: utf-8 -*-
from __future__ import print_function
import scrapy
from sports.items import SeasonData
import MySQLdb


class PersistentObj:
    def __init__(self):
        self.cursor = None
        pass

    def _init(self):
        conn = MySQLdb.connect(
                host='10.1.0.6',
                user='viivgame',
                passwd='viivgame'
                )
        self.cursor = conn.cursor()

    def _check_curson(self):
        if not self.cursor:
            self._init()
            assert self.cursor

    def InsertTeamSeasonSummary(self, name, season, data):
        self._check_curson()
        InsertSql = "insert into team_season_summary (
            name,
            season,
            type,
            result,
            jinqiu,
            shiqiu,
            chuanqiu
            redcard,
            yellocard,
            zhugong,
            qiangduan,
            yuewei,
            fangui,
            touqiu,
            renyiqiudefen,
            shezheng
            jizhongmenkuan,
            chuanzhong,

        )"
        for row in data:
            pass
        pass

    def InsertTeamSeasonDetailData(self, data):
        self._check_curson()
        pass

    def InsertPlayerSeasonSummary(self, data):
        self._check_curson()
        pass

    def InsertPlayerSeasonDetailData(self, data):
        self._check_curson()
        pass

Persist = PersistentObj()

extract_data = lambda response, xpath : [x.strip() for x in
        response.xpath(xpath).extract() if x.strip()]

class QqSpider(scrapy.Spider):
    name = "team"
    allowed_domains = ["soccerdata.sports.qq.com"]
    start_urls = (
        #'http://soccerdata.sports.qq.com/player/13017.htm',
        'http://soccerdata.sports.qq.com/team/1.htm',
        #'http://soccerdata.sports.qq.com/team/164.htm',
    )

    # {url : status}
    teams_url = {
            'http://soccerdata.sports.qq.com/team/1.htm': True
            }
    players_url = dict()

    def parse(self, response):
        name_xpath = '//div[@class="mLeftTop"]/h2/text()'
        name = ' '.join(extract_data(response, name_xpath))
        season_xpath = '//div[@class="set-t"]/span/text()'
        for season in response.xpath(season_xpath).extract():
            summary = self.parse_team_season_sum_data(response, name, season)
            team_data = self.parse_team_season_detail_data(response, name, season)
            player_data = self.parse_player_season_sum_data(response, season, self.players_url)

            file_name = '%s_%s.dat' % (name, season)
            with open(file_name.encode('utf-8'), 'a+') as fd:
                for t in summary:
                    temp = ' '.join(t) + '\n'
                    fd.write(temp.encode('utf-8'))
                fd.write('\n')

                # 球队数据
                for competition in team_data:
                    temp = ' '.join(competition) + '\n'
                    fd.write(temp.encode('utf-8'))
                fd.write('\n')

                # 球员数据(非守门员)
                for competition in player_data[0]:
                    temp = ' '.join(competition) + '\n'
                    fd.write(temp.encode('utf-8'))
                fd.write('\n')

                # 守门员数据
                for competition in player_data[1]:
                    temp = ' '.join(competition) + '\n'
                    fd.write(temp.encode('utf-8'))

        for url, status in self.teams_url.items():
            if not status:
                print(url)
                yield scrapy.Request(url)

        with open('players', 'a+') as fd:
            for name, url in self.players_url.items():
                data = '%s %s\n' % (name, url)
                fd.write(data.encode('utf-8'))

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

        Persist.InsertTeamSeasonSummary(name, season, summary)

        return summary

    def parse_team_season_detail_data(self, response, name, season):
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
        host_team_name = host_team_a.xpath('./text()').extract()
        host_team_href = host_team_a.xpath('./@href').extract()

        for name, href in zip(host_team_name, host_team_href):
            if name not in self.teams_url:
                self.teams_url[href] = False

        result_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="a3"]//a'%season)
        result_team_name = result_team_a.xpath('./text()').extract()
        result_team_href = result_team_a.xpath('./@href').extract()
        #print(result_team_name)

        guest_team_a = response.xpath('//table[@id="%s-div1"]/tr[@class="a2"]/td[@class="t_left"]//a'%season)
        guest_team_name = guest_team_a.xpath('./text()').extract()
        guest_team_href = guest_team_a.xpath('./@href').extract()

        for name, href in zip(guest_team_name, guest_team_href):
            if name not in self.teams_url:
                self.teams_url[href] = False

        # 球队赛季每场比赛的表现
        competitions = []
        for normal, attack, defense in zip(normal_data, attack_data, defense_data):
            print(' '.join(normal + attack[5:] + defense[5:]))
            competitions.append(normal + attack[5:] + defense[5:])

        Persist.InsertTeamSeasonDetailData(competition)


        return competitions


    def parse_player_season_sum_data(self, response, season, players):
        """
        解析个人赛季总体数据

        个人赛季汇总数据：常规10；进攻10；防守9
        """
        td_text_xpath = './/td//text()'
        player_name_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_1"]/tr[@class="a2"]/td[2]/a/text()' % (season, season)
        player_href_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_1"]/tr[@class="a2"]/td[2]/a/@href' % (season, season)

        player_normal_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_1"]/tr[@class="a2"]' % (season, season)
        player_attack_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_2"]/tr[@class="a2"]' % (season, season)
        player_defense_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-play_stat_div_3"]/tr[@class="a2"]' % (season, season)

        player_name = extract_data(response, player_name_xpath)
        player_href = extract_data(response, player_href_xpath)
        player_normal_data = []
        for tr in response.xpath(player_normal_xpath):
            player_normal_data.append(extract_data(tr, td_text_xpath))

        player_attack_data = []
        for tr in response.xpath(player_attack_xpath):
            player_attack_data.append(extract_data(tr, td_text_xpath))

        player_defense_data = []
        for tr in response.xpath(player_defense_xpath):
            player_defense_data.append(extract_data(tr, td_text_xpath))

        # 球员（非守门员）数据
        players_data = []
        for normal, attack, defense in zip(player_normal_data, player_attack_data, player_defense_data):
            print(' '.join(normal + attack[3:] + defense[3:]))
            players_data.append(normal + attack[3:] + defense[3:])

        for name, href in zip(player_name, player_href):
            players[name] = href

        # 守门员数据
        # 12
        goalkeeper_title_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a1"]//text()' % (season, season)
        goalkeeper_tr_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]' % (season, season)

        goalkeeper_name_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]/td[2]/a/text()' % (season, season)
        goalkeeper_href_xpath = '//div[@id="player-stat-%s"]//table[@id="%s-div1"]/tr[@class="a2"]/td[2]/a/@href' % (season, season)

        # 守门员数据汇总
        goalkeepers_data = []
        goalkeeper_title = extract_data(response, goalkeeper_title_xpath)
        print("守门员数据：")
        print(' '.join(goalkeeper_title))
        for tr in response.xpath(goalkeeper_tr_xpath):
            data = extract_data(tr, './/text()')
            print(' '.join(data))
            goalkeepers_data.append(data)

        goalkeeper_name = extract_data(response, goalkeeper_name_xpath)
        goalkeeper_href = extract_data(response, goalkeeper_href_xpath)

        for name, href in zip(goalkeeper_name, goalkeeper_href):
            players[name] = href

        return (players_data, goalkeepers_data)
