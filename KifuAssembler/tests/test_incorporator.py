from KifuAssembler.src.incorporator import Incorporator, KifuParser
from KifuAssembler.src.data_types import Root, WhiteMove, BlackMove


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


def test_Incorporate_ReturnsCorrectPreOrderTraversalTuple():
    incorporator = Incorporator()
    incorporator.incorporate([])

    actual = incorporator.to_tuple()
    expected = (Root(),)

    assert actual == expected


def test_ToSgf_ReturnsCorrectSgf():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), ]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 10), ]

    incorporator = Incorporator(moves1, "_sample_url_", "BWin")
    incorporator.incorporate(moves2, "_sample_url_", "WWin")

    actual = incorporator.to_sgf()
    expected = (
        '''\
(;B[jj]C[Visit Count := 2
]C[WinRate     := 50.00%
](;W[ik]C[WinRate     := 0.00%
];W[kk]C[Game urls   := _sample_url_
]C[WinRate     := 0.00%
])(;W[ii]C[WinRate     := 100.00%
];W[jk]C[Game urls   := _sample_url_
]C[WinRate     := 100.00%
]))\
'''
    )

    assert actual == expected


def test_ToSgf_ReturnsCorrectSgf_2():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(9, 10), BlackMove(9, 11)]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(10, 9), BlackMove(11, 9)]
    moves3 = [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 10), ]

    incorporator = Incorporator(moves1, "_sample_url_", "WWin")
    incorporator.incorporate(moves2, "_sample_url_", "WWin")
    incorporator.incorporate(moves3, "_sample_url_", "BWin")

    actual = incorporator.to_sgf()
    expected = ('''\
(;B[jj]C[Visit Count := 3
]C[WinRate     := 33.33%
](;W[ik]C[Visit Count := 2
]C[WinRate     := 100.00%
];W[kk]C[Visit Count := 2
]C[WinRate     := 100.00%
](;B[jk]C[WinRate     := 0.00%
];B[jl]C[Game urls   := _sample_url_
]C[WinRate     := 0.00%
])(;B[kj]C[WinRate     := 0.00%
];B[lj]C[Game urls   := _sample_url_
]C[WinRate     := 0.00%
]))(;W[ii]C[WinRate     := 0.00%
];W[jk]C[Game urls   := _sample_url_
]C[WinRate     := 0.00%
]))\
'''
                )

    assert actual == expected


def test_ToSgf_ReturnsCorrectSgf_3():
    moves1 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(9, 10), BlackMove(9, 11)]
    moves2 = [BlackMove(9, 9), WhiteMove(8, 10), WhiteMove(10, 10), BlackMove(10, 9), BlackMove(11, 9)]
    moves3 = [BlackMove(9, 9), ]

    incorporator = Incorporator(moves1)
    incorporator.incorporate(moves2)
    incorporator.incorporate(moves3)

    actual = incorporator.to_sgf()
    expected = ('''\
(;B[jj]C[Game urls   := _sample_url_
]C[Visit Count := 3
]C[WinRate     := 50.00%
];W[ik]C[Visit Count := 2
]C[WinRate     := 50.00%
];W[kk]C[Visit Count := 2
]C[WinRate     := 50.00%
](;B[jk]C[WinRate     := 50.00%
];B[jl]C[Game urls   := _sample_url_
]C[WinRate     := 50.00%
])(;B[kj]C[WinRate     := 50.00%
];B[lj]C[Game urls   := _sample_url_
]C[WinRate     := 50.00%
]))\
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
