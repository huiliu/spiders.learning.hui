#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
#
# 计算live数据的球员得分
# 输入的数据必须为腾讯图文直接结果数据，或组装类似结构的json
#
# -----------------------------------------------------------------------------

import rules

class FootballCalc:
    """
    """
    def __init__(self, score_rule):
        """TODO: Docstring for __init__.

        :score_rule:    得分计算规则
        """
        self.scoreRule = score_rule
        self.calcRule = rules.FootballRule


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
    
        home_id = int(live_data['resultinfo']['matchinfo']['homeid'].lstrip('t'))
        away_id = int(live_data['resultinfo']['matchinfo']['awayid'].lstrip('t'))
    
        home_player_stat = live_data['resultinfo']['stat']['home']['player']
        away_player_stat = live_data['resultinfo']['stat']['away']['player']
    
        home_player_list = live_data['resultinfo']['lineup']['home']['player']
        away_player_list = live_data['resultinfo']['lineup']['away']['player']
    
        home_result = self._calc_players_score(home_player_stat,
                                        home_player_list, home_id, away_score)
        away_result = self._calc_players_score(away_player_stat,
                                        away_player_list, away_id, home_score)
    
        # 此场比赛中，所有球员的评价得分
        players_score = home_result[0] + away_result[0]
        # 两队的球员基本信息，用于生成球员模板表
        players_template = home_result[1] + away_result[1]
    
        return (players_score, players_template)

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
                                'score': score
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
    def __init__(self, score_rule):
        pass
