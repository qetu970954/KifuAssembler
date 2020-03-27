import pytest
import copy
from KifuAssembler.src.utils import rotate_270, rotate_180, rotate_90, BlackMove, WhiteMove, \
    build_symmetric_lookup_table


@pytest.mark.parametrize("test_moves, expected", [
    (BlackMove(2, 0), BlackMove(0, 16)),
    (BlackMove(16, 0), BlackMove(0, 2)),
    (BlackMove(16, 18), BlackMove(18, 2)),
    (WhiteMove(2, 18), WhiteMove(18, 16))
])
def test_Rotate90_IsCorrect(test_moves, expected):
    actual = rotate_90(test_moves)
    assert actual == expected


@pytest.mark.parametrize("test_moves, expected", [
    (BlackMove(2, 0), BlackMove(16, 18)),
    (BlackMove(16, 0), BlackMove(2, 18)),
    (BlackMove(16, 18), BlackMove(2, 0)),
    (WhiteMove(2, 18), WhiteMove(16, 0))
])
def test_Rotate180_IsCorrect(test_moves, expected):
    actual = rotate_180(test_moves)
    assert actual == expected


@pytest.mark.parametrize("test_moves, expected", [
    (BlackMove(2, 0), BlackMove(18, 2)),
    (BlackMove(16, 0), BlackMove(18, 16)),
    (BlackMove(16, 18), BlackMove(0, 16)),
    (WhiteMove(2, 18), WhiteMove(0, 2))
])
def test_Rotate270_IsCorrect(test_moves, expected):
    actual = rotate_270(test_moves)
    assert actual == expected

def test_build_table():
    build_symmetric_lookup_table()
