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

        hxs = HtmlXPathSelector(response)
        xpath_headline = "/html/body/div[7]/div/div/div/div[3]/h1/a"
        xpath_mainnews = "/html/body/div[7]/div/div/div/div[3]/ul/li"
        headline = hxs.select(xpath_headline)
        mainNews = hxs.select(xpath_mainnews)

        items = []
        item = NewsItem()

        item['title'] = headline.select('text()').extract()[0]
        item['href'] = headline.select('@href').extract()[0]
        item['uptime'] = timeNow
        item['pri'] = 0
        items.append(item)

        for mainNewsItem in mainNews:
            # print mainNewsItem
            item = NewsItem()
            item['title'] = mainNewsItem.select('a/text()').extract()[0]
            item['href'] = mainNewsItem.select('a/@href').extract()[0]
            item['uptime'] = timeNow
            item['pri'] = 3
            # print mainNewsItem
            # print item
            items.append(item)
        print items
        return items
