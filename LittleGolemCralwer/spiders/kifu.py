# -*- coding: utf-8 -*-
import scrapy

import GLOBALS
from KifuAssembler.extractor import Extractor
from LittleGolemCralwer.items import KifuItem


def generate_start_urls(player_name):
    specifiers = Extractor().extract(GLOBALS.GAME_JSON_LOCATION, "specifier")
    urls_group = Extractor().extract(GLOBALS.GAME_JSON_LOCATION, "url")
    for specifier, urls in zip(specifiers, urls_group):
        if player_name in specifier:
            return urls


class KifuSpider(scrapy.Spider):
    """
    This spider tries to crawl the raw kifu of games played by a given expert.
    See samples/sample_Lomaben.json as an example of kifus that an expert "Lomaben" played.
    """

    name = 'kifu'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.start_urls = generate_start_urls(self.playername)
        except AttributeError:
            print("Please specify player name in the command line argument (see readme)")

    def parse(self, response):
        yield response.follow(response.css("a.yellow::attr(href)").get(), self.extract_sgf, meta={'url': response.url})

    def extract_sgf(self, response):
        item = KifuItem()
        item['kifu'] = response.text
        item['url'] = response.meta['url']
        yield item
