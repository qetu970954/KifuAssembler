# -*- coding: utf-8 -*-
import scrapy

from LittleGolemCralwer.items import LittlegolemcralwerItem


class LgSpider(scrapy.Spider):
    name = 'backup'
    start_urls = [f'http://www.littlegolem.net/jsp/tournament/tournament.jsp?trnid=connect6.ch.{i}.1.1'
                  for i in range(26, 28)]

    def parse(self, response):
        for game_id in response.css("div.portlet:nth-child(5) > div:nth-child(2) > table a::attr(href)").getall():
            yield response.follow(game_id, self.parse_game)

    def parse_game(self, response):
        yield response.follow(response.css("a.yellow::attr(href)").get(), self.extract_sgf, meta={'url': response.url})

    def extract_sgf(self, response):
        item = LittlegolemcralwerItem()
        item['content'] = response.text
        item['url'] = response.meta['url']
        yield item
