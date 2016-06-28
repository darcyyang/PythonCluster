# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovierecommendationItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    # name = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
    desc = scrapy.Field()
    tags = scrapy.Field()
    actors = scrapy.Field()
    longDesc = scrapy.Field()
    age = scrapy.Field()
    genre = scrapy.Field()
    area = scrapy.Field()
    language = scrapy.Field()
    releaseDate = scrapy.Field()
    runtime = scrapy.Field()
    itemFrom = scrapy.Field()
    pass
