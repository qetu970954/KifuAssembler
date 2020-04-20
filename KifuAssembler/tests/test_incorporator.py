from KifuAssembler.src.incorporator import Incorporator, KifuParser, dump_to
from KifuAssembler.src.utils import Root, WhiteMove, BlackMove
import io


def test_Ctor_ReturnsCorrectPreOrderTraversalTuple():
    moves = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]

    incorporator = Incorporator(moves)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0),
                WhiteMove(0, 1),
                BlackMove(0, 2))

    assert actual == expected
    assert type(actual) == tuple


def test_Incorporate_ReturnsCorrectPreOrderTraversalTuple_0():
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


def test_Incorporate_ReturnsCorrectPreOrderTraversalTuple_1():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(1, 0), WhiteMove(1, 1), BlackMove(0, 2), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2),
                BlackMove(1, 0), WhiteMove(1, 1), BlackMove(0, 2),)

    assert actual == expected


def test_Incorporate_ReturnsCorrectPreOrderTraversalTuple_2():
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


def test_Incorporate_ReturnsCorrectPreOrderTraversalTuple_3():
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


def test_Incorporate_ReturnsCorrectPreOrderTraversalTuple_4():
    incorporator = Incorporator()
    incorporator.incorporate([])

    actual = incorporator.to_tuple()
    expected = (Root(),)

    assert actual == expected


def test_DumpTo_ReturnsCorrectSgf_0():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), ]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 10), ]

    incorporator = Incorporator(moves1, "_sample_url_", "BWin")
    incorporator.incorporate(moves2, "_sample_url_", "WWin")

    # We use this object to emulate a `file`, so no additional file will be created when unit-testing
    file = io.StringIO()
    dump_to(incorporator, file)
    actual = file.getvalue()
    expected = ('''\
(;B[jj]C[Visit Count = 2
BWin count  = 1
WWin count  = 1
Draw count  = 0
WinRate     = 50.00%
](;W[ik]C[BWin count  = 1
WWin count  = 0
Draw count  = 0
WinRate     = 0.00%
];W[kk]C[BWin count  = 1
WWin count  = 0
Draw count  = 0
WinRate     = 0.00%
Game urls   = _sample_url_])(;W[ii]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 100.00%
];W[jk]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 100.00%
Game urls   = _sample_url_]))\
'''
                )

    assert actual == expected


def test_DumpTo_ReturnsCorrectSgf_1():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(9, 10), BlackMove(9, 11)]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(10, 9), BlackMove(11, 9)]
    moves3 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 10), ]

    incorporator = Incorporator(moves1, "_sample_url_", "WWin")
    incorporator.incorporate(moves2, "_sample_url_", "WWin")
    incorporator.incorporate(moves3, "_sample_url_", "BWin")

    file = io.StringIO()
    dump_to(incorporator, file)
    actual = file.getvalue()
    expected = ('''\
(;B[jj]C[Visit Count = 3
BWin count  = 1
WWin count  = 2
Draw count  = 0
WinRate     = 33.33%
](;W[ik]C[Visit Count = 2
BWin count  = 0
WWin count  = 2
Draw count  = 0
WinRate     = 100.00%
];W[kk]C[Visit Count = 2
BWin count  = 0
WWin count  = 2
Draw count  = 0
WinRate     = 100.00%
](;B[jk]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 0.00%
];B[jl]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 0.00%
Game urls   = _sample_url_])(;B[kj]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 0.00%
];B[lj]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 0.00%
Game urls   = _sample_url_]))(;W[ii]C[BWin count  = 1
WWin count  = 0
Draw count  = 0
WinRate     = 0.00%
];W[jk]C[BWin count  = 1
WWin count  = 0
Draw count  = 0
WinRate     = 0.00%
Game urls   = _sample_url_]))\
'''
                )
    assert actual == expected


