# -*- coding: utf-8 -*-
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from news.items import NewsItem
from datetime import datetime

Get = lambda x, y : x.xpath(y).extract()[0].strip()\
                                    if len(x.xpath(y).extract()) > 0 else None

def parseIfengContent(response):
    """
    """
    xpathBody = '//div[@id="artical_real"]'
    sel = Selector(response)

    content = ''
    div = sel.xpath(xpathBody)
    for tmp in div.xpath('.//text()').extract():
        content = "%s%s\n" % (content, tmp.strip())
    item = response.meta['item']
    item['content'] = content.strip()

    return item

class NewsIfengSpider(BaseSpider):
    """
    """
    name = "news.ifeng.spider"
    site_name = u"凤凰网资讯"
    start_urls = ['http://news.ifeng.com/']

    def parse(self, response):
        """
        """
        timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        xpath = {
                    "head0": "/html/body/div[5]/div/div/div/h2/a",
                    "head1": "/html/body/div[5]/div/div/div/h3/a",
                    "importNews0": "/html/body/div[5]/div/div[2]/ul/li/h4/a/b",
                    "mainland0": '/html/body/div[5]/div/div[3]/div[2]/dl/dd/h6/a',
                    "mainland1": '/html/body/div[5]/div/div[3]/ul/li/a',
                    "inter0": '/html/body/div[6]/div/div/div[2]/dl/dd/h6/a',
                    "inter1": '/html/body/div[6]/div/div/ul/li/a',
                    "tai0": '/html/body/div[6]/div/div[3]/div[2]/dl/dd/h6/a',
                    "tai1": '/html/body/div[6]/div/div[3]/ul/li/a',
                    "hkXPath0": '/html/body/div[6]/div/div[4]/div[2]/dl/dd/h6/a',
                    "hkXPath1": '/html/body/div[6]/div/div[4]/ul/li/a'
                }
        pri = {
                    "head0": 0,
                    "head1": 3,
                    "importNews0": 2,
                    "mainland0": 5,
                    "mainland1": 7,
                    "inter0": 5,
                    "inter1": 7,
                    "tai0": 5,
                    "tai1": 7,
                    "hkXPath0": 5,
                    "hkXPath1": 7
                }

        hxs = Selector(response)

        for x, p in zip(xpath.values(), pri.values()):
            for tmp in hxs.xpath(x):
                item = NewsItem()

                item['title'] = Get(tmp, "text()")
                item['href'] = Get(tmp, '@href')
                item['uptime'] = timeNow
                item['pri'] = p
                item['site'] = self.site_name

                request = Request(item['href'], callback=parseIfengContent)
                request.meta['item'] = item
                yield request

        """
        importNewsXPath1 = '/html/body/div[5]/div/div[@class="box_02"]'
        importNewsXPath11 = './/a'

        News(hxs, importNewsXPath0, 2)
        News(hxs.xpath(importNewsXPath1), importNewsXPath11, 4)
        """

class HeadlineIfengSpider(BaseSpider):
    name = 'headline.ifeng.spider'
    site_name = u"凤凰网主页"
    start_urls = ['http://www.ifeng.com/']

    def parse(self, response):
        """
        """
        timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        hxs = Selector(response)
        xpath_headline = "/html/body/div[7]/div/div/div/div[3]/h1/a"
        xpath_mainnews = "/html/body/div[7]/div/div/div/div[3]/ul/li"
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
            item = NewsItem()
            item['title'] = Get(mainNewsItem, "a/text()")
            item['href'] = Get(mainNewsItem, "a/@href")
            item['uptime'] = timeNow
            item['pri'] = 3
            item['site'] = self.site_name

            request = Request(item['href'], callback=parseIfengContent)
            request.meta['item'] = item
            yield request

class NationalGovSpider(BaseSpider):
    name = "nation.gov.spider"
    start_urls = [
                    'http://www.gov.cn/jrzg/zgyw.htm',
                    'http://www.gov.cn/yjgl/tfsj.htm'
                    ]

    def parse(self, response):
        """
        """
        xpathNews = '//a'
        xpathDate = '//span/text()'

        hxs = Selector(response)
        News = hxs.xpath(xpathNews)
        Date = hxs.xpath(xpathDate).extract()

        srcUrl = response.url
        if srcUrl == self.start_urls[0]:
            i = 2; j = -8
            m = 2; n = -1
            site_name = u'政府网中国要闻'
        elif srcUrl == self.start_urls[1]:
            i = 2; j = ''
            m = 1; n = ''
            site_name = u'政府网突发事件'
        else:
            log.msg('网址错误啊！', level=log.WARING)

        for n, d in zip(News[2:-8], Date[2:-1]):
            item = NewsItem()
            item['title'] = Get(n, 'text()')
            item['href'] = "http://www.gov.cn/jrzg/%s" % Get(n, '@href')
            item['pri'] = 0
            item['site'] = site_name

            if site_name == u'政府网中国要闻':
                item['uptime'] = "%s-%s" % (datetime.now().strftime("%Y"), d[1:-1])
            else:
                item['uptime'] = d[1:-1]

            request = Request(item['href'], callback=self.parseGovContent)
            request.meta['item'] = item

            yield request

    def parseGovContent(self, response):
        """
        """
        content = ""
        cssNewsBody = 'td.p1'
        xpathNewsText = './/text()'
        item = response.meta['item']

        sel = Selector(response)
        selBody = sel.css(cssNewsBody)

        if len(selBody) == 1:
            for temp in selBody[0].xpath(xpathNewsText).extract():
                content = "%s%s\n" % (content, temp.strip())
            item['content'] = content.strip()
        else:
            item['content'] = ''

        return item

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

                    request = Request(item['href'],
                                                callback=self.parsePeopleContent)
                    request.meta['item'] = item
                    yield request
                else:
                    for i, j in zip(tt, hh):
                        item = NewsItem()
                        item['title'] = tt[0].strip()
                        item['href'] = hh[0]
                        item['uptime'] = timeNow
                        item['pri'] = pri
                        item['site'] = self.siteName

                        request = Request(item['href'],
                                                    callback=self.parsePeopleContent)
                        request.meta['item'] = item
                        yield request


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

    def parsePeopleContent(self, response):
        """
        """
        xpathNewsBody = 'div[@class="text"]'
        xpathNewsText = './/p/text()'
        item = response.meta['item']

        sel = Selector(response)

        body = sel.xpath(xpathNewsBody)
        if len(body) != 1:
            log.msg("没有获取到新闻内容。%s  %s" %\
                            (item['title'], item['href']), level=log.WARNING)
        content = ''
        for temp in body[0].xpath(xpathNewsText).extract():
            content = "%s%s\n" % (content, temp)
        item['content'] = content.strip()

        return item
