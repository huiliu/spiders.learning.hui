#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# 获取赛程中的球队ID列表
#
# Usage:
#       pythone getclubs.py
#
# ------------------------------------------------------------------------------

import pymongo
import argparse

def parse_cmd_options():
    parser = argparse.ArgumentParser(description="从赛程表中提取球队ID")
    parser.add_argument(
                '--host', default='10.1.0.6',
                help='MongoDB服务器IP default: %(default)s'
            )
    parser.add_argument(
                '-p', '--port', default=27017, type=int,
                help='MongoDB服务器端口 default: %(default)s'
            )
    parser.add_argument(
                '-d', '--database', default='football',
                help='MongoDB数据库名字 default: %(default)s'
            )
    parser.add_argument(
                '-c', '--collection', default='fixtures',
                help='MongoDB数据库集合名字 default: %(default)s'
            )
    parser.add_argument(
                '--compid', default=208, type=int,
                help='联赛类型 default: %(default)s'
            )
    parser.add_argument(
                '-s', '--season', default=2016, type=int,
                help='赛季 default: %(default)s'
            )

    args = parser.parse_args()

    return args

class DBConfig:
    """连接MongoDB服务器的相关参数
    """

    host       = '10.1.0.6'     # 服务器IP
    port       = 27017          # 服务器端口
    database   = 'football'     # 数据库名
    collection = 'fixtures'     # 集合名
    compid     = None           # 联赛类型
    season     = '2016'         # 赛季


def get_clubs_id(args):
    client = pymongo.MongoClient(args.host, args.port)
    db = client.get_database(args.database)
    collection = db.get_collection(args.collection)

    condition = dict()
    if args.compid:
        condition['compid'] = str(args.compid)
    if args.season:
        condition['season'] = str(args.season)

    clubs = list()

    for record in collection.find(condition, {'_id': 0, 'homeid': 1, 'awayid': 1}):
        if record['homeid'] not in clubs:
            clubs.append(record['homeid'])
        if record['awayid'] not in clubs:
            clubs.append(record['awayid'])

    return [c[1:] for c in clubs]

def main():
    args = parse_cmd_options()
    data = get_clubs_id(args)

    print(','.join(data))

if '__main__' == __name__:
    main()
