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
import sys
import datetime
import argparse
import score_rules
import calc_core
import enum

def parse_cmd_options():
    """解析命令行参数
    """
    parser = argparse.ArgumentParser(description="计算球员得分")
    parser.add_argument(
                '--host', default="10.1.0.6",
                help="Mongo服务器IP. default: %(default)s"
            )
    parser.add_argument(
                '-p', '--port', type=int, default=27017,
                help="Mongo服务器端口. default: %(default)s"
            )
    parser.add_argument(
                '-d', '--database', default="football",
                help="数据库名. default: %(default)s"
            )
    parser.add_argument(
                '-c', '--collection', default="mid",
                help="collection名. default: %(default)s"
            )
    parser.add_argument(
            '-t', '--type', type=int, default=1,
            help="运动类型.(1:足球;2:篮球) default: %(default)s", 
            )
    parser.add_argument(
                '-r', '--rule', type=int, help="得分计算规则", default=1
            )
    parser.add_argument(
                '-o', '--output', help="输入到文件. default: %(default)s",
                default="PlayerMatchScoreTemplate.xml"
            )
    parser.add_argument(
            'mid', type=int, help="赛事ID (default: 默认计算所有)"
            )

    args = parser.parse_args()

    # 解析命令行参数
    scoreRule = None
    Calc = None

    if enum.SR_NORMAL_FOOTBALL == args.rule:
        scoreRule = score_rules.NormalScoreRule()
    elif enum.SR_OLYPICS_FOOTBALL == args.rule:
        scoreRule = score_rules.OlypicsScoreRule()
    else:
        assert False
        return None

    if enum.ST_FOOTBALL == args.type:
        Calc = calc_core.FootballCalc(scoreRule, args.output)
    elif enum.ST_BASKETBALL == args.type:
        Calc = calc_core.BasketballCalc(scoreRule, args.output)
    else:
        assert False
        return None

    condition = {}
    condition['mid'] = str(args.mid)

    collection = get_collection(args)

    return (Calc, collection.find(condition))

def get_collection(arg):
    """返回collection对象

    :arg:       与数据库相关的配置
    :returns:   collection对象

    """
    try:
        client = pymongo.MongoClient(arg.host, arg.port)
        football = client.get_database(arg.database)
        mid = football.get_collection(arg.collection)

        return mid
    except Exception as e:
        sys.exit(e)

def main():

    scores = list()
    Calc, records = parse_cmd_options()

    if records and records.count() >= 1:
        if records.count() > 1:
            print("有点不对劲哦，这场比赛怎么有两条记录！\n只计算了其中一条记录的得分，请确认！")
        record = records[0]

        now_time = datetime.datetime.now().strftime('%s')
        kickoff_time = int(datetime.datetime.strptime(record['resultinfo']['matchinfo']['datetime'], '%Y-%m-%d %H:%M').strftime('%s')),
        if now_time < kickoff_time[0]:
            # 没有开赛
            print("比赛还没开始哦！")
            return

        result = Calc.calc_one_match(record)
        scores.extend(result[0])
        for item in result[0]:
            print(item)

    Calc.export_playerscore_template(scores)

if __name__ == '__main__':
    main()
