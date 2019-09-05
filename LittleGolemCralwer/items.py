# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LittlegolemcralwerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    content = scrapy.Field()


class Connect6ExpertsItem(scrapy.Item):
    player = scrapy.Field()
    url = scrapy.Field()
    elo = scrapy.Field()


class GamesItem(scrapy.Item):
    specifier = scrapy.Field()
    url = scrapy.Field()
