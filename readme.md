## LittleGolemCrawler
[![Build Status](https://travis-ci.com/qetu970954/LittleGolemCralwer.svg?token=7esN258CaAa7xyc7UmSY&branch=master)](https://travis-ci.com/qetu970954/LittleGolemCralwer)


**Crawl and assemble historical Kifus for a specific Connect6 player**

### Before you start
This project use [`pipenv`]("https://github.com/pypa/pipenv") to manage dependencies, 
please install it before you start.

### Project Structure
There are two major components:
    1. LittleGolemCrawler : Contains crawler that can crawl Kifu from the LG website.
    2. Scalpels : Contains helper objects and functions for assembling various "Kifu"s.
 
### Clone and Setup 
```shell
$ git clone https://qetu970954@github.com/qetu970954/LittleGolemCralwer.git
$ cd LittleGolemCralwer
$ pipenv update
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

You can see resources/expert.json for available players.

