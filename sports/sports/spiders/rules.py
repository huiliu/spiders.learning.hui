#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
比赛详细统计信息(football.mid)中，字段对应的名字
{
    'g': '进球',
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
#
# 计算足球球员得分
#


import pymongo

# 得分计算规则
# ------------------------------------------------------------------------
# 首发得分
first_on_group = 2
# 未失球门将、后场得分
unlost_goal_ev_1 = 4
# 未失球前卫得分
unlost_goal_ev_2 = 1

# 门将、后场进球得分
goal_ev_1 = 8
# 前卫进球得分
goal_ev_2 = 6
# 前锋进球得分
goal_ev_3 = 4

# 助攻得分
assist_ev = 3

# 传球得分
trans_ev_ration = 15
# 推断得分
break_ev = 1
# 越位得分
over_ev = -0.5
# 黄牌得分
yellow_card = -1
# 红牌得分
red_card = -3
# ------------------------------------------------------------------------

def calc_score(record, enemy_g):
    """
        根据策划需求计算球员得分
    """
    assert 'score' in record
    # 首发
    if record['status'] == u'首发':
        record['score'] += first_on_group

    # 未失球
    if enemy_g == 0:
        # 对手未进球
        if record['posi'] in (u'门将', u'后卫', u'后腰', u'左后卫', u'右后卫',
                u'中后卫', u'边后卫'):
            record['score'] += unlost_goal_ev_1
        elif record['posi'] in (u'前卫', u'前腰', u'左前卫', u'右前卫',
                u'中前卫', u'边前卫', u'中场'):
            record['score'] += unlost_goal_ev_2

    # 进球
    if 'g' in record and int(record['g']) > 0:
        # 球员得分
        if record['posi'] in (u'门将', u'后卫', u'后腰', u'左后卫', u'右后卫',
                u'中后卫', u'边后卫'):
            record['score'] += goal_ev_1 * int(record['g'])
        elif record['posi'] in (u'前卫', u'前腰', u'左前卫', u'右前卫',
                u'中前卫', u'边前卫', u'中场'):
            record['score'] += goal_ev_2 * int(record['g'])
        elif record['posi'] in (u'前锋', u'左边锋', u'右边锋', u'中锋', u'边锋'):
            record['score'] += goal_ev_3 * int(record['g'])

    # 助攻
    if 'a' in record and int(record['a']) > 0:
        record['score'] += 3 * int(record['a'])
        pass

    # 传球
    if 'p' in record and int(record['p']) > 0:
        record['score'] += int(int(record['p']) / trans_ev_ration)

    # 断球
    if 't' in record and int(record['t']) > 0:
        record['score'] += break_ev * int(record['t'])

    # 越位
    if 'o' in record and int(record['o']) > 0:
        record['score'] += over_ev * int(record['o'])

    # 黄牌
    if 'yb' in record and int(record['yb']) > 0:
        record['score'] += yellow_card * int(record['yb'])

    # 红牌
    if 'rb' in record and int(record['rb']) > 0:
        record['score'] += red_card * int(record['rb'])

    #print("%s: %d" %(record['name'], record['score']))

    return {
            'id': int(record['id'].lstrip('p')),
            'score': record['score'],
            'mid' : record['mid']
            }

def get_player_position(uid, data):
    for player in data:
        if uid == player['id']:
            return (player['status'], player['posi'], player['name'])
    return None

def test():
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
            pos = get_player_position(player['id'], home_player_list)
            if pos and 3 == len(pos):
                p['status'] = pos[0]
                p['posi'] = pos[1]
                p['name'] = pos[2]
                p['score'] = 0
                p['mid'] = cur['mid']
                calc_score(p, away_g)
            #home_player_data.append(p)
        break

if __name__ == '__main__':
    test()
