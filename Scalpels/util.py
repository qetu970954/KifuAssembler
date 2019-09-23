# Reference website of generating class that support equality : https://ppt.cc/fusdrx

class Root:
    """
    >>> Root() == Root()
    True
    """

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __str__(self) -> str:
        return ""


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
        return f"W[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]"


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
        return f"B[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]"


class WhiteMoveWithComment(WhiteMove):
    """
    >>> WhiteMoveWithComment(3, 4, comment="Foo") == WhiteMoveWithComment(3, 4, comment="Foo")
    True

    # Note that different comment message but with same i and j are consider equal
    >>> WhiteMoveWithComment(3, 4, comment="Foo") == WhiteMoveWithComment(3, 4, comment="Bar")
    True

    # If i or j varies, then is consider not equil
    >>> WhiteMoveWithComment(3, 4, comment="Foo") == WhiteMoveWithComment(3, 5, comment="Bar")
    False
    """

    def __init__(self, i, j, *, visit_cnt=0, comment=""):
        super().__init__(i, j, visit_cnt=visit_cnt)
        self.comment = comment

    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self) -> str:
        return f"W[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]C[{self.comment}]"


class BlackMoveWithComment(BlackMove):
    """
    >>> BlackMoveWithComment(3, 4, comment="Foo") == BlackMoveWithComment(3, 4, comment="Foo")
    True

    # Note that different comment message but with same i and j are consider equal
    >>> BlackMoveWithComment(3, 4, comment="Foo") == BlackMoveWithComment(3, 4, comment="Bar")
    True

    # If i or j varies, then is consider not equal
    >>> BlackMoveWithComment(3, 4, comment="Foo") == BlackMoveWithComment(3, 5, comment="Bar")
    False
    """

    def __init__(self, i, j, *, visit_cnt=0, comment=""):
        super().__init__(i, j, visit_cnt=visit_cnt)
        self.comment = comment

    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self) -> str:
        return f"B[{'ABCDEFGHIJKLMNOPQRS'[self.i]}{'ABCDEFGHIJKLMNOPQRS'[self.j]}]C[{self.comment}]"