def test_DumpTo_ReturnsCorrectSgf_2():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(9, 10), BlackMove(9, 11)]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(10, 9), BlackMove(11, 9)]
    moves3 = [BlackMove(9, 9), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)
    incorporator.incorporate(moves3)

    file = io.StringIO()
    dump_to(incorporator, file)
    actual = file.getvalue()
    print(actual)
    expected = ('''\
(;B[jj]C[Visit Count = 3
BWin count  = 0
WWin count  = 0
Draw count  = 3
WinRate     = 50.00%
Game urls   = _sample_url_];W[ik]C[Visit Count = 2
BWin count  = 0
WWin count  = 0
Draw count  = 2
WinRate     = 50.00%
];W[kk]C[Visit Count = 2
BWin count  = 0
WWin count  = 0
Draw count  = 2
WinRate     = 50.00%
](;B[jk]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
];B[jl]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
Game urls   = _sample_url_])(;B[kj]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
];B[lj]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
Game urls   = _sample_url_]))\
''')

    assert actual == expected


def test_parse_ReturnsCorrectMoveList():
    """
    The kifu is in smart game format
    :return:
    """
    sample_kifu = "(;FF[4]EV[connect6.ch.26.1.1]PB[Phoenix]PW[Lomaben]SO[http://www.littlegolem.com];B[j10];W[j9l11];" \
                  "B[k9l8];W[k10i11])"

    actual = KifuParser.parse(sample_kifu)

    expected = [BlackMove(9, 9),
                WhiteMove(9, 8),
                WhiteMove(11, 10),
                BlackMove(10, 8),
                BlackMove(11, 7),
                WhiteMove(10, 9),
                WhiteMove(8, 10), ]

    assert actual == expected


def test_SymmetricalIncorporate_ReturnsCorrectPreOrderTraversalTuple_0():
    moves1 = [BlackMove(0, 0), WhiteMove(2, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(0, 0), WhiteMove(1, 2), BlackMove(3, 3), ]

    incorporator = Incorporator(moves1, merge_symmetric_moves=True)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0),
                WhiteMove(1, 2),
                BlackMove(2, 0),
                BlackMove(3, 3),)

    assert actual == expected


def test_SymmetricalIncorporate_ReturnsCorrectPreOrderTraversalTuple_1():
    moves1 = [BlackMove(0, 0), WhiteMove(2, 1), BlackMove(0, 2)]
    moves2 = [BlackMove(0, 18), WhiteMove(1, 16), BlackMove(2, 18), ]  # Rotate 90%
    moves3 = [BlackMove(18, 18), WhiteMove(16, 17), BlackMove(18, 16), ]  # Rotate 180%
    moves4 = [BlackMove(18, 0), WhiteMove(17, 2), BlackMove(16, 0), ]  # Rotate 270%
    moves5 = [BlackMove(0, 18), WhiteMove(2, 17), BlackMove(0, 16), ]  # Horizontal reflection

    incorporator = Incorporator(moves1, merge_symmetric_moves=True)
    incorporator.incorporate(moves2)
    incorporator.incorporate(moves3)
    incorporator.incorporate(moves4)
    incorporator.incorporate(moves5)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(0, 0),
                WhiteMove(1, 2),
                BlackMove(2, 0),)

    assert actual == expected


def test_IncorporateWithC6FlagEnabled_ReturnsCorrectTuple_0():
    moves1 = [BlackMove(9, 9), WhiteMove(10, 10), WhiteMove(10, 8), ]
    moves2 = [BlackMove(9, 9), WhiteMove(10, 8), WhiteMove(10, 10), ]

    incorporator = Incorporator(moves1, merge_symmetric_moves=True, use_c6_merge_rules=True)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(8, 10),)

    assert actual == expected


def test_IncorporateWithC6FlagEnabled_ReturnsCorrectTuple_1():
    moves1 = [BlackMove(9, 9),
              WhiteMove(11, 7), WhiteMove(12, 6),
              BlackMove(11, 11), BlackMove(12, 12),
              WhiteMove(11, 3), WhiteMove(12, 3),
              BlackMove(9, 3), BlackMove(8, 3)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(7, 11), WhiteMove(6, 12),
              BlackMove(11, 11), BlackMove(12, 12),
              WhiteMove(11, 3), WhiteMove(12, 3),
              BlackMove(9, 3), BlackMove(8, 3)]

    incorporator = Incorporator(moves1, merge_symmetric_moves=True, use_c6_merge_rules=True)
    incorporator.incorporate(moves2)
    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(6, 6),
                WhiteMove(7, 7),
                BlackMove(6, 12),
                BlackMove(7, 11),

                WhiteMove(6, 3),
                WhiteMove(7, 3),
                BlackMove(9, 3),
                BlackMove(10, 3),

                WhiteMove(15, 11),
                WhiteMove(15, 12),
                BlackMove(15, 8),
                BlackMove(15, 9))

    actual = incorporator.to_tuple()

    assert actual == expected


