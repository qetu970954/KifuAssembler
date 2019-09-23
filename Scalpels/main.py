from Scalpels.extractor import Extractor
from .LGSgfParser import LGSgfParser
from .incorporator import Incorporator

if __name__ == '__main__':
    name = input("Select a json file to merge: >>>\n")
    sgfs = Extractor().extract(f"resources/{name}", "content")
    urls = Extractor().extract(f"resources/{name}", "url")

    incorporator = Incorporator()

    for sgf, url in zip(sgfs, urls):
        moves = LGSgfParser.parse(sgf)
        incorporator.incorporate(moves, url)

    with open("merge.sgf", "w") as f:
        f.write(incorporator.to_sgf())
