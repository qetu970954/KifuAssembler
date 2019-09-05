## LittleGolemCrawler
**This crawler crawls historical sgf files for game Connect6**

Note: This project use [`pipenv`]("https://github.com/pypa/pipenv") to manage dependencies, 
please install it first before you start. 

### Clone and Setup 
```shell
$ git clone 
$ cd LittleGolemCralwer
$ pipenv update
```

### Usage
Crawl the Connect6 experts and store the result into `<OutputFile>`
```
$ scrapy crawl expert -o <OutputFile>
```

e.g.:
```
$ scrapy crawl expert -o resources/expert.json
```
Note: You should modify `GLOBALS.py` if you stored the json file in a different place.


---

Search for the games played by expert (requires expert.json).

```
$ scrapy crawl expert -o <ExpertGames>
```

e.g.:
```
$ scrapy crawl game -o resources/expert_games.json
```

 
