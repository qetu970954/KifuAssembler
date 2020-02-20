from collections import namedtuple
from itertools import product

from anytree import AnyNode, RenderTree, PreOrderIter

from KifuAssembler.src.data_types import Root, WhiteMove, BlackMove, gogui_style_str


class KifuParser:
    """
    Kifu parser to convert a smart game format (from Little Golem) into a sequence of moves.
    """
    table = {}

    for i, j in product("abcdefghijklmnopqrs", range(1, 20)):
        table[f"{i}{j}"] = ("abcdefghijklmnopqrs".index(i), j - 1)

    for i, j in product("abcdefghijklmnopqrs", "abcdefghijklmnopqrs"):
        table[f"{i}{j}"] = ("abcdefghijklmnopqrs".index(i), "abcdefghijklmnopqrs".index(j))

    for i, j, i2, j2 in product("abcdefghijklmnopqrs", range(1, 20), "abcdefghijklmnopqrs", range(1, 20)):
        table[f"{i}{j}{i2}{j2}"] = \
            ("abcdefghijklmnopqrs".index(i), j - 1, "abcdefghijklmnopqrs".index(i2), j2 - 1)

    @staticmethod
    def parse(content: str):
        # Split content by ';' and discard the element if it is empty.
        moves = [e for e in content[1:-1].split(';') if e]
        moves.pop(0)

        result = []

        # For each moves, take out the mapped action and transform to Objects
        for move in moves:
            role = move[0]
            action_key = move[2:move.index("]")]
            if role == 'B':
                if len(KifuParser.table[action_key]) == 2:
                    i, j = KifuParser.table[action_key]
                    result.append(BlackMove(i, j))
                elif len(KifuParser.table[action_key]) == 4:
                    i1, j1, i2, j2 = KifuParser.table[action_key]
                    result.append(BlackMove(i1, j1))
                    result.append(BlackMove(i2, j2))

            elif role == 'W':
                if len(KifuParser.table[action_key]) == 2:
                    i, j = KifuParser.table[action_key]
                    result.append(WhiteMove(i, j))
                elif len(KifuParser.table[action_key]) == 4:
                    i1, j1, i2, j2 = KifuParser.table[action_key]
                    result.append(WhiteMove(i1, j1))
                    result.append(WhiteMove(i2, j2))

        return result


def to_string(a_node: AnyNode):
    result = str(a_node.data)

    if a_node.urls and a_node.is_terminate_node:
        result += f"C[Game urls   := "
        result += ", ".join(a_node.urls)
        result += "\n]"

    if a_node.visit_cnt >= 2:
        result += f"C[Visit Count := {a_node.visit_cnt}\n]"

    if isinstance(a_node.data, BlackMove):
        win_rate = format(
            100 * ((a_node.bwin + a_node.draw / 2) / (
                a_node.bwin + a_node.wwin + a_node.draw)),
            '3.2f'
        )
        result += f"C[WinRate     := {win_rate}%\n]"
        result += f"C[BWin count  := {a_node.bwin}\n]"
        result += f"C[WWin count  := {a_node.wwin}\n]"
        result += f"C[Draw count  := {a_node.draw}\n]"

    elif isinstance(a_node.data, WhiteMove):
        win_rate = format(
            100 * ((a_node.wwin + a_node.draw / 2) / (
                a_node.bwin + a_node.wwin + a_node.draw)),
            '3.2f'
        )
        result += f"C[WinRate     := {win_rate}%\n]"
        result += f"C[BWin count  := {a_node.bwin}\n]"
        result += f"C[WWin count  := {a_node.wwin}\n]"
        result += f"C[Draw count  := {a_node.draw}\n]"


    return result


class Incorporator:
    r"""
    An incorporator that can merge various game moves into a tree-like structure.

    This class is used by json_to_tree.py for assembling different kifus.

    >>> moves = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11)]
    >>> incorporator = Incorporator(moves)
    >>> incorporator.print_tree()
    <BLANKLINE>
    └── B[kk]
        └── W[aa]
            └── B[kl]
    >>> moves2 = [BlackMove(10, 10), WhiteMove(1, 1), BlackMove(10, 11)]
    >>> incorporator.incorporate(moves2)
    >>> incorporator.print_tree()
    <BLANKLINE>
    └── B[kk]
        ├── W[aa]
        │   └── B[kl]
        └── W[bb]
            └── B[kl]
    """

    def __init__(self, moves=None, url="_sample_url_", game_results="Draw"):
        self.root = AnyNode(data=Root(),
            visit_cnt=1,
            urls=[],
            is_terminate_node=False)

        if moves:
            self.incorporate(moves, url, game_results)

    def incorporate(self, moves: list, url="_sample_url_", game_results="Draw"):
        # Start from root node
        current_node = self.root

        while moves:
            current_mv = moves.pop(0)

            # Find the child from current_node which's content is identical to current_mv
            results = [c for c in current_node.children if c.data == current_mv]

            if results:
                # If such child exists, replace `current_node` to that child
                # This makes us walk to the deeper tree node to search for the first never-seen moves
                current_node = results[0]
                current_node.visit_cnt += 1

            else:
                # Otherwise, attach a new node to the tree
                current_node = AnyNode(
                    data=current_mv,
                    parent=current_node,
                    visit_cnt=1,
                    urls=[],
                    bwin=0,
                    wwin=0,
                    draw=0,
                    is_terminate_node=False
                )

            if len(moves) == 0:
                current_node.urls.append(url)
                current_node.is_terminate_node = True

            if game_results == "BWin":
                current_node.bwin += 1
            elif game_results == "WWin":
                current_node.wwin += 1
            elif game_results == "Draw":
                current_node.draw += 1

    def to_tuple(self):
        """Returns a pre-order tree traversal node sequence"""
        return tuple(node.data for node in PreOrderIter(self.root))

    def to_sgf(self):
        """Returns the tree in sgf format."""

        def depth_first_traversal(current_node, result):
            result += to_string(current_node)

            for child in current_node.children:
                if len(current_node.children) >= 2:
                    result += "(;"
                else:
                    result += ";"

                result = depth_first_traversal(child, result)

                if len(current_node.children) >= 2:
                    result += ")"

            return result

        return "(" + depth_first_traversal(self.root, "") + ")"

    def print_tree(self):
        for pre, _, node in RenderTree(self.root):
            print(f"{pre}{node.data}")


def to_GoGui_sgf(a_str):
    moves = [gogui_style_str(mv) for mv in KifuParser.parse(a_str)][1:]
    return "(;FF[4]CA[UTF-8]AP[GoGui:1.5.1];" + ";".join(moves) + ")"
