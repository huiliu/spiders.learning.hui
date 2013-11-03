# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from news.items import EnviromentItem
from scrapy import log

class environmentSpider(BaseSpider):
    name = 'environment.news.spider'
    start_urls = ['http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp?city=&startdate=2000-01-01&enddate=2013-11-02&page=1']

    def parse(self, response):
        """
        """
        hxs = HtmlXPathSelector(response)
        record_count = int(hxs.select("/html/body/table/tr/td[2]/div/center/div/table/tr[33]/td/b[2]/font/text()").extract()[0])
        log.msg("总页数为：%d\n", record_count, level = log.WARNING)
        for i in range(2, record_count + 1):
            log.msg("第%d页\n" % i)
            yield Request('http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp?city=&startdate=2000-01-01&enddate=2013-11-02&page=%d' % i, callback=self.parse_items)

    def parse_items(self, response):
        """
        """
        hxs = HtmlXPathSelector(response)
        xpath_tr = '/html/body/table/tr/td[2]/div/center/div/table/tr'
        tr = hxs.select(xpath_tr)

        # Becouse the tr of table
        if len(tr) <= 5:
            log.msg("表格的列数不对！%s", repr(tr), level = log.WARNING)
            return

        items = []
        for i in range(2, len(tr) - 3):
            tds = tr[i].select('td/text()').extract()
            if len(tds) != 7:
                log.msg("表格的列数不对！%s", repr(tds))
                continue
            item = EnviromentItem()
            item['id'] = int(tds[0])
            item['city_name'] = tds[1]
            item['date'] = tds[2]
            item['pollution_id'] = int(tds[3])
            item['contamination'] = tds[4]
            item['qLevel'] = tds[5]
            item['qState'] = tds[6]
            items.append(item)

        return items
