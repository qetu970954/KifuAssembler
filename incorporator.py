from collections import namedtuple

from anytree import AnyNode, RenderTree, PreOrderIter

from NodeTypes import Root

TraversalNode = namedtuple("TraversalNode", ["TreeNode", "CandidateChild"])


class Incorporator:
    """
    An incorporator that can merge various game moves into a tree-like structure.

    >>> from NodeTypes import BlackMove, WhiteMove, Root
    >>> moves = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11)]
    >>> incorporator = Incorporator(moves)
    >>> incorporator.print_tree()
    Root()
    └── BlackMove(i=10, j=10)
        └── WhiteMove(i=0, j=0)
            └── BlackMove(i=10, j=11)

    >>> moves2 = [BlackMove(10, 10), WhiteMove(1, 1), BlackMove(10, 11)]
    >>> incorporator.incorporate(moves2)
    >>> incorporator.print_tree()
    Root()
    └── BlackMove(i=10, j=10)
        ├── WhiteMove(i=0, j=0)
        │   └── BlackMove(i=10, j=11)
        └── WhiteMove(i=1, j=1)
            └── BlackMove(i=10, j=11)

    """

    def __init__(self, moves):
        self.root = AnyNode(data=Root())

        parent_node = self.root
        for move in moves:
            parent_node = AnyNode(data=move, parent=parent_node)

    def incorporate(self, moves: list):
        """
        Moves are literally a sequence of move on the board.
        e.g., Root(), BlackMove(), WhiteMove(), BlackMove()

        This algorithm incorporate moves into the tree.
        It searches for the first move that has never been seen on the tree,
        and attach the remaining moves to the tree.
        """
        current_node = self.root
        while moves:
            current_mv = moves.pop(0)

            # Get the specific child if it's content is identical to current_mv
            result = [child for child in current_node.children if child.data == current_mv]

            if result:
                # If the child exists, update `current_node` to that child
                # This simply let us walk to a deep tree level
                current_node = result[0]
                continue

            else:
                # Otherwise, attach the remaining moves into a new branch in the tree
                parent = AnyNode(data=current_mv, parent=current_node)
                for mv in moves:
                    parent = AnyNode(data=mv, parent=parent)
                break


    def to_tuple(self):
        return tuple(node.data for node in PreOrderIter(self.root))

    def print_tree(self):
        for pre, _, node in RenderTree(self.root):
            print(f"{pre}{node.data}")
