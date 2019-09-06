# -*- coding: utf-8 -*-

import scrapy

import GLOBALS
from LittleGolemCralwer.items import GameItem
from extractor import Extractor


class GamesSpider(scrapy.Spider):
    """This spider tries to crawl the urls of games played by a specific expert (stored in expert.json)."""

    name = 'game'
    start_urls = Extractor().extract(GLOBALS.EXPERT_JSON_LOCATION, "url")

    def parse(self, response):
        for href in response.css("div.portlet table td:nth-child(3) a::attr(href)").getall():
            if "gtid=connect6" in href:
                url = response.urljoin(href)
                yield scrapy.Request(url, callback=self.parse_gamelist)

    def parse_gamelist(self, response):
        item = GameItem()
        item['specifier'] = response.css(".caption::text").get()
        item['url'] = [response.urljoin(href) for href in
                       response.css(".page-content table tr td b a::attr(href)").getall()]
        yield item
