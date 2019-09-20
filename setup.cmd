python -m pytest && ^
python -m doctest lgSgfMerger.incorporator.py && ^
rm resources/expert.json resources/game.json && ^
scrapy crawl expert -o resources/expert.json && ^
scrapy crawl game -o resources/game.json