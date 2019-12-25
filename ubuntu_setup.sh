#! /usr/bin/env bash
rm results/*.json
scrapy crawl expert -o results/expert.json &&
scrapy crawl game -o results/game.json

