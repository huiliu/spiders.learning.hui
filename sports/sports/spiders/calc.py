#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# 根据MongoDB中的赛事统计信息(football.mid)，计算球员的得分并存储到MongoDB中
# (football.player_score)
# 由于数据可能残缺，可能出现异常
#
# ----------------------------------------------------------------------------

import rules
import pymongo
import datetime


def main():
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
    for cur in mid.find():
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
                pos = rules.get_player_position(player['id'], home_player_list)
                if pos and 3 == len(pos):
                    p['status'] = pos[0]
                    p['posi'] = pos[1]
                    p['name'] = pos[2]
                    p['score'] = 0
                    p['mid'] = competition_id
                    gPlayerScore.append(rules.calc_score(p, away_g))
                    gPlayers[p['id']] = {
                            'id': int(p['id'].lstrip('p')),
                            'name': p['name'],
                            'club': home_id,
                            'country': 0,
                            'posi': p['posi']
                            }

            for player in away_player_stat:
                p = player
                pos = rules.get_player_position(player['id'], away_player_list)
                if pos and 3 == len(pos):
                    p['status'] = pos[0]
                    p['posi'] = pos[1]
                    p['name'] = pos[2]
                    p['score'] = 0
                    p['mid'] = competition_id
                    gPlayerScore.append(rules.calc_score(p, home_g))
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

    player_score.insert_many(gPlayerScore)
    player_template.insert_many(gPlayers.values())
    print("playerscore : %d" % len(gPlayerScore))
    print("player_template : %d" % len(gPlayers))
    print("competion : %d" % len(mids))

if __name__ == '__main__':
    main()
