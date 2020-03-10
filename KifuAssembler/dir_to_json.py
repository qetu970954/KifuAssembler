# Helper script to grab multiple sgf files inside a directory and put them into a single json file.
# (so it can be "assembled" into a merged sgf)
import pathlib
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="The directory that stores sgf files.")
parser.add_argument("output_directory", help="The output directory that stores the json file.")
parser.add_argument("-czf", action='store_true', help="Input sgf files are generate by nctu6_compete")
parser.add_argument("--name", default="result.json", help="The json output.")

if __name__ == '__main__':
    args = parser.parse_args()
    if not pathlib.Path(args.input_directory).exists():
        print("The input directory does not exists!")

    result = []
    for sgf in pathlib.Path(args.input_directory).glob("*.sgf"):
        with sgf.open('r') as f:
            if args.czf:
                text = sgf.read_text()[:37]
                text += ";B[jj]"
                text += sgf.read_text()[37:]
                if sgf.name[-12: -4] == "BlackWin":
                    result.append({"kifu": text, "url": "", "game_result": "BWin"})
                elif sgf.name[-12: -4] == "WhiteWin":
                    result.append({"kifu": text, "url": "", "game_result": "WWin"})
            else:
                result.append({"kifu": sgf.read_text(), "url": "", "game_result": "None"})

    with (pathlib.Path(args.output_directory) / args.name).open("w") as json_file:
        json.dump(result, json_file, indent=4)