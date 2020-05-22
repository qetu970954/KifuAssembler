import re
import subprocess
from itertools import product
from time import sleep

import requests
import tqdm
import yaml
from scrapy.selector import Selector

from KifuAssembler.src.utils import KifuParser


def main():
    def get_convert_table():
        # Build lookup table from moves from CZF into Little Golem moves
        upper_to_lower = {}
        for i, j in zip("ABCDEFGHJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxy"):
            upper_to_lower[i] = j

        convert_table = {}
        for i, j in product("ABCDEFGHJKLMNOPQRSTUVWXYZ", range(1, 20)):
            convert_table[f"{i}{j}"] = upper_to_lower[i] + "abcdefghijklmnopqrstuvwxy"[j - 1]

        return convert_table


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

        for gid in tqdm.tqdm(game_ids):
            gid = gid[4:]  # Pick up the id part
            print(f"Gameid is {gid}")

            sgf = requests.get(f'http://www.littlegolem.net/servlet/sgf/{gid}/game{gid}.txt').text
            moves = KifuParser.parse(sgf)[1::]  # Ignore first move, usually B[JJ], because czf already placed it.

            # Launch czf for competition
            proc = subprocess.Popen(
                ['podman', 'run', '-i', '--rm',
                 f'-e=NVIDIA_VISIBLE_DEVICES={config["gpu_id"]}',
                 f'-v={config["working_dir"]}:/czf',
                 '-w=/czf', 'czf',
                 './ai', 'latest.weight', 'latest.model', f'{config["sim_cnt"]}'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf-8")

            # Convert moves to czf compatible moves, and feed into the process
            for str_mv in ["ABCDEFGHJKLMNOPQRSTUVWXYZ"[mv.i] + str(mv.j + 1) for mv in moves]:
                proc.stdin.write(f"play d {str_mv}\n")

            # Let czf compute think two moves
            proc.stdin.write("genmove\n")
            proc.stdin.write("genmove\n")
            proc.stdin.write("quit\n")
            proc.stdin.flush()
            out, _ = proc.communicate()

            # Grep results
            mv1, mv2 = re.findall("= [0-9A-Z]+", out)
            mv1, mv2 = mv1[2:], mv2[2:]
            print(f"First move is : {mv1}. Second move is : {mv2}.")

            # Get the table for converting czf moves to little Golem compatible moves
            table = get_convert_table()
            print(f"Sending {table[mv1]}{table[mv2]} to gid={gid}")

            requests.post('https://www.littlegolem.net/jsp/game/game.jsp',
                params={"sendgame": f"{gid}", "sendmove": f"{table[mv1]}{table[mv2]}"},
                cookies=player_cookies
            )


if __name__ == '__main__':
    with open("miscellaneous/lg_uploader_config.yml", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    while True:
        main()
        print("Sleeping...")
        for _ in tqdm.tqdm(range(config["poll_seconds"])):
            sleep(1)

