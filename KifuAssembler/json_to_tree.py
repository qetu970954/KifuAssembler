# Assemble kifus inside a json files to a sgf tree
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

parser.add_argument('-s', '--enable_symmetrical_assembling',
    action='store_true',
    help="View symmetrical sgfs as the same."
)

parser.add_argument('-l', '--lower_bound',
    type=int,
    default=5,
    help="Ignore moves which has length smaller than this flag."
)

parser.add_argument('-c6',
    action='store_true',
    help="Use connect6 merge rule (i.e., (W0, W1) and (W1, W0) are considered interchangeable)."
)

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.exists(args.json_src):
        print(f"Error! The json src file {args.json_src} does not exist!")
        exit()

    kifus = Extractor().extract(args.json_src, "kifu")
    urls = Extractor().extract(args.json_src, "url")
    game_results = Extractor().extract(args.json_src, "game_result")

    print("Assembling to a tree...")
    incorporator = Incorporator(
        merge_symmetric_moves=args.enable_symmetrical_assembling,
        use_c6_merge_rules=args.c6
    )
    with tqdm.tqdm(total=len(kifus)) as pbar:
        for kifu, url, game_results in zip(kifus, urls, game_results):
            # Use Kifuparser to parse the raw string into sequence of move
            moves = KifuParser.parse(kifu)
            if len(moves) < args.lower_bound:
                continue

            # Use incorporator to incorporate moves into the tree
            incorporator.incorporate(moves, url, game_results)
            pbar.update(1)

    print(f"'{pbar.total - pbar.n}' kifus are skipped because it has too few moves.\n")

    print(f"Writing to file '{args.output_file}'...>")
    with open(args.output_file, "w") as f:
        dump_to(incorporator, f, editor_style=args.c6)
