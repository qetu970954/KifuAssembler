from collections import namedtuple

Root = namedtuple("Root", [])

BlackMove = namedtuple("BlackMove", ["i", "j"], defaults=(0, 0,))
WhiteMove = namedtuple("WhiteMove", ["i", "j"], defaults=(0, 0,))


def sgf_view(move):
    if isinstance(move, Root):
        return ""

    result = ""
    if isinstance(move, BlackMove):
        result += "B["
    elif isinstance(move, WhiteMove):
        result += "W["
    else:
        raise Exception("Unknown move type!")

    result += "ABCDEFGHIJKLMNOPQRS"[move.i]
    result += "ABCDEFGHIJKLMNOPQRS"[move.j]
    result += ']'

    return result
