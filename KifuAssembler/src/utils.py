"""
Node-Type
"""
import copy
from collections import defaultdict


class Root:
    """
    >>> Root() == Root()
    True
    """

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __str__(self) -> str:
        return ""


class BlackMove:
    """
    >>> BlackMove(3, 4) == BlackMove(3, 4)
    True
    >>> BlackMove(3, 4) == BlackMove(3, 5)
    False
    """

    def __init__(self, i, j, *, visit_cnt=0):
        self.i = i
        self.j = j
        self.visit_cnt = visit_cnt

    def __eq__(self, other):
        return other and self.i == other.i and self.j == other.j

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"B[{'abcdefghijklmnopqrs'[self.i]}{'abcdefghijklmnopqrs'[self.j]}]"

    def __hash__(self):
        return hash((self.i, self.j))


class WhiteMove:
    """
    >>> WhiteMove(1, 2) == WhiteMove(1, 2)
    True
    >>> WhiteMove(1, 2) == WhiteMove(1, 0)
    False
    """

    def __init__(self, i, j, *, visit_cnt=0):
        self.i = i
        self.j = j
        self.visit_cnt = visit_cnt

    def __eq__(self, other):
        return other and self.i == other.i and self.j == other.j

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"W[{'abcdefghijklmnopqrs'[self.i]}{'abcdefghijklmnopqrs'[self.j]}]"

    def __hash__(self):
        return hash((self.i, self.j))


def gogui_style_str(move):
    if isinstance(move, BlackMove):
        return f"B[{'abcdefghijklmnopqrs'[move.i]}{'srqponmlkjihgfedcba'[move.j]}]"
    elif isinstance(move, WhiteMove):
        return f"W[{'abcdefghijklmnopqrs'[move.i]}{'srqponmlkjihgfedcba'[move.j]}]"
    else:
        return ""


def do_nothing(a_move):
    return copy.copy(a_move)


def rotate_90(a_move):
    result = copy.copy(a_move)
    result.i, result.j = a_move.j, a_move.i
    result.j = 18 - result.j
    return result


def rotate_180(a_move):
    result = copy.copy(a_move)
    result.i = 18 - result.i
    result.j = 18 - result.j
    return result


def rotate_270(a_move):
    result = copy.copy(a_move)
    result.i, result.j = result.j, result.i
    result.i = 18 - result.i
    return result


def horizontal_reflect(a_move):
    result = copy.copy(a_move)
    result.j = 18 - result.j
    return result


def horizontal_reflect_rotate_90(a_move):
    return rotate_90(horizontal_reflect(a_move))


def horizontal_reflect_rotate_180(a_move):
    return rotate_180(horizontal_reflect(a_move))


def horizontal_reflect_rotate_270(a_move):
    return rotate_270(horizontal_reflect(a_move))


def build_symmetric_lookup_table():
    symmetric_lookup = defaultdict(list)

    for x in range(9, -1, -1):
        for y in range(x, -1, -1):
            bm = BlackMove(x, y)

            new_bm = horizontal_reflect_rotate_270(bm)
            symmetric_lookup[(new_bm.i, new_bm.j)].append(horizontal_reflect_rotate_270)

            new_bm = horizontal_reflect_rotate_180(bm)
            symmetric_lookup[(new_bm.i, new_bm.j)].append(horizontal_reflect_rotate_180)

            new_bm = horizontal_reflect_rotate_90(bm)
            symmetric_lookup[(new_bm.i, new_bm.j)].append(horizontal_reflect_rotate_90)

            new_bm = horizontal_reflect(bm)
            symmetric_lookup[(new_bm.i, new_bm.j)].append(horizontal_reflect)

            new_bm = rotate_270(bm)
            symmetric_lookup[(new_bm.i, new_bm.j)].append(rotate_90)

            new_bm = rotate_180(bm)
            symmetric_lookup[(new_bm.i, new_bm.j)].append(rotate_180)

            new_bm = rotate_90(bm)
            symmetric_lookup[(new_bm.i, new_bm.j)].append(rotate_270)

            new_bm = do_nothing(bm)
            symmetric_lookup[(new_bm.i, new_bm.j)].append(do_nothing)

    return symmetric_lookup
