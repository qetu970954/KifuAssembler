cd results && del *.json && cd ../
scrapy crawl expert -o results/expert.json && ^
scrapy crawl game -o results/game.json