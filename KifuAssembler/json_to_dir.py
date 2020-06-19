import pathlib
import argparse
import tqdm

from KifuAssembler.src.extractor import Extractor
from KifuAssembler.src.assembler import to_GoGui_sgf

parser = argparse.ArgumentParser(
    description="See the contents in a json file, and make gogui-compatible sgfs file according to the content.")
parser.add_argument("input_json", help="The json file to see")
parser.add_argument("output_dir", help="The output directory that stores the sgf files.")

if __name__ == '__main__':
    args = parser.parse_args()
    p = pathlib.Path(args.output_dir)
    p.mkdir(exist_ok=True)

    kifus = Extractor().extract(args.input_json, "kifu")
    game_results = Extractor().extract(args.input_json, "game_result")

    with tqdm.tqdm(total=len(kifus)) as pbar:
        for idx, (kifu, result) in enumerate(zip(kifus, game_results)):
            with (p / pathlib.Path(f"{result}_{idx}.sgf")).open('w') as f:
                f.write(to_GoGui_sgf(kifu))
            pbar.update(1)
