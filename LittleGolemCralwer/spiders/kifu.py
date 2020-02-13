# -*- coding: utf-8 -*-
import scrapy
import unicodedata
from LittleGolemCralwer.spiders import config
from KifuAssembler.src.extractor import Extractor
from LittleGolemCralwer.items import KifuItem


# Fetch the games url that is played by a given $player_name.
# Here the $player_name is key-inned from command line.
def generate_start_urls(player_name):
    specifiers = Extractor().extract(config.GAME_JSON_LOCATION, "specifier")
    urls_group = Extractor().extract(config.GAME_JSON_LOCATION, "url")

    # Find the player_name in `specifier`, if found, return the urls
    for specifier, urls in zip(specifiers, urls_group):
        if player_name in specifier:
            return urls


# Handling string crawled from Little Golem, manually pruning unwanted characters
def obtain_game_result(response):
    black_player_score, white_player_score = response.css(".label-info::text")[0].get(), \
                                             response.css(".label-info::text")[1].get()
    black_player_score, white_player_score = unicodedata.normalize("NFKD", black_player_score)[1], \
                                             unicodedata.normalize("NFKD", white_player_score)[1]
    if black_player_score == '2' and white_player_score == '0':
        game_result = "BlackWin"
    elif black_player_score == '0' and white_player_score == '2':
        game_result = "WhiteWin"
    elif black_player_score == '1' and white_player_score == '1':
        game_result = "Draw"
    else:
        game_result = "Unknown"
    return game_result


class KifuSpider(scrapy.Spider):
    """
    This spider tries to crawl the raw kifu of games played by a given expert.
    """

    name = 'kifu'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.start_urls = generate_start_urls(self.playername)
        except AttributeError:
            print("Please specify player name in the command line argument (see readme)")

    def parse(self, response):

        game_result = obtain_game_result(response)

        yield response.follow(response.css("a.yellow::attr(href)").get(), self.extract_sgf,
            meta={'url': response.url,
                  'game_result': game_result}
        )

    def extract_sgf(self, response):
        item = KifuItem()
        item['kifu'] = response.text
        item['url'] = response.meta['url']
        item['game_result'] = response.meta['game_result']
        yield item
