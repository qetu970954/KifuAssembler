from Scalpels.incorporator import Incorporator
from Scalpels.util import BlackMove, WhiteMove, Root, WhiteMoveWithComment


def test_Ctor_WithValidMoves_ReturnsCorrectPreOrderTraversalTuple():
    moves = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]

    incorporator = Incorporator(moves)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0),
                WhiteMove(0, 1),
                BlackMove(0, 2))

    assert actual == expected
    assert type(actual) == tuple


def test_Incorporate_DifferentMoves_ReturnsCorrectPreOrderTraversalTuple_0():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(0, 0), WhiteMove(1, 1), BlackMove(0, 2), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0),
                WhiteMove(0, 1), BlackMove(0, 2),
                WhiteMove(1, 1), BlackMove(0, 2),)

    assert actual == expected


def test_Incorporate_DifferentMoves_ReturnsCorrectPreOrderTraversalTuple_1():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(1, 0), WhiteMove(1, 1), BlackMove(0, 2), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2),
                BlackMove(1, 0), WhiteMove(1, 1), BlackMove(0, 2),)

    assert actual == expected


def test_Incorporate_DifferentMoves_ReturnsCorrectPreOrderTraversalTuple_2():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(0, 0), WhiteMove(0, 2), BlackMove(0, 1), ]
    moves3 = [BlackMove(0, 0), WhiteMove(0, 2), BlackMove(0, 3), WhiteMove(0, 4), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)
    incorporator.incorporate(moves3)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2),
                WhiteMove(0, 2), BlackMove(0, 1),
                BlackMove(0, 3), WhiteMove(0, 4),)

    assert actual == expected


def test_Incorporate_DifferentMoves_ReturnsCorrectPreOrderTraversalTuple_3():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(0, 0), WhiteMove(0, 2), BlackMove(0, 1), ]
    moves3 = [BlackMove(0, 0), WhiteMove(0, 2), BlackMove(0, 3), WhiteMove(0, 4), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)
    incorporator.incorporate(moves3)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2),
                WhiteMove(0, 2), BlackMove(0, 1),
                BlackMove(0, 3), WhiteMove(0, 4),)

    assert actual == expected


def test_Incorporate_Nothing_ReturnsCorrectPreOrderTraversalTuple():
    incorporator = Incorporator()
    incorporator.incorporate([])

    actual = incorporator.to_tuple()
    expected = (Root(),)

    assert actual == expected


def test_ToSgf_NormalCase_ReturnsCorrectSgf():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), ]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 10), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_sgf()
    expected = ";B[JJ](;W[IK];W[KK])(;W[II];W[JK])"

    assert actual == expected


def test_ToSgf_NormalCase_ReturnsCorrectSgf_2():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(9, 10), BlackMove(9, 11)]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(10, 9), BlackMove(11, 9)]
    moves3 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 10), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)
    incorporator.incorporate(moves3)

    actual = incorporator.to_sgf()
    expected = ";B[JJ](;W[IK];W[KK](;B[JK];B[JL])(;B[KJ];B[LJ]))(;W[II];W[JK])"

    assert actual == expected


def test_ToSgf_WithComment_ReturnsCorrectSgf():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMoveWithComment(10, 10, "SAMPLE_URL"), ]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 10), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_sgf()
    expected = ";B[JJ](;W[IK];W[KK]C[SAMPLE_URL])(;W[II];W[JK])"

    assert actual == expected
