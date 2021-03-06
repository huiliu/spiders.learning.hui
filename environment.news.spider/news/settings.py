# Scrapy settings for news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import scrapy

BOT_NAME = 'news'

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news (+http://www.yourdomain.com)'
ITEM_PIPELINES = [
                    "news.pipelines.EnviromentPipeline"
                 ]
LOG_LEVEL = scrapy.log.WARNING
LOG_FILE = '/tmp/enviroment_log'
