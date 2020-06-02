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
            working_dir = Path(config["working_dir"]["root"])

            try:
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

            print(f"First move is : {mv1}. Second move is : {mv2}, last player has winrate {winrate}")

            # Get the table for converting czf moves to little Golem compatible moves
            table = get_convert_table()
            print(f"Sending {table[mv1]}{table[mv2]} to gid={gid}")

            requests.post('https://www.littlegolem.net/jsp/game/game.jsp',
                params={"sendgame": f"{gid}", "sendmove": f"{table[mv1]}{table[mv2]}"},
                cookies=player_cookies
            )

            text_output_dir = Path(config["game_text_output_dir"])
            text_output_dir.mkdir(exist_ok=True, parents=True)
            with text_output_dir.joinpath(f"{gid}.txt").open("a+") as f:
                print(f"{table[mv1]}, {table[mv2]}, {winrate}", file=f)


if __name__ == '__main__':
    with open("miscellaneous/lg_uploader_config.yml", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    while True:
        main()
        print("Sleeping...")
        for _ in tqdm.tqdm(range(config["poll_seconds"])):
            sleep(1)