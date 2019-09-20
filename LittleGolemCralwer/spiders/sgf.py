# -*- coding: utf-8 -*-
import scrapy

from lgSgfMerger import GLOBALS
from LittleGolemCralwer.items import SgfItem
from lgSgfMerger.extractor import Extractor


def generate_start_urls(player_name):
    specifiers = Extractor().extract(GLOBALS.GAME_JSON_LOCATION, "specifier")
    urls_group = Extractor().extract(GLOBALS.GAME_JSON_LOCATION, "url")
    for specifier, urls in zip(specifiers, urls_group):
        if player_name in specifier:
            return urls


class SgfSpider(scrapy.Spider):
    name = 'sgf'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = generate_start_urls(self.playername)

    def parse(self, response):
        yield response.follow(response.css("a.yellow::attr(href)").get(), self.extract_sgf, meta={'url': response.url})

    def extract_sgf(self, response):
        item = SgfItem()
        item['content'] = response.text
        item['url'] = response.meta['url']
        yield item
