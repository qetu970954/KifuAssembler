# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ExpertItem(scrapy.Item):
    player = scrapy.Field()
    url = scrapy.Field()
    elo = scrapy.Field()


class GameItem(scrapy.Item):
    specifier = scrapy.Field()
    url = scrapy.Field()


class KifuItem(scrapy.Item):
    kifu = scrapy.Field()
    url = scrapy.Field()
