from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from voa.items import VoaItem


class voaSpider(BaseSpider):
    name = 'english.voa'
    allowed_domains = ['51voa.com']
    start_urls = ['http://www.51voa.com']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select('//*[@id="list"]/ul/li/a[2]/text()').extract()
        urls = hxs.select('//*[@id="list"]/ul/li/a[2]/@href').extract()

        itmes = []
        for title, url in zip(titles, urls):
            print "Title:\t" + title
            print "URL:\t" + url
