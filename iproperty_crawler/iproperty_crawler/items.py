# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IpropertyCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    website_url = scrapy.Field()
    property_name = scrapy.Field()
    asking_price = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    property_type = scrapy.Field()
    tenure  = scrapy.Field()
    posted_date = scrapy.Field()
    land_title_type = scrapy.Field()
