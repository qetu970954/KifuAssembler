from NODETYPES import BlackMove, WhiteMove, Root
from incorporator import Incorporator


def test_Ctor_WithValidMoves_ReturnsCorrectPreOrderTraversalTuple():
    moves = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11), ]

    incorporator = Incorporator(moves)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(10, 10),
                WhiteMove(0, 0),
                BlackMove(10, 11))

    assert actual == expected
    assert type(actual) == tuple


def test_Incorporate_DifferentMoves_ReturnsCorrectPreOrderTraversalTuple_0():
    moves1 = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11), ]
    moves2 = [BlackMove(10, 10), WhiteMove(1, 1), BlackMove(10, 11), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(10, 10),
                WhiteMove(0, 0), BlackMove(10, 11),
                WhiteMove(1, 1), BlackMove(10, 11),)

    assert actual == expected


def test_Incorporate_DifferentMoves_ReturnsCorrectPreOrderTraversalTuple_1():
    moves1 = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11), ]
    moves2 = [BlackMove(11, 10), WhiteMove(1, 1), BlackMove(10, 11), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11),
                BlackMove(11, 10), WhiteMove(1, 1), BlackMove(10, 11),)

    assert actual == expected


def test_Incorporate_DifferentMoves_ReturnsCorrectPreOrderTraversalTuple_2():
    moves1 = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11), ]
    moves2 = [BlackMove(11, 10), WhiteMove(1, 1), BlackMove(10, 11), ]
    moves3 = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(11, 12), WhiteMove(3, 4), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)
    incorporator.incorporate(moves3)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11),
                BlackMove(11, 12), WhiteMove(3, 4),
                BlackMove(11, 10), WhiteMove(1, 1), BlackMove(10, 11),)

    assert actual == expected


def test_Incorporate_Nothing_ReturnsCorrectPreOrderTraversalTuple():
    incorporator = Incorporator()
    incorporator.incorporate([])

    actual = incorporator.to_tuple()
    expected = (Root(),)

    assert actual == expected


def test_ToSgf_NormalCase_ReturnsCorrectSgf():
    moves1 = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11), ]
    moves2 = [BlackMove(10, 10), WhiteMove(1, 1), BlackMove(10, 11), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_sgf()
    expected = ";B[JJ](;W[AA];B[JK])(;W[BB];B[JK])"

    assert actual == expected