def test_IncorporateWithC6FlagEnabled_ReturnsCorrectTuple_2():
    moves1 = [BlackMove(9, 9),
              WhiteMove(9, 8), WhiteMove(8, 8)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(10, 9), WhiteMove(10, 10)]

    incorporator = Incorporator(moves1, merge_symmetric_moves=True, use_c6_merge_rules=True)
    incorporator.incorporate(moves2)
    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(8, 8),
                WhiteMove(8, 9),)

    assert actual == expected


def test_IncorporateWithC6FlagEnabled_ReturnsCorrectTuple_3():
    moves1 = [BlackMove(9, 9),
              WhiteMove(8, 8), WhiteMove(10, 9)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(9, 8), WhiteMove(8, 10)]

    incorporator = Incorporator(moves1, merge_symmetric_moves=True, use_c6_merge_rules=True)
    incorporator.incorporate(moves2)
    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(8, 8),
                WhiteMove(9, 10),)

    assert actual == expected


def test_IncorporateWithC6FlagEnabled_ReturnsCorrectTuple_4():
    moves1 = [BlackMove(9, 9),
              WhiteMove(8, 8), WhiteMove(9, 7)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(9, 7), WhiteMove(8, 8)]

    incorporator = Incorporator(moves1, merge_symmetric_moves=True, use_c6_merge_rules=True)
    incorporator.incorporate(moves2)
    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(7, 9),
                WhiteMove(8, 8),)

    assert actual == expected


def test_IncorporateWithC6FlagEnabled_ReturnsCorrectTuple_5():
    moves1 = [BlackMove(9, 9),
              WhiteMove(7, 9), WhiteMove(8, 8), BlackMove(6, 6), BlackMove(7, 7)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(8, 8), WhiteMove(7, 9), BlackMove(7, 7), BlackMove(6, 6)]

    incorporator = Incorporator(moves1, merge_symmetric_moves=True, use_c6_merge_rules=True)
    incorporator.incorporate(moves2)
    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(7, 9),
                WhiteMove(8, 8),
                BlackMove(6, 6),
                BlackMove(7, 7))

    assert actual == expected


def test_IncorporateWithC6FlagEnabled_ReturnsCorrectTuple_6():
    moves1 = [BlackMove(9, 9), WhiteMove(7, 9), WhiteMove(8, 8), BlackMove(8, 7)]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(7, 9), BlackMove(8, 7)]
    incorporator = Incorporator(moves1, merge_symmetric_moves=True, use_c6_merge_rules=True)
    incorporator.incorporate(moves2)

    actual = incorporator.to_tuple()
    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(7, 9),
                WhiteMove(8, 8),
                BlackMove(8, 7),)
    assert actual == expected


# def test_IncorporateWithC6FlagEnabled_ReturnsCorrectTuple_7():
#     # moves1 = [BlackMove(9, 9), WhiteMove(7, 8), WhiteMove(9, 8),
#     # moves2 = [BlackMove(9, 9), WhiteMove(8, 9), WhiteMove(8, 7), BlackMove(8, 10), BlackMove(9, 11)]
#     # incorporator.incorporate(moves2)
#
#     s = "(;FF[4]EV[connect6.in.DEFAULT.238]PB[gzero_bot]PW[Michail]SO[http://www.littlegolem.com];B[j10];W[j11l11];B[i11h10];W[h12i10];B[g8g9];W[f8g7];B[f12g11];W[i9e13];B[e11d10];W[g13f10];B[d11f11];W[h11c11];B[f9e10];W[c12h7];B[d9c8];W[h13b7];B[d13c9])"
#     moves = KifuParser.parse(s)
#     incorporator = Incorporator(moves, merge_symmetric_moves=True, use_c6_merge_rules=True)
#
#     actual = incorporator.to_tuple()
#     expected = (Root(),
#                 BlackMove(9, 9),
#                 WhiteMove(7, 8),
#                 WhiteMove(9, 8),)
#     assert actual == expected
