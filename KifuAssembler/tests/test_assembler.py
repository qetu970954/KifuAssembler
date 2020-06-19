from KifuAssembler.src.assembler import Assembler, dump_to, to_tuple
from KifuAssembler.src.utils import KifuParser, Root, WhiteMove, BlackMove
import io


def test_Ctor_ReturnsCorrectPreOrderTraversalTuple():
    moves = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]

    assembler = Assembler(moves)

    actual = to_tuple(assembler)
    expected = (Root(),
                BlackMove(0, 0),
                WhiteMove(0, 1),
                BlackMove(0, 2))

    assert actual == expected
    assert type(actual) == tuple


def test_Assemble_ReturnsCorrectPreOrderTraversalTuple_0():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(0, 0), WhiteMove(1, 1), BlackMove(0, 2), ]

    assembler = Assembler(moves1)
    assembler.assemble(moves2)

    actual = to_tuple(assembler)
    expected = (Root(),
                BlackMove(0, 0),
                WhiteMove(0, 1), BlackMove(0, 2),
                WhiteMove(1, 1), BlackMove(0, 2),)

    assert actual == expected


def test_Assemble_ReturnsCorrectPreOrderTraversalTuple_1():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(1, 0), WhiteMove(1, 1), BlackMove(0, 2), ]

    assembler = Assembler(moves1)
    assembler.assemble(moves2)

    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2),
                BlackMove(1, 0), WhiteMove(1, 1), BlackMove(0, 2),)

    assert actual == expected


def test_Assemble_ReturnsCorrectPreOrderTraversalTuple_2():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(0, 0), WhiteMove(0, 2), BlackMove(0, 1), ]
    moves3 = [BlackMove(0, 0), WhiteMove(0, 2), BlackMove(0, 3), WhiteMove(0, 4), ]

    assembler = Assembler(moves1)
    assembler.assemble(moves2)
    assembler.assemble(moves3)

    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2),
                WhiteMove(0, 2), BlackMove(0, 1),
                BlackMove(0, 3), WhiteMove(0, 4),)

    assert actual == expected


def test_Assemble_ReturnsCorrectPreOrderTraversalTuple_3():
    moves1 = [BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2), ]
    moves2 = [BlackMove(0, 0), WhiteMove(0, 2), BlackMove(0, 1), ]
    moves3 = [BlackMove(0, 0), WhiteMove(0, 2), BlackMove(0, 3), WhiteMove(0, 4), ]

    assembler = Assembler(moves1)
    assembler.assemble(moves2)
    assembler.assemble(moves3)

    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(0, 0), WhiteMove(0, 1), BlackMove(0, 2),
                WhiteMove(0, 2), BlackMove(0, 1),
                BlackMove(0, 3), WhiteMove(0, 4),)

    assert actual == expected


def test_Assemble_ReturnsCorrectPreOrderTraversalTuple_4():
    assembler = Assembler()
    assembler.assemble([])

    actual = to_tuple(assembler)

    expected = (Root(),)

    assert actual == expected


def test_DumpTo_ReturnsCorrectSgf_0():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), ]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 10), ]

    assembler = Assembler(moves1, "_sample_url_", game_results="BWin", merge_symmetric_moves=True)
    assembler.assemble(moves2, "_sample_url_", "WWin")

    # We use this object to emulate a `file`, so no additional file will be created when unit-testing
    file = io.StringIO()
    dump_to(assembler, file, editor_style=False)
    actual = file.getvalue()
    print(actual)
    expected = '''\
(;GM[511]C[Visit Count = 2
BWin count  = 1
WWin count  = 1
Draw count  = 0
];B[JJ]C[Visit Count = 2
BWin count  = 1
WWin count  = 1
Draw count  = 0
WinRate     = 50.00%
];W[II]C[Visit Count = 2
BWin count  = 1
WWin count  = 1
Draw count  = 0
WinRate     = 50.00%
](;W[IK]C[BWin count  = 1
WWin count  = 0
Draw count  = 0
WinRate     = 0.00%
Game urls   = _sample_url_
])(;W[JK]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 100.00%
Game urls   = _sample_url_
]))C[Visit Count = 2
BWin count  = 1
WWin count  = 1
Draw count  = 0
]\
'''

    assert actual == expected


