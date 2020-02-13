"""
Node-Type
"""


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
        return isinstance(other, self.__class__) and self.i == other.i and self.j == other.j

    def __str__(self) -> str:
        return f"B[{'abcdefghijklmnopqrs'[self.i]}{'abcdefghijklmnopqrs'[self.j]}]"


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
        return isinstance(other, self.__class__) and self.i == other.i and self.j == other.j

    def __str__(self) -> str:
        return f"W[{'abcdefghijklmnopqrs'[self.i]}{'abcdefghijklmnopqrs'[self.j]}]"


def gogui_style_str(move):
    if isinstance(move, BlackMove):
        return f"B[{'abcdefghijklmnopqrs'[move.i]}{'srqponmlkjihgfedcba'[move.j]}]"
    elif isinstance(move, WhiteMove):
        return f"W[{'abcdefghijklmnopqrs'[move.i]}{'srqponmlkjihgfedcba'[move.j]}]"
    else:
        return ""
