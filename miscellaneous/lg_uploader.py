import re
import subprocess
from itertools import product
from pathlib import Path
from time import sleep

import requests
import tqdm
import yaml
from scrapy.selector import Selector

from KifuAssembler.src.utils import KifuParser
from KifuAssembler.src.incorporator import to_Pure_sgf


def get_convert_table():
    # Build lookup table that convert CZF moves into Little Golem moves
    upper_to_lower = {}
    for i, j in zip("ABCDEFGHJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxy"):
        upper_to_lower[i] = j

    convert_table = {}
    for i, j in product("ABCDEFGHJKLMNOPQRSTUVWXYZ", range(1, 20)):
        convert_table[f"{i}{j}"] = upper_to_lower[i] + "abcdefghijklmnopqrstuvwxy"[j - 1]

    return convert_table


def GetNCTU6Result(sgf):
    print(f'Let NCTU6 think "{sgf}"')

    nctu6_working_dir = Path(config["nctu6_working_dir"])

    proc = subprocess.Popen(
        ['podman', 'run', '-i', '--rm',
         f'-e=NVIDIA_VISIBLE_DEVICES={config["gpu_id"]}',
         f'-v={nctu6_working_dir.as_posix()}:/work',
         '-w=/work', 'czf',
         f'wine',
         f'NCTU6.exe',
         f'-playtsumego',
         to_Pure_sgf(sgf)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf-8", bufsize=1
    )

    try:
        proc.wait()

    except KeyboardInterrupt:
        proc.terminate()
        return

    nctu6_outputs = proc.stdout.readline().split(';')

    print(f"nctu6_output is {nctu6_outputs}")

    if nctu6_outputs[3] in ["C[B:w]", "C[B:a_w]"] and nctu6_outputs[1][0] == "B":
        print("NCTU6 says black win")
        return nctu6_outputs[1][2:4].lower(), nctu6_outputs[2][2:4].lower()

    elif nctu6_outputs[3] in ["C[W:w]", "C[W:a_w]"] and nctu6_outputs[1][0] == "W":
        print("NCTU6 says white win")
        return nctu6_outputs[1][2:4].lower(), nctu6_outputs[2][2:4].lower()
    else:
        return None, None


def GetCZFResult(sgf):
    moves = KifuParser.parse(sgf)[1:]  # Ignore first move, usually B[JJ], because czf already placed it.

    # Launch czf for competition
    working_dir = Path(config["working_dir"]["root"])

    proc = subprocess.Popen(
        ['podman', 'run', '-i', '--rm',
         f'-e=NVIDIA_VISIBLE_DEVICES={config["gpu_id"]}',
         f'-v={working_dir.as_posix()}:/work',
         '-w=/work', 'czf',
         f'./{config["working_dir"]["ai_path"]}/ai',
         f'./{config["working_dir"]["network_path"]}/latest.weight',
         f'./{config["working_dir"]["network_path"]}/latest.model',
         f'{config["sim_cnt"]}'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf-8", bufsize=1
    )

    try:
        # Convert moves to czf compatible moves, and feed into the process
        for str_mv in ["ABCDEFGHJKLMNOPQRSTUVWXYZ"[mv.i] + str(mv.j + 1) for mv in moves]:
            proc.stdin.write(f"play d {str_mv}\n")

        # Let czf compute think two moves
        proc.stdin.write("c6genmove\n")
        proc.stdin.write("winrate_of_lastplayer\n")
        proc.stdin.write("quit\n")
        proc.stdin.flush()
        out, _ = proc.communicate()

    except KeyboardInterrupt:
        proc.terminate()
        return

    mvs, winrate = [line[2:] for line in out.splitlines() if line[2:]]
    mv1, mv2 = mvs.split("_and_")

    # Get the table for converting czf moves to little Golem compatible moves
    table = get_convert_table()
    mv1, mv2 = table[mv1], table[mv2]
    return mv1, mv2, winrate


def main():
    payload = {'login'   : config['login'],
               'password': config['password']}

    with requests.Session() as sess:
        player_cookies = sess.post("http://www.littlegolem.net/jsp/login/", data=payload).cookies

        # Fetch games need to played
        r = requests.get("https://www.littlegolem.net/jsp/game/", cookies=player_cookies)

        games_to_play = str(
            Selector(text=r.text).css(
                ".blue-madison > div:nth-child(2) > div:nth-child(1) > table:nth-child(1) > tbody").get()
        )

        game_ids = re.findall("gid=[0-9]*", games_to_play)  # Regular expression search for game ids

        # For each gam:
        #   step1. Forward it to NCTU6, let it assess if there is a direct win. If it is, return NCTU6's move to LG
        #   step2. Otherwise, launch CZF to calculate the next move
        for gid in tqdm.tqdm(game_ids):
            gid = gid[4:]  # Pick up the id part
            print(f"Gameid is {gid}")

            sgf = requests.get(f'http://www.littlegolem.net/servlet/sgf/{gid}/game{gid}.txt').text

            mv1, mv2 = GetNCTU6Result(sgf)
            if mv1 and mv2:
                print(f"NCTU6's assessment is : mv1 = {mv1}, mv2 = {mv2}")
                winrate = "proven"

            else:
                mv1, mv2, winrate = GetCZFResult(sgf)
                print(f"CZF's assessment is : mv1 = {mv1}, mv2 = {mv2}")

            print(f"First move is : {mv1}. Second move is : {mv2}, last player has winrate {winrate}")

            print(f"Sending {mv1}{mv2} to gid={gid}")

            requests.post('https://www.littlegolem.net/jsp/game/game.jsp',
                params={"sendgame": f"{gid}", "sendmove": f"{mv1}{mv2}"},
                cookies=player_cookies
            )

            text_output_dir = Path(config["game_text_output_dir"])
            text_output_dir.mkdir(exist_ok=True, parents=True)
            with text_output_dir.joinpath(f"{gid}.txt").open("a+") as f:
                print(f"{mv1}, {mv2}, {winrate}", file=f)


if __name__ == '__main__':
    with open("miscellaneous/lg_uploader_config.yml", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    while True:
        main()
        print("Sleeping...")
        for _ in tqdm.tqdm(range(config["poll_seconds"])):
            sleep(1)
