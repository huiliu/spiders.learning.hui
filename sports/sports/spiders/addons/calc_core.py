#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
#
# 计算live数据的球员得分
# 输入的数据必须为腾讯图文直接结果数据，或组装类似结构的json
#
# -----------------------------------------------------------------------------

import rules
import enum
import common
import codecs
import datetime
from xml.etree import ElementTree as ET

class FootballCalc:
    """计算足球比赛球员得分
    """
    PlayerMatchScoreTemplate = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns1:Document xmlns:ns1="http://viivgame.cn/schema/db_match_schedule.xsd">
%s
</ns1:Document>"""

    PlayerMatchScoreEntryTemplate = """\t<ns1:player_match_score N_player_id="%d" N_match_id="%d" N_score="%.2f"/>"""

    def __init__(self, score_rule, playerTemplate, output):
        """TODO: Docstring for __init__.

        :score_rule:    得分计算规则
        :output:        输出文件名
        """
        self.scoreRule = score_rule
        self.player_template = playerTemplate
        self.calcRule = rules.FootballRule
        self.output = output
        self.sportType = enum.ST_FOOTBALL
        self.homeid = 0
        self.awayid = 0

    def calc_one_match(self, live_data):
        """计算某场比赛的球员得分
    
            :live_data:     来自腾讯网的图文直接数据
    
            :return:        球员得分
        """
        self.mid = int(live_data['mid'])
        home_score = 0
        if 'g' in live_data['resultinfo']['stat']['home']:
            home_score = int(live_data['resultinfo']['stat']['home']['g'])
    
        away_score = 0
        if 'g' in live_data['resultinfo']['stat']['away']:
            away_score = int(live_data['resultinfo']['stat']['away']['g'])
    
        self.homeid = int(live_data['resultinfo']['matchinfo']['homeid'].lstrip('t'))
        self.awayid = int(live_data['resultinfo']['matchinfo']['awayid'].lstrip('t'))
    
        home_player_stat = live_data['resultinfo']['stat']['home']['player']
        away_player_stat = live_data['resultinfo']['stat']['away']['player']
    
        home_player_list = live_data['resultinfo']['lineup']['home']['player']
        away_player_list = live_data['resultinfo']['lineup']['away']['player']
    
        home_result = self._calc_players_score(home_player_stat,
                                        home_player_list, self.homeid, away_score)
        away_result = self._calc_players_score(away_player_stat,
                                        away_player_list, self.awayid, home_score)
    
        # 此场比赛中，所有球员的评价得分
        players_score = home_result[0] + away_result[0]
        # 两队的球员基本信息，用于生成球员模板表
        players_template = home_result[1] + away_result[1]
    
        return (players_score, players_template)

    def export_playerscore_template(self, data):
        """导出球员得分模板表
        """
        players = self.get_team_all_players()
        entries = []
        for record in data:
            uid = common.generate_uid(record['id'], self.sportType)
            entry = self.PlayerMatchScoreEntryTemplate % (
                        uid,
                        common.generate_uid(record['mid'], self.sportType),
                        record['score']
                    )
            entries.append(entry)
            try:
                players.remove(uid)
            except Exception as e:
                print("PlayerId: %d in mid: %d and PlayerTemplate does not match" % (record['id'], self.mid))

        for ID in players:
            entry = self.PlayerMatchScoreEntryTemplate % (
                        common.generate_uid(ID, self.sportType),
                        common.generate_uid(record['mid'], self.sportType),
                        0
                    )
            entries.append(entry)

        codecs.open(self.output, 'w', encoding='utf-8').write(
                    self.PlayerMatchScoreTemplate % '\n'.join(entries)
                )

    def export_playerscore_to_db(self, data, tbl, cursor):
        """将球员得分数据导入到数据库中

        :data:      赛事球员得分数据
        :cursor:    数据库游标
        """
        SQLTemplate = "INSERT INTO %s (player_id, match_id, score, match_start_time) VALUES %s"

        now = datetime.datetime.now().strftime("%s")
        scores = []
        for record in data:
            score = '(%d, %d, %.2f, %d)' % (
                        common.generate_uid(record['id'], self.sportType),
                        common.generate_uid(record['mid'], self.sportType),
                        record['score'],
                        now
                    )
            scores.append(score)

        sql = SQLTemplate % (tbl, ','.join(values))
        cursor.execute(sql)

    def get_team_all_players(self):
        """给未进入大名单球员增加一条虚记录
        """
        tree = None
        try:
            tree = ET.parse(self.player_template)
        except Exception as e:
            print(e)
        players = set()
        root = tree.getroot()
        for entry in root[0][0]:
            clubid = common.get_uid(int(entry[4].text), self.sportType)
            if clubid == self.homeid or clubid == self.awayid:
                pid = int(entry[0].text)
                players.add(int(entry[0].text))

        return players

    def export_playervalues_to_db(self):
        pass

    def _calc_players_score(self, players_show_data, player_list, home_id, lost_score):
        """计算球员们的得分
    
        :players_show_data:     比赛中球员们的表现
        :player_list:           球员位置(前中后)、状态信息(首发、替补)
        :lost_score:            已方失球数
    
        :returns: (球员得分,球员模板)
        """
        players_score = list()
        players_template = dict()
    
        for player in players_show_data:
            p = player
            pos = self.calcRule.get_player_position(player['id'], player_list)
            if pos and 3 == len(pos):
                p['status'] = pos[0]
                p['posi'] = pos[1]
                p['name'] = pos[2]
                p['score'] = 0
                score = self.calcRule.calc_score(self.scoreRule, p, lost_score)
                # 该比赛球员得分信息
                players_score.append(
                            {
                                'id': int(p['id'].lstrip('p')),
                                'mid': self.mid,
                                'score': score,
                            }
                        )
                # 球员信息
                players_template[p['id']] = {
                        'id': int(p['id'].lstrip('p')),
                        'name': p['name'],
                        'club': home_id,
                        'country': 0,
                        'posi': p['posi']
                        }
        return (players_score, players_template.values())


class BasketballCalc:
    def __init__(self, score_rule, output):
        pass
