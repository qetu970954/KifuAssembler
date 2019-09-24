import argparse
import os

from KifuAssembler.extractor import Extractor
from KifuAssembler.incorporator import Incorporator, KifuParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Assemble kifus to a kifu tree.")
    parser.add_argument('-s', '--src_file_path', type=str, help="The source file path to extract kifu from.")
    parser.add_argument('-o', '--output_file_path', type=str, help="The merged kifu's output path.",
        default="results/result.sgf")

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
