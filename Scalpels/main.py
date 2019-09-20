from Scalpels.extractor import Extractor
from .LGSgfParser import LGSgfParser
from .incorporator import Incorporator

if __name__ == '__main__':
    sgfs = Extractor().extract("resources/Lomaben.json", "content")
    moves = [LGSgfParser.parse(sgf) for sgf in sgfs]
    incorporator = Incorporator()

    print(len(moves))
    for mv in moves:
        incorporator.incorporate(mv)

    with open("merge.sgf", "w") as f:
        f.write(incorporator.to_sgf())
