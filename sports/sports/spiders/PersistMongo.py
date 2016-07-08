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
        
