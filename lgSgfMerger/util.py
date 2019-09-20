import typing


class Root(typing.NamedTuple):
    def __str__(self) -> str:
        return ""


class WhiteMove(typing.NamedTuple):
    i: int = 0
    j: int = 0

    def __str__(self) -> str:
        return f"W[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]"


class BlackMove(typing.NamedTuple):
    i: int = 0
    j: int = 0

    def __str__(self) -> str:
        return f"B[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]"

