# KifuAssembler

[![Build Status](https://travis-ci.com/qetu970954/KifuAssembler.svg?branch=master)](https://travis-ci.com/qetu970954/KifuAssembler)   [![codecov](https://codecov.io/gh/qetu970954/KifuAssembler/branch/master/graph/badge.svg)](https://codecov.io/gh/qetu970954/KifuAssembler)





**Crawls and Assembles historical Kifus of a specific Connect6 player**


## Clone and Setup 
This project use [`poetry`](https://python-poetry.org/docs/managing-environments/) for dependency management.

```bash
$ git clone https://github.com/qetu970954/KifuAssembler.git
$ cd KifuAssembler
$ poetry update
$ poetry shell
```

Run setup script:
```bash
$ ./windows_setup.cmd   # On Windows
$ ./ubuntu_setup.sh    # On Ubuntu
```
This should generates `expert.json` and `game.json` in the `results/` directory,
and some crawled information are stored inside these files.

### Crawl !!
Let scrapy crawl the kifu for `$PlayerName` and store the result to `$OutputFile` 
```
$ scrapy crawl kifu -a player_name=<PlayerName> -o <OutputFile> 
```
e.g.:
```shell
$ scrapy crawl kifu -a player_name=Lomaben -o results/Lomaben.json
```
This spider internally looks for `results/game.json` and use it's content, so you must make sure that file exist before you run this.

### Assemble !!

Let KifuAssembler assemble the kifu's you crawled
```shell
$ python -m KifuAssembler.assemble -s=<InputFile> -o=<OutputFile> 
```
If not specified, the result will be put in `results/result.sgf`
e.g.:
```shell
$ python -m KifuAssembler.assemble -s=results/Lomaben.json
```
