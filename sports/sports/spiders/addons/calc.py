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

import pymongo
import datetime
import argparse
import score_rules
import calc_core

MT_FOOTBALL = 1
MT_BASKETBALL = 2

SR_NORMAL_FOOTBALL = 1
SR_OLYPICS_FOOTBALL = 2

SR_NORMAL_BASKETBALL = 11
SR_OLYPICS_BASKETBALL = 12

def parse_cmd_options():
    """解析命令行参数
    """
    parser = argparse.ArgumentParser(description="计算球员得分")
    parser.add_argument(
            '-t', '--type', type=int, help="运动类型.(1:足球;2:篮球)", default=1
            )
    parser.add_argument(
                '-r', '--rule', type=int, help="得分计算规则", default=1
            )
    parser.add_argument(
            'mid', type=int, help="赛事ID (default: 默认计算所有)"
            )

    args = parser.parse_args()

    # 解析命令行参数
    condition = {}
    scoreRule = None
    Calc = None

    condition['mid'] = str(args.mid)

    if SR_NORMAL_FOOTBALL == args.rule:
        scoreRule = score_rules.NormalScoreRule()
    elif SR_OLYPICS_FOOTBALL == args.rule:
        scoreRule = score_rules.OlypicsScoreRule()
    else:
        assert False
        return None

    if MT_FOOTBALL == args.type:
        Calc = calc_core.FootballCalc(scoreRule)
    elif MT_BASKETBALL == args.type:
        Calc = calc_core.BasketballCalc(scoreRule)
    else:
        assert False
        return None

    return (Calc, condition)

def main():

    Calc, condition = parse_cmd_options()

    client = pymongo.MongoClient('10.1.0.6', 27017)
    football = client.football_2016
    mid = football.get_collection('mid')

    #player_score = football.get_collection('player_score')
    #player_template = football.get_collection('player_template')

    records = mid.find(condition)
    if records and records.count() >= 1:
        if records.count() > 1:
            print("有点不对劲哦，这场比赛怎么有两条记录！")
        record = records[0]

        now_time = datetime.datetime.now().strftime('%s')
        kickoff_time = int(datetime.datetime.strptime(record['resultinfo']['matchinfo']['datetime'], '%Y-%m-%d %H:%M').strftime('%s')),
        if now_time < kickoff_time[0]:
            # 没有开赛
            print("比赛还没开始哦！")
            return

        result = Calc.calc_one_match(record)

        for item in result[0]:
            print(item)
        for item in result[1]:
            print(item)

if __name__ == '__main__':
    main()
