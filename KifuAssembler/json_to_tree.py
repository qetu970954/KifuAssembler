# Assemble kifus inside the json files into a sgf tree
import argparse
import tqdm

from KifuAssembler.src.extractor import Extractor
from KifuAssembler.src.incorporator import Incorporator, KifuParser

parser = argparse.ArgumentParser(description="Assemble kifus to a kifu tree.")
parser.add_argument('json_src', type=str, help="The source json path to extract kifu from.")
parser.add_argument('output_file', type=str, help="The location to output assembled tree.", default="results/result.sgf")
parser.add_argument('--enable_symmetric_assemble', action='store_true', help="View symmetrical moves as the same. "
                                                                          "Default: Not set.")

if __name__ == '__main__':
    args = parser.parse_args()

    kifus = Extractor().extract(args.json_src, "kifu")
    urls = Extractor().extract(args.json_src, "url")
    game_results = Extractor().extract(args.json_src, "game_result")

    print(args)
    incorporator = Incorporator(symmetric=args.enable_symmetric_assemble)

    with tqdm.tqdm(total=len(kifus)) as pbar:
        for kifu, url, game_results in zip(kifus, urls, game_results):
            # Use Kifuparser to parse the raw string into sequence of move
            moves = KifuParser.parse(kifu)
            # Use incorporator to incorporate moves into the tree
            incorporator.incorporate(moves, url, game_results)
            pbar.update(1)

    print(f"Writing to file '{args.output_file}'...>")
    with open(args.output_file, "w") as f:
        f.write(incorporator.to_sgf())
