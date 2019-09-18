from NodeTypes import BlackMove, WhiteMove, Root
from incorporator import Incorporator


def test_Ctor_ValidMoves_ReturnsCorrectPreOrderTraversalTuple():
    moves = [BlackMove(10, 10),
             WhiteMove(0, 0),
             BlackMove(10, 11)]

    incorporator = Incorporator(moves)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(10, 10),
                WhiteMove(0, 0),
                BlackMove(10, 11))

    assert actual == expected
    assert type(actual) == tuple


def test_Incorporate_ValidMoves_ReturnsCorrectPreOrderTraversalTuple():
    moves1 = [BlackMove(10, 10),
              WhiteMove(0, 0),
              BlackMove(10, 11)]
    moves2 = [BlackMove(10, 10),
              WhiteMove(1, 1),
              BlackMove(10, 11)]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(10, 10),
                WhiteMove(0, 0), BlackMove(10, 11),
                WhiteMove(1, 1), BlackMove(10, 11),)

    assert actual == expected


def test_Incorporate_ValidMoves_ReturnsCorrectPreOrderTraversalTuple2():
    moves1 = [BlackMove(10, 10),
              WhiteMove(0, 0),
              BlackMove(10, 11)]
    moves2 = [BlackMove(11, 10),
              WhiteMove(1, 1),
              BlackMove(10, 11)]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)
    incorporator.print_tree()
    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11),
                BlackMove(11, 10), WhiteMove(1, 1), BlackMove(10, 11),)

    assert actual == expected
