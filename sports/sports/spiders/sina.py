# -*- coding: utf-8 -*-
# ---------------------------------------------
# 抓取sina.com.cn上的体育数据
# ---------------------------------------------
import scrapy


class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["match.sports.sina.com.cn"]
    start_urls = (
        'http://match.sports.sina.com.cn/football/csl/index.php?utype=rnd&l_typ=208&rnd=1&dpc=1',
    )

    def parse(self, response):
        pass

    def parse_csl_schedules(self, response):
        """
        抓取中超赛程
        """
        pass
