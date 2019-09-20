from dataclasses import dataclass


@dataclass(frozen=True)
class Root:
    def __str__(self) -> str:
        return ""


@dataclass(frozen=True)
class WhiteMove:
    i: int = 0
    j: int = 0

    def __str__(self) -> str:
        return f"W[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]"


@dataclass(frozen=True)
class BlackMove:
    i: int = 0
    j: int = 0

    def __str__(self) -> str:
        return f"B[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]"


@dataclass(frozen=True)
class WhiteMoveWithComment(BlackMove):
    comment: str = ""

    def __str__(self) -> str:
        return f"W[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]C[{self.comment}]"


@dataclass(frozen=True)
class BlackMoveWithComment(BlackMove):
    comment: str = ""

    def __str__(self) -> str:
        return f"B[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]C[{self.comment}]"
