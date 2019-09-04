# -*- coding: utf-8 -*-
import scrapy
from LittleGolemCralwer.items import LittlegolemcralwerItem


class LgSpider(scrapy.Spider):
    name = 'LG'
    start_urls = ['http://www.littlegolem.net/jsp/tournament/tournament.jsp?trnid=connect6.ch.27.1.1']


    def parse(self, response):
        for game_id in response.css("div.portlet:nth-child(5) > div:nth-child(2) > table a::attr(href)").getall():
            yield response.follow(game_id, self.parse_game)

    def parse_game(self, response):
        yield response.follow(response.css("a.yellow::attr(href)").get(), self.extract_sgf)

    def extract_sgf(self, response):
        item = LittlegolemcralwerItem()
        item['content'] = response.text
        yield item
