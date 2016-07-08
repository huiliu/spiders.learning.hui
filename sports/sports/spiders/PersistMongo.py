#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 将数据持久化到MongoDB
#

import pymongo

class Persist:
    """docstring for Persist:"""
    def __init__(self, cfg):
        self.client = pymongo.MongoClient(cfg['host'], cfg['port'])
        self.db = self.client[cfg['db']]

    def insert_one(self, tbl, data):
        if not (tbl and isinstance(tbl, str)):
            print("failed insert into mongodb! because tbl")
            return
        if not (data and isinstance(data, dict)):
            print("failed insert into mongodb! because data")
            return
        self.db[tbl].insert_one(data)

    def insert_many(self, tbl, data):
        if not (tbl and isinstance(tbl, str)):
            print("failed insert into mongodb! because tbl")
            return
        if not (data and isinstance(data, list)):
            print("failed insert into mongodb! because data")
            return
        self.db[tbl].insert_many(data)
        
class PersistLiveData:
    def __init__(self, cfg):
        self.cfg = cfg
        self.client = pymongo.MongoClient(cfg['host'], cfg['port'])
        self.live_collection = self.client[cfg['db']].get_collection(cfg['match'])

    def InsertLive(self, data):
        """
            插入赛程信息
        """
        if isinstance(data, dict):
            self.live_collection.insert_one(data)

    def get_fixture_match_id(self, cond={}):
        cur = self.client[self.cfg['db']][self.cfg['fixture']].find(cond, {'_id': 0, 'id': 1})

        return cur

    def get_downloaded_match_id(self):
        # 赛事实况
        ret = self.live_collection.find({}, {'_id': 0, 'mid': 1})
        matchids = list()
        for item in ret:
            matchids.append(item['mid'])
        return matchids

