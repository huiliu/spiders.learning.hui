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
#   python export_fixtures.py -h 10.1.0.6 -p 27017 -d football -c fixtures -m 8 -s 2017 -o 8_2017.xml
#
#   OR
#   python export_fixtures.py --config config.ini -o 8_2017.xml
#   
#
################################################################################
from ConfigParser import ConfigParser
import pymongo
import codecs
import datetime
import argparse
import sys

# 比赛类型
SPORT_TYPE = 1
FINAL_TIME = 60 * 30 # 秒

DOCUMENT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns1:Document xmlns:ns1="http://viivgame.cn/schema/db_match_schedule.xsd">
%s
</ns1:Document>
"""
ROW_TEMPLATE = """<ns1:db_match_schedule N_match_id="%s" N_match_type="%s" N_sport_type="%s" N_match_round="%s" N_match_start_time="%s" N_match_valide_time="%s" N_home_id="%s" N_away_id="%s" N_home_score="%s" N_away_score="%s"/>"""

def load_config(cfgfile='config.ini'):
    fd = codecs.open(cfgfile, 'r', encoding='utf-8')
    cfg = ConfigParser()
    cfg.readfp(fd)
    cfg_dict = dict()
    for k, v in cfg.items('mongo'):
        cfg_dict[k] = v
    for k, v in cfg.items('condition'):
        cfg_dict[k] = v

    return cfg_dict

def export(src, dst, condition):
    if not (src and dst):
        print("数据错误!")
        assert False
        return

    content = []
    content_classify = dict()
    for record in src.find(condition):
        start_time = datetime.datetime.strptime("%s %s" % (record['date'], record['time']), "%Y-%m-%d %H:%M").strftime('%s')

        if record['date'] in content_classify:
            content_classify[record['date']][0].append(record)
            if int(start_time) < content_classify[record['date']][1]:
                content_classify[record['date']][1] = int(start_time)
        else:
            content_classify[record['date']] = ([record], int(start_time))

    for k, v in content_classify.iteritems():
        # 最早开赛前30分钟
        valide_time = str(v[1] - FINAL_TIME)
        for record in v[0]:

            now = datetime.datetime.now().strftime('%s')
            start_time = datetime.datetime.strptime("%s %s" % (record['date'], record['time']), "%Y-%m-%d %H:%M").strftime('%s')
            homescore = awayscore = '-1'
            if int(now) > int(start_time):
                homescore = record['homescore']
                awayscore = record['awayscore']

            row = ROW_TEMPLATE % (
                        record['id'],
                        record['compid'],
                        str(SPORT_TYPE),
                        record['round'],
                        start_time,
                        #record['date'],
                        valide_time,
                        record['homeid'][1:],
                        record['awayid'][1:],
                        homescore,
                        awayscore
                    )
            content.append(row)

    open(dst,'w').write(DOCUMENT % '\n'.join(content))

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
                '-m', '--match', help='联赛类型。208:中超'
            )
    parser.add_argument(
                '-s', '--season', help='赛季'
            )
    parser.add_argument(
                '-o', '--output', required=True,
                help='输出文件名.'
            )

    args = parser.parse_args()

    if not(args.config or args.db or args.collection):
        sys.exit('must set -d, -c or --config')

    return args

def main():

    host       = None
    port       = 27017
    db         = None
    collection = None
    condition = dict()

    args = parse_cmd_options()

    if args.match:
        condition['compid'] = args.match
    if args.season:
        condition['season'] = args.season

    if args.config:
        # 如果有指定配置文件，则优先使用配置文件
        cfg        = load_config()

        host       = cfg['host']
        port       = int(cfg['port'])
        db         = cfg['db']
        collection = cfg['collection']

        if 'compid' in cfg:
            condition['compid'] = cfg['compid']
        if 'season' in cfg:
            condition['season'] = cfg['season']
    else:
        host       = args.host
        port       = args.port
        db         = args.db
        collection = args.collection

    col = None
    if host and port and db and collection:
        client = pymongo.MongoClient(host, port)
        database = client.get_database(db)
        col = database.get_collection(collection)

    export(col, args.output, condition)

if '__main__' == __name__:
    main()
