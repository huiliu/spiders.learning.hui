# -*- coding: utf-8 -*-
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from news.items import NewsItem
from datetime import datetime

class NewsIfengSpider(BaseSpider):
    """
    """
    name = "news.ifeng.spider"
    site_name = u"凤凰网资讯"
    start_urls = ['http://news.ifeng.com/']

    def parse(self, response):
        """
        """
        items = []
        timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        Get = lambda x, y : x.select(y).extract()[0].strip()\
                                    if len(x.select(y).extract()) > 0 else None

        def News(hxs, xpath, pri):
            for tmp in hxs.select(xpath):
                item = NewsItem()

                item['title'] = Get(tmp, "text()")
                item['href'] = Get(tmp, '@href')
                item['uptime'] = timeNow
                item['pri'] = pri
                item['site'] = self.site_name

                items.append(item)

        hxs = HtmlXPathSelector(response)

        hlXPath0 = "/html/body/div[5]/div/div/div/h2/a"
        hlXPath1 = "/html/body/div[5]/div/div/div/h3/a"

        News(hxs, hlXPath0, 0)
        News(hxs, hlXPath1, 3)

        importNewsXPath0 = "/html/body/div[5]/div/div[2]/ul/li/h4/a/b"
        importNewsXPath1 = '/html/body/div[5]/div/div[@class="box_02"]'
        importNewsXPath11 = './/a'

        News(hxs, importNewsXPath0, 2)
        News(hxs.select(importNewsXPath1), importNewsXPath11, 4)

        mainlandXPath0 = '/html/body/div[5]/div/div[3]/div[2]/dl/dd/h6/a'
        mainlandXPath1 = '/html/body/div[5]/div/div[3]/ul/li/a'
        News(hxs, mainlandXPath0, 5)
        News(hxs, mainlandXPath1, 7)

        interXPath0 = '/html/body/div[6]/div/div/div[2]/dl/dd/h6/a'
        interXPath1 = '/html/body/div[6]/div/div/ul/li/a'
        News(hxs, interXPath0, 5)
        News(hxs, interXPath1, 7)

        taiXPath0 = '/html/body/div[6]/div/div[3]/div[2]/dl/dd/h6/a'
        taiXPath1 = '/html/body/div[6]/div/div[3]/ul/li/a'
        News(hxs, taiXPath0, 5)
        News(hxs, taiXPath1, 7)

        hkXPath0 = '/html/body/div[6]/div/div[4]/div[2]/dl/dd/h6/a'
        hkXPath1 = '/html/body/div[6]/div/div[4]/ul/li/a'
        News(hxs, hkXPath0, 5)
        News(hxs, hkXPath1, 7)

        return items

class environmentSpider(BaseSpider):
    name = 'headline.ifeng.spider'
    site_name = u"凤凰网主页"
    start_urls = ['http://www.ifeng.com/']

    def parse(self, response):
        """
        """
        timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        Get = lambda x, y : x.select(y).extract()[0].strip()\
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
        item['site'] = self.site_name
        items.append(item)

        for mainNewsItem in mainNews:
            # print mainNewsItem
            item = NewsItem()
            item['title'] = Get(mainNewsItem, "a/text()")
            item['href'] = Get(mainNewsItem, "a/@href")
            item['uptime'] = timeNow
            item['pri'] = 3
            item['site'] = self.site_name
            # print mainNewsItem
            # print item
            items.append(item)
        return items

Get = lambda x, y : x.select(y).extract()[0].strip()\
                                    if len(x.select(y).extract()) > 0 else None
class NationalGovSpider(BaseSpider):
    name = "nation.gov.spider"
    site_name = u'政府网中国要闻'
    start_urls = ['http://www.gov.cn/jrzg/zgyw.htm']

    def parse(self, response):
        """
        """
        xpathNews = '//a'
        xpathDate = '//span/text()'

        hxs = HtmlXPathSelector(response)
        News = hxs.select(xpathNews)
        Date = hxs.select(xpathDate).extract()

        items = []
        for n, d in zip(News[2:-8], Date[2:-1]):
            item = NewsItem()
            item['title'] = Get(n, 'text()')
            item['href'] = "http://www.gov.cn/jrzg/%s" % Get(n, '@href')
            item['uptime'] = d[0]
            item['pri'] = 0
            item['site'] = self.site_name
            items.append(item)
        return items
