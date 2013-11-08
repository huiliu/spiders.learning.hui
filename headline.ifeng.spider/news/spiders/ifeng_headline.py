# -*- coding: utf-8 -*-
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from news.items import NewsItem

from datetime import datetime

class environmentSpider(BaseSpider):
    name = 'headline.ifeng.news.spider'
    start_urls = ['http://www.ifeng.com/']

    def parse(self, response):
        """
        """
        timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        Get = lambda x, y : x.select(y).extract()[0]\
                                    if len(x.select(y).extract()) > 0 else None

        hxs = HtmlXPathSelector(response)
        xpath_headline = "/html/body/div[8]/div/div/div/div[3]/h1/a"
        xpath_mainnews = "/html/body/div[8]/div/div/div/div[3]/ul/li"
        headline = hxs.select(xpath_headline)
        mainNews = hxs.select(xpath_mainnews)

        items = []
        item = NewsItem()

        item['title'] = Get(headline, "text()")
        item['href'] = Get(headline, "@href")
        item['uptime'] = timeNow
        item['pri'] = 0
        items.append(item)

        for mainNewsItem in mainNews:
            # print mainNewsItem
            item = NewsItem()
            item['title'] = Get(mainNewsItem, "a/text()")
            item['href'] = Get(mainNewsItem, "a/@href")
            item['uptime'] = timeNow
            item['pri'] = 3
            # print mainNewsItem
            # print item
            items.append(item)
        return items
