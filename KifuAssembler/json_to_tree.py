# Assemble kifus inside the json files into a sgf tree
import argparse
import os

import tqdm

from KifuAssembler.src.extractor import Extractor
from KifuAssembler.src.incorporator import Incorporator, KifuParser, dump_to

parser = argparse.ArgumentParser(description="Assemble kifus to a kifu tree.")

parser.add_argument('json_src',
    type=str,
    help="The source 'json' path to extract kifu from."
)

parser.add_argument('output_file',
    type=str,
    help="The location to output assembled tree.",
    default="results/result.sgf"
)

parser.add_argument('-s', '--enable_symmetrically_assemble',
    action='store_true',
    help="View symmetrical sgfs as identical."
)

parser.add_argument('-l', '--moves_lower_bound',
    type=int,
    default=10,
    help="Do NOT take moves which 'len(moves) < $l' into account."
)

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.exists(args.json_src):
        print("Error! The json src file \'{}\' does not exist!".format(args.json_src))
        exit(1)

    kifus = Extractor().extract(args.json_src, "kifu")
    urls = Extractor().extract(args.json_src, "url")
    game_results = Extractor().extract(args.json_src, "game_result")

    print("Assembling to a tree...")
    incorporator = Incorporator(symmetric=args.enable_symmetrically_assemble)
    with tqdm.tqdm(total=len(kifus)) as pbar:
        for kifu, url, game_results in zip(kifus, urls, game_results):
            # Use Kifuparser to parse the raw string into sequence of move
            moves = KifuParser.parse(kifu)
            if len(moves) < args.moves_lower_bound:
                continue

            # Use incorporator to incorporate moves into the tree
            incorporator.incorporate(moves, url, game_results)
            pbar.update(1)

    print(f"'{pbar.total - pbar.n}' kifus are skipped.\n")

    print(f"Writing to file '{args.output_file}'...>")
    with open(args.output_file, "w") as f:
        dump_to(incorporator, f)
