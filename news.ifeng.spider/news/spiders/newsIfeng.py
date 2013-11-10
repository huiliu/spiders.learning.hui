# -*- coding: utf-8 -*-
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from news.items import NewsItem
from datetime import datetime

Get = lambda x, y : x.xpath(y).extract()[0].strip()\
                                    if len(x.xpath(y).extract()) > 0 else None

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

        def News(hxs, xpath, pri):
            for tmp in hxs.xpath(xpath):
                item = NewsItem()

                item['title'] = Get(tmp, "text()")
                item['href'] = Get(tmp, '@href')
                item['uptime'] = timeNow
                item['pri'] = pri
                item['site'] = self.site_name

                items.append(item)

        hxs = Selector(response)

        hlXPath0 = "/html/body/div[5]/div/div/div/h2/a"
        hlXPath1 = "/html/body/div[5]/div/div/div/h3/a"

        News(hxs, hlXPath0, 0)
        News(hxs, hlXPath1, 3)

        importNewsXPath0 = "/html/body/div[5]/div/div[2]/ul/li/h4/a/b"
        importNewsXPath1 = '/html/body/div[5]/div/div[@class="box_02"]'
        importNewsXPath11 = './/a'

        News(hxs, importNewsXPath0, 2)
        News(hxs.xpath(importNewsXPath1), importNewsXPath11, 4)

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

        hxs = Selector(response)
        xpath_headline = "/html/body/div[8]/div/div/div/div[3]/h1/a"
        xpath_mainnews = "/html/body/div[8]/div/div/div/div[3]/ul/li"
        headline = hxs.xpath(xpath_headline)
        mainNews = hxs.xpath(xpath_mainnews)

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

class NationalGovSpider(BaseSpider):
    name = "nation.gov.spider"
    site_name = u'政府网中国要闻'
    start_urls = ['http://www.gov.cn/jrzg/zgyw.htm']

    def parse(self, response):
        """
        """
        xpathNews = '//a'
        xpathDate = '//span/text()'

        hxs = Selector(response)
        News = hxs.xpath(xpathNews)
        Date = hxs.xpath(xpathDate).extract()

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

class HeadLinePeopleSpider(BaseSpider):
    """
    """
    name = "headline.people.spider"
    siteName = u"人民网主页"
    start_urls = ["http://www.people.com.cn/"]

    def parse(self, response):
        """
        """
        def News(sel, xpath, pri):
            """
            """
            Headline = sel.xpath(xpath)

            for h in Headline:
                item = NewsItem()
                tt = h.xpath('.//a/text()').extract()
                hh = h.xpath('.//a/@href').extract()
                if tt and len(tt) == 1:
                    item['title'] = tt[0].strip()
                    item['href'] = hh[0]
                    item['uptime'] = timeNow
                    item['pri'] = pri
                    item['site'] = self.siteName
                    items.append(item)
                else:
                    for i, j in zip(tt, hh):
                        item = NewsItem()
                        item['title'] = tt[0].strip()
                        item['href'] = hh[0]
                        item['uptime'] = timeNow
                        item['pri'] = pri
                        item['site'] = self.siteName
                        items.append(item)

        xpathHeadline = "/html/body/div[3]/div/p"
        xpathBlock1Items = "/html/body/div[3]/div[3]/div/h2"
        xpathBlock2Head = "/html/body/div[3]/div[3]/div[2]/ul/li/strong"
        xpathBlock2Items = "/html/body/div[3]/div[3]/div[2]/ul/li"
        xpathRightBlockHead = "/html/body/div[3]/div[4]/div[4]/ul/li/strong"
        xpathRightBlockItems = "/html/body/div[3]/div[4]/div[4]/ul[2]/li"
        xpathBlock3Items = "/html/body/div[3]/div[3]/div[4]/ul/li"
        xpathHotSpecial = "/html/body/div[3]/div[4]/div[6]/ul/li"
        xpathHotInter = "/html/body/div[5]/div[3]/div/div/dl/dt"

        timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items = []
        sel = Selector(response)

        News(sel, xpathHeadline, 0)
        News(sel, xpathBlock1Items, 0)
        News(sel, xpathBlock2Items, 2)
        News(sel, xpathBlock2Items, 3)
        News(sel, xpathRightBlockHead, 3)
        News(sel, xpathRightBlockItems, 5)
        News(sel, xpathBlock3Items, 4)
        News(sel, xpathHotSpecial, 6)
        News(sel, xpathHotInter, 8)

        return items