def test_dumpTo_editorStyleEnabled_ReturnsCorrectSgf_0():
    moves1 = [BlackMove(9, 9), WhiteMove(0, 0), WhiteMove(0, 1)]
    moves2 = [BlackMove(9, 8), WhiteMove(0, 0), WhiteMove(0, 1)]
    assembler = Assembler(moves1, game_results="WWin", merge_symmetric_moves=True)
    assembler.assemble(moves2, game_results="BWin")

    file = io.StringIO()
    dump_to(assembler, file, editor_style=True)
    actual = file.getvalue()
    print(actual)
    expect = '''\
(;GM[511](;B[JJ]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 0.00%
];W[AA]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 100.00%
];W[AB]C[BWin count  = 0
WWin count  = 1
Draw count  = 0
WinRate     = 100.00%
Game urls   = _sample_url_
])(;B[IJ]C[BWin count  = 1
WWin count  = 0
Draw count  = 0
WinRate     = 100.00%
];W[AA]C[BWin count  = 1
WWin count  = 0
Draw count  = 0
WinRate     = 0.00%
];W[BA]C[BWin count  = 1
WWin count  = 0
Draw count  = 0
WinRate     = 0.00%
Game urls   = _sample_url_
]))C[Visit Count = 2
BWin count  = 1
WWin count  = 1
Draw count  = 0
]\
'''
    assert actual == expect


def test_dumpTo_editorStyleEnabled_ReturnsCorrectSgf_1():
    moves1 = [BlackMove(9, 9), WhiteMove(0, 0), WhiteMove(0, 1)]
    moves2 = [BlackMove(9, 10), WhiteMove(0, 0), WhiteMove(0, 1)]

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)
    file = io.StringIO()
    dump_to(assembler, file, editor_style=True)
    actual = file.getvalue()
    print(actual)
    expect = '''\
(;GM[511](;B[JJ]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
];W[AA]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
];W[AB]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
Game urls   = _sample_url_
])(;B[IJ]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
];W[RA]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
];W[SA]C[BWin count  = 0
WWin count  = 0
Draw count  = 1
WinRate     = 50.00%
Game urls   = _sample_url_
]))C[Visit Count = 2
BWin count  = 0
WWin count  = 0
Draw count  = 2
]\
'''
    assert actual == expect


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


def test_Assemble_mergeSymmetricMoves_ReturnsCorrectPreOrderTraversalTuple_0():
    moves1 = [BlackMove(0, 0), WhiteMove(2, 1), BlackMove(0, 2)]
    moves2 = [BlackMove(0, 18), WhiteMove(1, 16), BlackMove(2, 18), ]  # Rotate 90%
    moves3 = [BlackMove(18, 18), WhiteMove(16, 17), BlackMove(18, 16), ]  # Rotate 180%
    moves4 = [BlackMove(18, 0), WhiteMove(17, 2), BlackMove(16, 0), ]  # Rotate 270%
    moves5 = [BlackMove(0, 18), WhiteMove(2, 17), BlackMove(0, 16), ]  # Horizontal reflection

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)
    assembler.assemble(moves3)
    assembler.assemble(moves4)
    assembler.assemble(moves5)

    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(0, 0),
                WhiteMove(1, 2),
                BlackMove(2, 0),)

    assert actual == expected


def test_Assemble_C6FlagEnabled_ReturnsCorrectTuple_case0():
    moves1 = [BlackMove(9, 9), WhiteMove(10, 10), WhiteMove(10, 8), ]
    moves2 = [BlackMove(9, 9), WhiteMove(10, 8), WhiteMove(10, 10), ]

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)

    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(8, 10),)

    assert actual == expected


