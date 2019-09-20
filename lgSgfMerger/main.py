import json

from .LGSgfParser import LGSgfParser
from .incorporator import Incorporator

if __name__ == '__main__':
    with open("resources/Lomaben.json") as f:
        data = json.load(f)
        sgfs = [chunk["content"] for chunk in data]
        moves = [LGSgfParser.parse(sgf) for sgf in sgfs]
        incorporator = Incorporator()
        print(len(moves))
        for mv in moves:
            incorporator.incorporate(mv)

        with open("merge.sgf", "w") as f:
            f.write(incorporator.to_sgf())
