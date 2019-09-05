# -*- coding: utf-8 -*-
import os.path

import scrapy

import GLOBALS
from LittleGolemCralwer.items import GamesItem
from extractor import UrlExtractor


class GamesSpider(scrapy.Spider):
    """This spider tries to crawl the urls of games played by a specific expert (stored in expert.json)."""

    name = 'game'
    start_urls = UrlExtractor().extract_urls_from_json(GLOBALS.EXPERT_JSON_LOCATION) if \
        os.path.isfile(GLOBALS.EXPERT_JSON_LOCATION) else []

    def parse(self, response):
        for href in response.css("div.portlet table td:nth-child(3) a::attr(href)").getall():
            if href.find("gtid=connect6") != -1:
                url = response.urljoin(href)
                yield scrapy.Request(url, callback=self.parse_gamelist)

    def parse_gamelist(self, response):
        item = GamesItem()
        item['specifier'] = response.css(".caption::text").get()
        item['url'] = [response.urljoin(href) for href in
                       response.css(".page-content table tr td b a::attr(href)").getall()]
        yield item
