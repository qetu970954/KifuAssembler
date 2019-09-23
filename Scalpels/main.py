from Scalpels.extractor import Extractor
from .LGSgfParser import LGSgfParser
from .incorporator import Incorporator

if __name__ == '__main__':
    sgfs = Extractor().extract("resources/SmallLomaben.json", "content")
    urls = Extractor().extract("resources/SmallLomaben.json", "url")

    moves = [(LGSgfParser.parse(sgf, url + "\n")) for sgf, url in zip(sgfs, urls)]

    incorporator = Incorporator()

    for mv in moves:
        incorporator.incorporate(mv)

    with open("merge.sgf", "w") as f:
        f.write(incorporator.to_sgf())
