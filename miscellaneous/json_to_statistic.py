# Note: This file make sense only if you're familiar with CZF! And only works for the game "Connect6"

# This script will mimic the Little Golem experts and, make a bunch of Cgilab Zero Framework's selfplay statistics.
# These statistics then, can be converted to training data for optimizing models.

import datetime
import argparse
import yaml
from pathlib import Path
from KifuAssembler.src.extractor import Extractor
from KifuAssembler.src.utils import KifuParser
from collections import Counter, namedtuple
from concurrent.futures import ProcessPoolExecutor


def dump_to_yml(args, result_counter, batch_of_actions, batch_of_pis):
    with Path(args.output_dir) \
            .joinpath(f"expertkifusbuildat-{datetime.datetime.now().strftime('%b%d-%s%f')}_statistics.yml") \
            .open(mode="w") as f:
        yaml.safe_dump({"SimulationCount" : 0,
                        "BatchSize"       : args.batch_size,
                        "BWin/WWin/Draw"  : [result_counter["BWin"], result_counter["WWin"],
                                             result_counter["Draw"]],
                        "BatchOfPositions": batch_of_actions,
                        "BatchOfPis"      : batch_of_pis}, f, default_flow_style=None)


def main():
    args = parser.parse_args()

    kifus = Extractor().extract(args.input_json, "kifu")
    game_results = Extractor().extract(args.input_json, "game_result")

    k_r_pairs = []  # 'K'ifu_'R'esult_pairs
    for k, g in zip(kifus, game_results):
        k_r_pairs.append(Pair(k, g))

    print(f"There are {len(k_r_pairs)} of kifus in the given json file.")

    Path(args.output_dir).resolve().mkdir(parents=True, exist_ok=True)

    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = []

        while True:
            if len(k_r_pairs) < args.batch_size:
                break

            result_counter = Counter(BWin=0, WWin=0, Draw=0)
            batch_of_positions = []
            batch_of_pis = []

            for _ in range(args.batch_size):
                pair = k_r_pairs.pop(-1)

                result_counter[pair.result] += 1

                moves = KifuParser.parse(pair.kifu)[1::]

                # We assumed the first move is B[JJ], so we discard it because it is automatically placed on the center.
                batch_of_positions.append([mv.i + mv.j * 19 for mv in moves])

                pis = []
                for mv in moves:
                    pi = [0.0] * 361  # Create policy, a vector with length = 361.
                    pi[mv.i + mv.j * 19] = 1.0  # Directly set the corresponding coordinate to 1.0
                    pis.append(pi)
                batch_of_pis.append(pis)

            future = pool.submit(dump_to_yml, args, result_counter, batch_of_positions, batch_of_pis)
            futures.append(future)

        print("patience...")
        for f in futures:
            f.result()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse json file crawled from LG into statistics")
    parser.add_argument("batch_size", help="Number of games contained for each statistic files", type=int)
    parser.add_argument("input_json", help="The json file to see")
    parser.add_argument("output_dir", help="The directory to output statistics")
    parser.add_argument("-w", "--workers", help="Number of workers available (for parallel execution).",
        default=4,
        type=int
    )

    Pair = namedtuple("Pair", ["kifu", "result"])
    main()
