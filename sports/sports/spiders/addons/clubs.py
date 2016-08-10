#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# 获取赛程中的球队ID列表
#
# Usage:
#       pythone clubs.py
#
# ------------------------------------------------------------------------------

import pymongo
import enum
import codecs

TeamTemplate =\
"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<LocalDatas xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <LocalData>
        <g_TeamTemplate>%s
        </g_TeamTemplate>
    </LocalData>
</LocalDatas>
"""

TeamEntryTemplate = """
            <entry>
                <ID>%d</ID>
                <team_id>%d</team_id>
                <team_name>%s</team_name>
                <team_type>%d</team_type>
                <sport_type>%d</sport_type>
                <team_logo_id>%s</team_logo_id>
            </entry>"""

def get_img_url(sport_type, tid):
    """返回球队LOGO的URL
    """

    football_img_url_template = 'http://mat1.gtimg.com/sports/soccerdata/images/team/140/t%d.png'
    basketball_img_url_template = 'http://mat1.gtimg.com/sports/soccerdata/images/team/140/t%d.png'

    if enum.ST_FOOTBALL == sport_type:
        return football_img_url_template % tid
    elif enum.ST_BASKETBALL == sport_type:
        assert False
        return basketball_img_url_template % tid

def export_team_template(entries, output):
    """将模板表写到磁盘
    """
    data = TeamTemplate % ''.join(entries)
    codecs.open(output, 'w', encoding='utf-8').write(data)


def generate_team_template_entry(data, sport_type):

    stype = int(sport_type) << 28
    tid = int(data['id'])
    oid = tid | stype

    try:
        entry = TeamEntryTemplate % (
                    oid,
                    oid,
                    data['name'],
                    enum.TT_CLUB,
                    sport_type,
                    get_img_url(sport_type, tid)
                )
    except Exception as e:
        print(e)
        print('id: %d, name:%s' % (tid, data['name']))
        return ""

    return entry


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

def test():
    class DBConfig:
        """连接MongoDB服务器的相关参数
        """
    
        host       = '10.1.0.6'     # 服务器IP
        port       = 27017          # 服务器端口
        database   = 'football'     # 数据库名
        collection = 'fixtures'     # 集合名
        compid     = None           # 联赛类型
        season     = '2016'         # 赛季

    args = DBConfig()
    data = get_clubs_id(args)

    print(','.join(data))
    print(len(data))

if '__main__' == __name__:
    test()
