# -*- coding: utf-8 -*-
import scrapy

import GLOBALS
from LittleGolemCralwer.items import ExpertItem


class ExpertSpider(scrapy.Spider):
    """This spider tries to crawl the experts for Connect6."""

    name = 'expert'
    start_urls = GLOBALS.CONNECT6_EXPERT_URL

    def parse(self, response):
        def get_elos(response):
            result = [e for e in response.css(".portlet-body > table td:nth-child(3)::text").getall()]

            # Trim the leading and trailing whitespaces
            result = [e.strip() for e in result]

            # Remove empty strings
            result = [e for e in result if e]

            return result

        players = response.css(".portlet-body tr td a::text").getall()

        # href => hypertext reference, which is a link to another website
        urls = [response.urljoin(href) for href in response.css(".portlet-body tr td a::attr(href)").getall()]
        elos = get_elos(response)

        for player, url, elo in zip(players, urls, elos):
            item = ExpertItem()
            item['player'] = player
            item['url'] = url
            item['elo'] = elo
            yield item
