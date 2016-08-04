#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 根据策划规则
# 计算足球球员得分
#


import pymongo
"""
比赛详细统计信息(football.mid)中，字段对应的名字
对应于腾讯图文直播数据
{
    'g': '进球',
    'a': '助攻',
    's': '射门',
    'so': '射正球门',
    'rb': '红牌',
    'yb': '黄牌',
    'o': '越位',
    'wf': '被侵犯',
    'f': '犯规',
    'p': '传球',
    'ap': '传中',
    'kp': '关键传球',
    't': '抢断',
    'i': '断球',
    'c': '角球',
    'fk': '任意球',
    'pp': '控球率'
}
"""

class Football:
    """足球球员得分计算规则"""
        
    @staticmethod
    def calc_score(score_rule, record, lost):
        """
            根据策划需求计算球员得分
    
            :score_rule:    得分规则
            :record:        一个球员的表现记录
            :lost:          球队失球数
    
            :return:        球员得分
        """
        assert 'score' in record
        # 首发
        if record['status'] == u'首发':
            record['score'] += score_rule.first_on_group
    
        # 未失球
        if lost == 0:
            # 对手未进球
            if record['posi'] in (u'门将', u'后卫', u'后腰', u'左后卫', u'右后卫',
                    u'中后卫', u'边后卫'):
                record['score'] += score_rule.unlost_goal_ev_1
            elif record['posi'] in (u'前卫', u'前腰', u'左前卫', u'右前卫',
                    u'中前卫', u'边前卫', u'中场'):
                record['score'] += score_rule.unlost_goal_ev_2
    
        # 进球
        if 'g' in record and int(record['g']) > 0:
            # 球员得分
            if record['posi'] in (u'门将', u'后卫', u'后腰', u'左后卫', u'右后卫',
                    u'中后卫', u'边后卫'):
                record['score'] += score_rule.goal_ev_1 * int(record['g'])
            elif record['posi'] in (u'前卫', u'前腰', u'左前卫', u'右前卫',
                    u'中前卫', u'边前卫', u'中场'):
                record['score'] += score_rule.goal_ev_2 * int(record['g'])
            elif record['posi'] in (u'前锋', u'左边锋', u'右边锋', u'中锋', u'边锋'):
                record['score'] += score_rule.goal_ev_3 * int(record['g'])
    
        # 助攻
        if 'a' in record and int(record['a']) > 0:
            record['score'] += 3 * int(record['a'])
            pass
    
        # 传球
        if 'p' in record and int(record['p']) > 0:
            record['score'] += int(int(record['p']) / score_rule.trans_ev_ration)
    
        # 断球
        if 't' in record and int(record['t']) > 0:
            record['score'] += score_rule.break_ev * int(record['t'])
    
        # 越位
        if 'o' in record and int(record['o']) > 0:
            record['score'] += score_rule.over_ev * int(record['o'])
    
        # 黄牌
        if 'yb' in record and int(record['yb']) > 0:
            record['score'] += score_rule.yellow_card * int(record['yb'])
    
        # 红牌
        if 'rb' in record and int(record['rb']) > 0:
            record['score'] += score_rule.red_card * int(record['rb'])
    
        #print("%s: %d" %(record['name'], record['score']))
    
        return {
                'id': int(record['id'].lstrip('p')),
                'score': record['score'],
                'mid' : record['mid']
                }

    @staticmethod
    def get_player_position(uid, data):
        """
            取得某场比赛球员的信息（首发/替补，位置，姓名）
    
            :uid:           球员uid
            :data:          某场比赛的球员信息（来自图文直播数据）
    
            :return:        (status, posi, name)
        """
        for player in data:
            if uid == player['id']:
                return (player['status'], player['posi'], player['name'])
        return None

class Basketball:
    pass

def test():
    from score_rules import NormalScoreRule
    scoreRule = NormalScoreRule()

    client = pymongo.MongoClient('10.1.0.6', 27017)
    football = client['football']
    mid = football.get_collection('mid')

    for cur in mid.find({'mid': '343925'}):
        home_g = int(cur['resultinfo']['stat']['home']['g'])
        away_g = int(cur['resultinfo']['stat']['away']['g'])

        home_player_stat = cur['resultinfo']['stat']['home']['player']
        away_player_stat = cur['resultinfo']['stat']['away']['player']

        home_player_list = cur['resultinfo']['lineup']['home']['player']
        away_player_list = cur['resultinfo']['lineup']['away']['player']

        home_player_data = []
        for player in home_player_stat:
            p = player
            pos = Football.get_player_position(player['id'], home_player_list)
            if pos and 3 == len(pos):
                p['status'] = pos[0]
                p['posi'] = pos[1]
                p['name'] = pos[2]
                p['score'] = 0
                p['mid'] = cur['mid']
                Football.calc_score(scoreRule, p, away_g)
                print(p['score'])
                
        break

if __name__ == '__main__':
    test()
