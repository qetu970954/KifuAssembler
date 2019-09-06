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

To crawl the Connect6 experts and store the result into `<OutputFile>`
```
$ scrapy crawl expert -o <OutputFile>
```

e.g.:
```
$ scrapy crawl expert -o resources/expert.json
```
This create an `expert.json` in the `resource` directory, and the crawled data are stored in it.

Note: Modify `GLOBALS.py` if you stored the file in a different place.

---

To crawl the games played by expert (this requires `expert.json`).

```
$ scrapy crawl expert -o <Outputfile>
```

e.g.:
```
$ scrapy crawl game -o resources/game.json
```

---

To crawl all games that a players played:
```
$ scrapy crawl sgf -o <OutputFile> -a playername=<PlayerName>
```
e.g.:
```shell
$ scrapy crawl sgf -o resources/Lomaben.json -a playername=Lomaben
```
