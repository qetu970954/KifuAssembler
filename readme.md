## LittleGolemCrawler
**This crawler crawls historical sgf files for game Connect6**

Note: This project use [`pipenv`]("https://github.com/pypa/pipenv") to manage dependencies, 
please install it first before you start. 

### Clone and Setup 
```shell
$ git clone 
$ cd LittleGolemCralwer
$ pipenv update
$ ./cleanup.cmd
$ ./setup.cmd
```

### Usage

To crawl all games that a players played:
```
$ scrapy crawl sgf -o <OutputFile> -a playername=<PlayerName>
```
e.g.:
```shell
$ scrapy crawl sgf -o resources/Lomaben.json -a playername=Lomaben
```
