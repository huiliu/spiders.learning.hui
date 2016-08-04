#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# 根据MongoDB中的赛事统计信息(football.mid)，计算球员的得分并存储到MongoDB中
# (football.player_score)
# 由于数据可能残缺，可能出现异常
#
# usage:
#   python calc.py --help
#
#   计算足球赛事343925的球员得分，得分规则使用通用规则
#   python calc.py -t 1 -r 1 343925
#
# ----------------------------------------------------------------------------

import rules
import pymongo
import datetime
import argparse
import score_rules

MT_FOOTBALL = 1
MT_BASKETBALL = 2

SR_NORMAL_FOOTBALL = 1
SR_OLYPICS_FOOTBALL = 2

SR_NORMAL_BASKETBALL = 11
SR_OLYPICS_BASKETBALL = 12

def parse_cmd_options():
    """
        命令行参数
    """
    parser = argparse.ArgumentParser(description="计算球员得分")
    parser.add_argument(
            '-t', '--type', type=int, help="运动类型.(1:足球;2:篮球)", default=1
            )
    parser.add_argument(
                '-r', '--rule', type=int, help="得分计算规则", default=1
            )
    parser.add_argument(
            'mid', nargs='?', type=int, help="赛事ID (default: 默认计算所有)"
            )

    args = parser.parse_args()
    return args

def main():

    condition = {}
    scoreRule = None
    calcRule = None
    args = parse_cmd_options()

    if args.mid:
        condition['mid'] = str(args.mid)

    if MT_FOOTBALL == args.type:
        calcRule = rules.Football()
    elif MT_BASKETBALL == args.type:
        calcRule = rules.Basketball()
    else:
        assert False
        return

    if SR_NORMAL_FOOTBALL == args.rule:
        scoreRule = score_rules.NormalScoreRule()
    elif SR_OLYPICS_FOOTBALL == args.rule:
        scoreRule = score_rules.OlypicsScoreRule()
    else:
        assert False
        return

    gPlayers = dict()
    gPlayerScore = list()

    client = pymongo.MongoClient('10.1.0.6', 27017)
    football = client.football
    mid = football.get_collection('mid')
    player_score = football.get_collection('player_score')
    player_template = football.get_collection('player_template')

    mids =[]

    now_time = datetime.datetime.now().strftime('%s')
    # TODO: 此处可以加入查询条件，以计算指定比赛的球员得分
    #for cur in mid.find({'mid': '321808'}):
    for cur in mid.find(condition):
        competition_id = int(cur['mid'])
        if competition_id in mids:
            continue
        try:
            kickoff_time = int(datetime.datetime.strptime(cur['resultinfo']['matchinfo']['datetime'], '%Y-%m-%d %H:%M').strftime('%s')),
            if now_time < kickoff_time[0]:
                # 没有开赛
                continue
            mids.append(competition_id)

            home_g = 0
            if 'g' in cur['resultinfo']['stat']['home']:
                home_g = int(cur['resultinfo']['stat']['home']['g'])

            away_g = 0
            if 'g' in cur['resultinfo']['stat']['away']:
                away_g = int(cur['resultinfo']['stat']['away']['g'])

            home_id = int(cur['resultinfo']['matchinfo']['homeid'].lstrip('t'))
            away_id = int(cur['resultinfo']['matchinfo']['awayid'].lstrip('t'))

            home_player_stat = cur['resultinfo']['stat']['home']['player']
            away_player_stat = cur['resultinfo']['stat']['away']['player']

            home_player_list = cur['resultinfo']['lineup']['home']['player']
            away_player_list = cur['resultinfo']['lineup']['away']['player']

            for player in home_player_stat:
                p = player
                pos = calcRule.get_player_position(player['id'], home_player_list)
                if pos and 3 == len(pos):
                    p['status'] = pos[0]
                    p['posi'] = pos[1]
                    p['name'] = pos[2]
                    p['score'] = 0
                    p['mid'] = competition_id
                    gPlayerScore.append(calcRule.calc_score(scoreRule, p, away_g))
                    gPlayers[p['id']] = {
                            'id': int(p['id'].lstrip('p')),
                            'name': p['name'],
                            'club': home_id,
                            'country': 0,
                            'posi': p['posi']
                            }

            for player in away_player_stat:
                p = player
                pos = calcRule.get_player_position(player['id'], away_player_list)
                if pos and 3 == len(pos):
                    p['status'] = pos[0]
                    p['posi'] = pos[1]
                    p['name'] = pos[2]
                    p['score'] = 0
                    p['mid'] = competition_id
                    gPlayerScore.append(calcRule.calc_score(scoreRule, p, home_g))
                    gPlayers[p['id']] = {
                            'id': int(p['id'].lstrip('p')),
                            'name': p['name'],
                            'club': home_id,
                            'country': 0,
                            'posi': p['posi']
                            }
        except Exception as e:
            continue
            print(e, competition_id)

    #player_score.insert_many(gPlayerScore)
    #player_template.insert_many(gPlayers.values())
    for item in gPlayerScore:
        print(item)
    print("playerscore : %d" % len(gPlayerScore))
    print("player_template : %d" % len(gPlayers))
    print("competion : %d" % len(mids))

if __name__ == '__main__':
    main()
