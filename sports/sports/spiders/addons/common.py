#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一些通用规则

BITWISE_COUNT = 28

import enum

def get_uid(oid, sport_type):
    """反解析得到id
    """
    return oid & ((sport_type << BITWISE_COUNT) - 1)
    pass

def generate_uid(oid, sport_type):
    """生成唯一ID

    :oid:           原始ID
    :sport_type:    体育类型

    :return:        返回一个唯一ID
    """
    assert isinstance(oid, int)
    return oid | (sport_type << BITWISE_COUNT)

def get_football_postion(posi):
    """返回足球球员位置的枚举值

    :posi:      网页中的球员位置
    """
    if posi == u'门将':
        return enum.PP_FB_GOALKEEPER
    elif posi in (u'后卫', u'后腰', u'左后卫', u'右后卫', u'中后卫', u'边后卫'):
        return enum.PP_FB_BACK
    elif posi in (u'前卫', u'前腰', u'左前卫', u'右前卫', u'中前卫', u'边前卫', u'中场'):
        return enum.PP_FB_MIDFIELD
    elif posi in (u'前锋', u'左边锋', u'右边锋', u'中锋', u'边锋'):
        return enum.PP_FB_FORWARD
    else:
        print(posi)
        assert False
        return 0

def get_position(sport_type, posi):
    """返回球员位置
    """

    if enum.ST_FOOTBALL == sport_type:
        return get_football_postion(posi)
    elif enum.ST_BASKETBALL == sport_type:
        return get_basketball_postion(posi)
    else:
        assert False
        return 0

def get_basketball_postion(posi):
    pass
