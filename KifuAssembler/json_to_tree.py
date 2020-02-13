# Assemble kifus inside the json files into a sgf tree
import argparse

from KifuAssembler.src.extractor import Extractor
from KifuAssembler.src.incorporator import Incorporator, KifuParser

parser = argparse.ArgumentParser(description="Assemble kifus to a kifu tree.")
parser.add_argument('-s', '--json_src', type=str, help="The source json path to extract kifu from.")
parser.add_argument('-o', '--output_file', type=str, help="The location to output merged tree.",
    default="results/result.sgf")

if __name__ == '__main__':
    args = parser.parse_args()

    kifus = Extractor().extract(args.src_file_path, "kifu")
    urls = Extractor().extract(args.src_file_path, "url")

    incorporator = Incorporator()

    for kifu, url in zip(kifus, urls):
        # Use Kifuparser to parse the raw string into sequence of move
        moves = KifuParser.parse(kifu)
        # Use incorporator to incorporate moves into the tree
        incorporator.incorporate(moves, url)

    with open(args.output_file_path, "w") as f:
        f.write(incorporator.to_sgf())
