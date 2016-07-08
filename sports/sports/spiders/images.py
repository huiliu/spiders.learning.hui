# -*- coding: utf-8 -*-

# ------------------------------------------------
#
# 从腾讯网站抓取足球图像
# 
# ------------------------------------------------
import scrapy
import pymongo
import MySQLdb

class ImgQqSpider(scrapy.Spider):
    name = "images"
    allowed_domains = ["mat1.gtimg.com"]
    start_urls = (
        'http://mat1.gtimg.com/sports/soccerdata/images/player/17128.jpg',
    )

    def __init__(self):
        self.client = pymongo.MongoClient('10.1.0.6', 27017)

        urls = self._generate_player_icon_url()
        urls += self._generate_club_icon_url()
        #print(urls)
        self.start_urls = set(urls)

    def _generate_player_icon_url(self):
        """
            抓取球员头像
        """
        ## 球员图像地址URL模板
        ## %d 为球员ID
        url_tpl = 'http://mat1.gtimg.com/sports/soccerdata/images/player/%d.jpg'
        player_template = self.client['football'].get_collection('player_template')
        urls = []
        for doc in player_template.find({}, {'_id':0, 'id': 1}):
            url = url_tpl % doc['id']
            if url not in urls:
                urls.append(url)
        return urls

    def _generate_club_icon_url(self):
        """
            抓取俱乐部头像
        """
        url_tpl = 'http://mat1.gtimg.com/sports/soccerdata/soccerdata/images/team/140/t%s.jpg'
        club_template = self.client['football'].get_collection('clubs')
        urls = []
        for doc in club_template.find({}, {'_id':0, 'id': 1}):
            url = url_tpl % doc['id']
            if url not in urls:
                urls.append(url)

        print urls


    def parse(self, response):
        """
        """
        if 200 != response.status:
            return
        file_name = response.url.split('/')[-1]
        with open(file_name, 'w') as fd:
            fd.write(response.body)
