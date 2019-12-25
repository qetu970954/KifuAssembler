# Helper script to grab multiple sgf files inside a directory and put them into a single json file.
# (so it can be "assembled" into a merged sgf)
import pathlib
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="The directory that stores sgf files.")
parser.add_argument("output_directory", help="The output directory that stores the json file.")
parser.add_argument("--name", default="result.json", help="The json output.")

if __name__ == '__main__':
    args = parser.parse_args()

    result = []
    for sgf in pathlib.Path(args.input_directory).glob("*.sgf"):
        with sgf.open('r') as f:
            result.append({"kifu": sgf.read_text(), "url": ""})

    with (pathlib.Path(args.output_directory) / args.name).open("w") as json_file:
        json.dump(result, json_file)
