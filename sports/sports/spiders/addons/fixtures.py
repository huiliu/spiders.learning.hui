#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# 将mongoDB中的赛程数据导出为XML模板表格式
#
# usage:
#   python export_fixtures.py --help
#
#   导出英超2016/2017赛季赛程数据到8_2017.xml
#   python export_fixtures.py -h 10.1.0.6 -p 27017 -d football -c fixtures -m 8 -s 2016 -o 8_2016.xml
#
#   OR
#   python export_fixtures.py --config config.ini
#   
#
################################################################################
from ConfigParser import ConfigParser
import pymongo
import codecs
import datetime
import argparse
import sys
import enum
import common

# 比赛类型
SPORT_TYPE = 1
FINAL_TIME = 60 * 30 # 秒

DOCUMENT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns1:Document xmlns:ns1="http://viivgame.cn/schema/db_match_schedule.xsd">
%s
</ns1:Document>
"""
ROW_TEMPLATE = """<ns1:db_match_schedule N_match_id="%d" N_match_type="%d" N_sport_type="%s" N_match_round="%s" N_match_start_time="%s" N_match_valide_time="%s" N_home_id="%d" N_away_id="%d" N_home_score="%d" N_away_score="%d"/>"""

class ConfigFile:
    """docstring for ConfigFile:"""
    def __init__(self, cfgfile="config.ini"):
        fd = codecs.open(cfgfile, 'r', encoding='utf-8')
        self.cfg = ConfigParser()
        self.cfg.readfp(fd)
    def __getattr__(self, name):
        try:
            return self.cfg.get('main', name)
        except Exception as e:
            return None

def export_fixtures_to_template(args):

    condition = dict()
    try:
        if args.match:
            condition['compid'] = str(args.match)
    except Exception as e:
        pass
    try:
        if args.season:
            condition['season'] = str(args.season)
    except Exception as e:
        pass

    sport_type = enum.ST_FOOTBALL
    try:
        sport_type = int(args.type)
    except Exception as e:
        pass

    if not(args.host and args.port and args.db and args.collection):
        assert False
        print("导出赛程失败！")
        return

    client = pymongo.MongoClient(args.host, int(args.port))
    database = client.get_database(args.db)
    collection = database.get_collection(args.collection)

    content = []
    content_classify = dict()
    for record in collection.find(condition):
        start_time = datetime.datetime.strptime("%s %s" % (record['date'], record['time']), "%Y-%m-%d %H:%M").strftime('%s')

        if record['date'] in content_classify:
            content_classify[record['date']][0].append(record)
            if int(start_time) < content_classify[record['date']][1]:
                content_classify[record['date']][1] = int(start_time)
        else:
            content_classify[record['date']] = [[record], int(start_time)]

    for k, v in content_classify.iteritems():
        # 最早开赛前30分钟
        valide_time = str(v[1] - FINAL_TIME)
        for record in v[0]:

            now = datetime.datetime.now().strftime('%s')
            start_time = datetime.datetime.strptime("%s %s" % (record['date'], record['time']), "%Y-%m-%d %H:%M").strftime('%s')
            homescore = awayscore = -1
            if int(now) > int(start_time):
                try:
                    homescore = int(record['homescore'])
                    awayscore = int(record['awayscore'])
                except Exception as e:
                    print("%s 比赛有结果有误!")
                    pass

            mid = int(record['id'])
            mid = common.generate_uid(mid, sport_type)
            homeid = common.generate_uid(int(record['homeid'][1:]), sport_type)
            awayid = common.generate_uid(int(record['awayid'][1:]), sport_type)

            row = ROW_TEMPLATE % (
                        mid,
                        int(record['compid']),
                        str(sport_type),
                        record['round'],
                        start_time,
                        #record['date'],
                        valide_time,
                        homeid,
                        awayid,
                        homescore,
                        awayscore
                    )
            content.append(row)

    open(args.output,'w').write(DOCUMENT % '\n'.join(content))

def parse_cmd_options():
    parser = argparse.ArgumentParser(
            description="将爬虫抓取的赛程数据输出为赛程模板表格式",
            conflict_handler='resolve'
            )

    #parser.add_argument('-?', '--help', action='store_true')
    parser.add_argument(
            '-h', '--host', default='10.1.0.6',
            help='存放爬虫数据的MongoDB数据库ID default: %(default)s'
            )
    parser.add_argument(
                '-p', '--port', type=int, default=27017,
                help='MongoDB使用的端口。default: %(default)s'
            )
    parser.add_argument(
                '-d', '--db', default='football', help='db名'
            )
    parser.add_argument(
                '-c', '--collection', default='fixture', help='collection名'
            )
    parser.add_argument(
                '--config', help='从文件中读取配置信息。'
            )
    parser.add_argument(
                '-t', '--type', default=1,
                help='体育类型。1:足球. default: %(default)s'
            )
    parser.add_argument(
                '-m', '--match', help='联赛类型。208:中超'
            )
    parser.add_argument(
                '-s', '--season', help='赛季'
            )
    parser.add_argument(
                '-o', '--output', default="db_match_schedules.xml",
                help='输出文件名.'
            )

    args = parser.parse_args()

    if not(args.config or args.db or args.collection):
        sys.exit('must set -d, -c or --config')

    return args

def main():

    args = parse_cmd_options()

    if args.config:
        # 如果有指定配置文件，则优先使用配置文件
        args = ConfigFile(args.config)

    export_fixtures_to_template(args)

if '__main__' == __name__:
    main()
