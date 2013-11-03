# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class EnviromentItem(Item):
    # define the fields for your item here like:
    # name = Field()
    id =  Field()
    city_name = Field()
    date = Field()
    pollution_id = Field()
    contamination = Field()
    qLevel = Field()
    qState = Field()
    pass
