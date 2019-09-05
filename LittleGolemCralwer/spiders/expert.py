# -*- coding: utf-8 -*-
import scrapy

from LittleGolemCralwer.items import Connect6ExpertItem


class ExpertSpider(scrapy.Spider):
    """This spider tries to crawl the experts for Connect6"""
    name = 'expert'
    start_urls = ['http://www.littlegolem.net/jsp/info/player_list.jsp?gtvar=connect6_DEFAULT']

    def parse(self, response):
        def get_elos(response):
            result = [e for e in response.css(".portlet-body > table td:nth-child(3)::text").getall()]

            # Trim the leading and trailing whitespaces
            result = [e.strip() for e in result]

            # Remove empty strings
            result = [e for e in result if e]

            return result

        names = response.css(".portlet-body tr td a::text").getall()
        urls = [response.urljoin(link) for link in response.css(".portlet-body tr td a::attr(href)").getall()]
        elos = get_elos(response)

        for name, url, elo in zip(names, urls, elos):
            item = Connect6ExpertItem()
            item['name'] = name
            item['url'] = url
            item['elo'] = elo
            yield item
