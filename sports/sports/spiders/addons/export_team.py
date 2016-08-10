#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# 从赛程模板表中导出俱乐部模板表
#
# usage:
#       python export_team.py
# ----------------------------------------------------------------------------

import pymongo
import clubs
import enum

class DBConfig:
    """连接MongoDB服务器的相关参数
    """

    host       = '10.1.0.6'                 # 服务器IP
    port       = 27017                      # 服务器端口
    database   = 'football'                 # 数据库名
    collection = 'fixtures'                 # 集合名
    compid     = None                       # 联赛类型
    season     = '2016'                     # 赛季

    sport_type = enum.ST_FOOTBALL           # 体育类型
    output     = "TeamTemplate_table.xml"   # 导出文件名

def main():
    args = DBConfig()

    client = pymongo.MongoClient(args.host, args.port)
    db = client.get_database(args.database)
    collection = db.get_collection(args.collection)

    condition = dict()
    if args.compid:
        condition['compid'] = str(args.compid)
    if args.season:
        condition['season'] = str(args.season)

    clubs_id = list()
    entries = list()
    for record in collection.find(condition, {'_id': 0, 'homeid': 1, 'homename': 1}):
        if record['homeid'] not in clubs_id:
            clubs_id.append(record['homeid'])
            data = {"id": record['homeid'][1:], 'name': record['homename']}
            entry = clubs.generate_team_template_entry(data, args.sport_type)
            entries.append(entry)

    clubs.export_team_template(entries, args.output)

if '__main__' == __name__:
    main()
