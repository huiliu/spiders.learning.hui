#!/bin/bash

# -----------------------------------------------------------------------------
#
# 抓取2016/2017赛季信息
#
# -----------------------------------------------------------------------------

# 从网络上抓取赛程
## 中超 
#scrapy crawl fixtures -a start_date=2016-07-20 -a match_type=208
## 英超 
#scrapy crawl fixtures -a start_date=2016-08-13 -a match_type=8
# 意甲
scrapy crawl fixtures -a start_date=2016-08-21 -a match_type=21
## 德甲
scrapy crawl fixtures -a start_date=2016-08-27 -a match_type=22
## 法甲
scrapy crawl fixtures -a start_date=2016-08-13 -a match_type=24
## 西甲
scrapy crawl fixtures -a start_date=2016-08-20 -a match_type=23
## 亚冠
#scrapy crawl fixtures -a start_date=2016-08-23 -a match_type=605
## 欧冠
#scrapy crawl fixtures -a start_date=2016-08-23 -a match_type=605
## 欧联
#scrapy crawl fixtures -a start_date=2016-08-23 -a match_type=605

# 导出赛程
./sports/spiders/addons/fixtures.py --config sports/spiders/addons/config.ini
