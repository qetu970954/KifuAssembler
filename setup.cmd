pytest
python -m doctest incorporator.py
rm resources/expert.json resources/game.json
scrapy crawl expert -o resources/expert.json
scrapy crawl game -o resources/game.json