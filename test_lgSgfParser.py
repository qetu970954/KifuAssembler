from itertools import product

from util import BlackMove, WhiteMove


lgSgf_to_location = {}
for i, j in product("abcdefghijklmnopqrs", range(1, 20)):
    lgSgf_to_location[f"{i}{j}"] = ("abcdefghijklmnopqrs".index(i), j - 1)

for i, j, i2, j2 in product("abcdefghijklmnopqrs", range(1, 20), "abcdefghijklmnopqrs", range(1, 20)):
    lgSgf_to_location[f"{i}{j}{i2}{j2}"] = \
        ("abcdefghijklmnopqrs".index(i), j - 1, "abcdefghijklmnopqrs".index(i2), j2 - 1)

def parse(lg_sgf: str):
    # Split lg_sgf by ';' and discard the element if it is empty.
    moves = [e for e in lg_sgf[1:-1].split(';') if e]
    moves.pop(0)
    result = []
    for move in moves:
        role = move[0]
        if role == 'B':
            if len(lgSgf_to_location[move[2:-1]]) == 2:
                i, j = lgSgf_to_location[move[2:-1]]
                result.append(BlackMove(i, j))
            elif len(lgSgf_to_location[move[2:-1]]) == 4:
                i1, j1, i2, j2 = lgSgf_to_location[move[2:-1]]
                result.append(BlackMove(i1, j1))
                result.append(BlackMove(i2, j2))

        elif role == 'W':
            if len(lgSgf_to_location[move[2:-1]]) == 2:
                i, j = lgSgf_to_location[move[2:-1]]
                result.append(WhiteMove(i, j))
            elif len(lgSgf_to_location[move[2:-1]]) == 4:
                i1, j1, i2, j2 = lgSgf_to_location[move[2:-1]]
                result.append(WhiteMove(i1, j1))
                result.append(WhiteMove(i2, j2))

    return result


def test_lgSgfParser_LG_ReturnsCorrectMoves():
    sample_sgf = "(;FF[4]EV[connect6.ch.26.1.1]PB[Phoenix]PW[Lomaben]SO[http://www.littlegolem.com];B[j10];W[j9l11];" \
                 "B[k9l8];W[k10i11])"

    actual = parse(sample_sgf)
    expected = [BlackMove(9, 9),
                WhiteMove(9, 8),
                WhiteMove(11, 10),
                BlackMove(10, 8),
                BlackMove(11, 7),
                WhiteMove(10, 9),
                WhiteMove(8, 10), ]

    assert actual == expected
