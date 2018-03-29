# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Movie(scrapy.Item):
    name = scrapy.Field()
    english_name = scrapy.Field()
    year = scrapy.Field()
    length = scrapy.Field()
    release_date = scrapy.Field()
    genres = scrapy.Field()
    nation = scrapy.Field()
    director = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()
    awards = scrapy.Field()
    nominations = scrapy.Field()
