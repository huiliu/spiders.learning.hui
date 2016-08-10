#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
#
# 将抓取的球员信息导出为模板表
#
# -----------------------------------------------------------------------------

import enum
import common
import codecs

PlayerTemplate =\
"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<LocalDatas xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <LocalData>
        <g_PlayerTemplate>%s
        </g_PlayerTemplate>
    </LocalData>
</LocalDatas>
"""

PlayerEntryTemplate ="""
            <entry>
                <ID>%d</ID>
                <player_id>%d</player_id>
                <player_name>%s</player_name>
                <player_icon_id>%s</player_icon_id>
                <player_club_id>%d</player_club_id>
                <player_country_id>0</player_country_id>
                <player_position>%d</player_position>
            </entry>"""


def get_img_url(sport_type, oid):
    """返回球员图像URL

    :sport_type:        比赛类型enum SPORT_TYPE
    :oid:               球员ID(未处理之前)

    :returns: 返回球员图像URL
    """
    football_img_url_template = 'http://mat1.gtimg.com/sports/soccerdata/images/player/%d.jpg'
    basketball_img_url_template = 'http://mat1.gtimg.com/sports/soccerdata/images/player/%d.jpg'

    if enum.ST_FOOTBALL == sport_type:
        return football_img_url_template % int(oid)
    elif enum.ST_BASKETBALL == sport_type:
        assert False
        pass

def export_player_template(entries, output):
    """导出球员模板表
    """
    data = PlayerTemplate % ''.join(entries)
    codecs.open(output, 'w', encoding='utf-8').write(data)


def generate_player_template_item(players, sport_type):
    """生成球员模板表记录

    :players:           由爬虫抓取，经简单剥离后的球员数据

    :returns: TODO
    """
    entries = []
    for player in players:
        # 计算球员ID
        uid = int(player['id'])
        oid = common.generate_uid(uid, sport_type)

        try:
            entry = PlayerEntryTemplate % (
                    oid,
                    oid,
                    player['name'],
                    get_img_url(sport_type, uid),
                    common.generate_uid(player['club_id'], sport_type),
                    common.get_position(sport_type, player['posi'])
                ) 
        except Exception as e:
            print(e)
            print("uid: %d name: %s" %( uid, player['name']))
            continue

        entries.append(entry)

    return entries
    #return PlayerTemplate % ''.join(entries)
