## LittleGolemCrawler
**This crawler crawls historical sgf files for game Connect6**

**Note**: This project use [`pipenv`]("https://github.com/pypa/pipenv") to manage dependencies, 
please install it first before you start. 

### Clone and Setup 
```shell
$ git clone 
$ cd LittleGolemCralwer
$ pipenv update
```
### Usage
Crawl the website and store the result through `%OutputFile%`
```
$ scrapy crawl LG -o %%
```
e.g.:
```
$ scrapy crawl LG -o result.json
```