def test_Assemble_C6FlagEnabled_ReturnsCorrectTuple_case1():
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

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)
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

    actual = to_tuple(assembler)

    assert actual == expected


def test_Assemble_C6FlagEnabled_ReturnsCorrectTuple_case2():
    moves1 = [BlackMove(9, 9),
              WhiteMove(9, 8), WhiteMove(8, 8)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(10, 9), WhiteMove(10, 10)]

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)
    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(8, 8),
                WhiteMove(8, 9),)

    assert actual == expected


def test_Assemble_C6FlagEnabled_ReturnsCorrectTuple_case3():
    moves1 = [BlackMove(9, 9),
              WhiteMove(8, 8), WhiteMove(10, 9)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(9, 8), WhiteMove(8, 10)]

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)
    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(8, 8),
                WhiteMove(9, 10),)

    assert actual == expected


def test_Assemble_C6FlagEnabled_ReturnsCorrectTuple_case4():
    moves1 = [BlackMove(9, 9),
              WhiteMove(8, 8), WhiteMove(9, 7)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(9, 7), WhiteMove(8, 8)]

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)
    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(7, 9),
                WhiteMove(8, 8),)

    assert actual == expected


def test_Assemble_C6FlagEnabled_ReturnsCorrectTuple_case5():
    moves1 = [BlackMove(9, 9),
              WhiteMove(7, 9), WhiteMove(8, 8), BlackMove(6, 6), BlackMove(7, 7)]

    moves2 = [BlackMove(9, 9),
              WhiteMove(8, 8), WhiteMove(7, 9), BlackMove(7, 7), BlackMove(6, 6)]

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)
    actual = to_tuple(assembler)

    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(7, 9),
                WhiteMove(8, 8),
                BlackMove(6, 6),
                BlackMove(7, 7))

    assert actual == expected


def test_Assemble_C6FlagEnabled_ReturnsCorrectTuple_case6():
    moves1 = [BlackMove(9, 9), WhiteMove(7, 9), WhiteMove(8, 8), BlackMove(8, 7)]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(7, 9), BlackMove(8, 7)]
    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)

    actual = to_tuple(assembler)
    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(7, 9),
                WhiteMove(8, 8),
                BlackMove(8, 7),)
    assert actual == expected


def test_Assemble_C6FlagEnabled_ReturnsCorrectTuple_case7():
    moves1 = [BlackMove(9, 9), WhiteMove(9, 8), WhiteMove(8, 9), BlackMove(8, 8), BlackMove(7, 10)]
    moves2 = [BlackMove(9, 9), WhiteMove(9, 8), WhiteMove(8, 9), BlackMove(8, 8), BlackMove(10, 7)]
    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)

    actual = to_tuple(assembler)
    expected = (Root(),
                BlackMove(9, 9),
                WhiteMove(8, 9),
                WhiteMove(9, 8),
                BlackMove(8, 8),
                BlackMove(7, 10),)
    assert actual == expected


def test_topMoves_chooseTop2_ReturnListsOfMoves():
    moves1 = [BlackMove(9, 9), WhiteMove(0, 0), WhiteMove(0, 2), BlackMove(0, 3), BlackMove(0, 4)]
    moves2 = [BlackMove(9, 9), WhiteMove(0, 0), WhiteMove(0, 2), BlackMove(0, 3), BlackMove(0, 4)]
    moves3 = [BlackMove(9, 9), WhiteMove(0, 0), WhiteMove(0, 1)]
    moves4 = [BlackMove(9, 9), WhiteMove(0, 0), WhiteMove(0, 1)]
    moves5 = [BlackMove(9, 9), WhiteMove(0, 2), WhiteMove(8, 8)]

    assembler = Assembler(moves1, merge_symmetric_moves=True)
    assembler.assemble(moves2)
    assembler.assemble(moves3)
    assembler.assemble(moves4)
    assembler.assemble(moves5)

    actual = assembler.top_n_moves(2)
    expected = [';;B[JJ];W[AA];W[AC]', ';;B[JJ];W[AA];W[AB]']

    assert actual == expected