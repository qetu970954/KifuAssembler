import argparse
import random
import datetime
import yaml
from pathlib import Path


def main():
    batch_of_actions = []
    batch_of_pis = []
    white_win_count = args.batch_size // 2
    black_win_count = args.batch_size - white_win_count

    for _ in range(white_win_count):
        start = random.randint(0, 13)
        white_c6 = list(range(start, start + 6))
        black_response = random.choices([i for i in range(361) if i not in white_c6 + [180]], k=4)
        actions = white_c6[:2] + black_response[:2] + white_c6[2:4] + black_response[2:4] + white_c6[4:]
        batch_of_actions.append(actions)
        pis = []
        for a in actions:
            pi = [0] * 361
            pi[a] = 1
            pis += [pi]
        batch_of_pis.append(pis)

    for _ in range(black_win_count):
        start = random.randint(0, 13)
        black_c6 = list(range(start, start + 6))
        white_response = random.choices([i for i in range(361) if i not in black_c6 + [180]], k=6)
        actions = white_response[:2] + black_c6[:2] + white_response[2:4] + black_c6[2:4] + white_response[
                                                                                            4:] + black_c6[4:]
        batch_of_actions.append(actions)
        pis = []
        for a in actions:
            pi = [0] * 361
            pi[a] = 1
            pis += [pi]
        batch_of_pis.append(pis)

    with Path(args.output_dir) \
            .joinpath(f"boarderkifusbuildat-{datetime.datetime.now().strftime('%b%d-%s%f')}_statistics.yml") \
            .open(mode="w") as f:
        yaml.safe_dump({"SimulationCount" : 0,
                        "BatchSize"       : args.batch_size,
                        "BWin/WWin/Draw"  : [black_win_count, white_win_count, 0],
                        "BatchOfPositions": batch_of_actions,
                        "BatchOfPis"      : batch_of_pis}, f, default_flow_style=None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate sgf that placed on the boarder")
    parser.add_argument("batch_size", help="Number of games inside this statistics", type=int)
    parser.add_argument("output_dir", help="The directory to output statistics")

    args = parser.parse_args()
    print(args)
    main()
