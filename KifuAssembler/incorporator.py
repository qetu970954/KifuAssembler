from itertools import product

from anytree import AnyNode, RenderTree, PreOrderIter

from KifuAssembler.data_types import Root, WhiteMove, BlackMove


class KifuParser:
    """
    Kifu parser to convert a smart game format (from Little Golem) into a sequence of moves.
    """
    table = {}

    for i, j in product("abcdefghijklmnopqrs", range(1, 20)):
        table[f"{i}{j}"] = ("abcdefghijklmnopqrs".index(i), j - 1)

    for i, j, i2, j2 in product("abcdefghijklmnopqrs", range(1, 20), "abcdefghijklmnopqrs", range(1, 20)):
        table[f"{i}{j}{i2}{j2}"] = \
            ("abcdefghijklmnopqrs".index(i), j - 1, "abcdefghijklmnopqrs".index(i2), j2 - 1)

    @staticmethod
    def parse(content: str):
        # Split content by ';' and discard the element if it is empty.
        moves = [e for e in content[1:-1].split(';') if e]
        moves.pop(0)

        result = []

        for move in moves:
            role = move[0]
            if role == 'B':
                if len(KifuParser.table[move[2:-1]]) == 2:
                    i, j = KifuParser.table[move[2:-1]]
                    result.append(BlackMove(i, j))
                elif len(KifuParser.table[move[2:-1]]) == 4:
                    i1, j1, i2, j2 = KifuParser.table[move[2:-1]]
                    result.append(BlackMove(i1, j1))
                    result.append(BlackMove(i2, j2))

            elif role == 'W':
                if len(KifuParser.table[move[2:-1]]) == 2:
                    i, j = KifuParser.table[move[2:-1]]
                    result.append(WhiteMove(i, j))
                elif len(KifuParser.table[move[2:-1]]) == 4:
                    i1, j1, i2, j2 = KifuParser.table[move[2:-1]]
                    result.append(WhiteMove(i1, j1))
                    result.append(WhiteMove(i2, j2))

        return result


class Incorporator:
    r"""
    An incorporator that can merge various game moves into a tree-like structure.

    This class is used by assemble.py for assembling different kifus.

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

    def __init__(self, moves=None, url="_sample_url_"):
        self.root = AnyNode(data=Root(), visit_cnt=1, urls=[], is_terminate_node=False)
        if moves:
            self.incorporate(moves, url)

    def incorporate(self, moves: list, url="_sample_url_"):
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
                    is_terminate_node=False
                )

            if len(moves) == 0:
                current_node.urls.append(url)
                current_node.is_terminate_node = True

    def to_tuple(self):
        """Returns a pre-order tree traversal node sequence"""
        return tuple(node.data for node in PreOrderIter(self.root))

    def to_sgf(self):
        """Returns the tree in sgf format."""

        def depth_first_traversal(current_node, result):
            result += str(current_node.data)

            if current_node.urls and current_node.is_terminate_node:
                result += f"C[Game urls   := "
                result += ", ".join(current_node.urls)
                result += "\n]"

            if current_node.visit_cnt >= 2:
                result += f"C[Visit Count := {current_node.visit_cnt}\n]"

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
