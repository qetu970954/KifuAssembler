from anytree import AnyNode, RenderTree, PreOrderIter

from Move import BlackMove, WhiteMove


class Incorporator:
    """
    An incorporator that can merge various game moves into a tree.
    """

    def __init__(self, moves: tuple):
        self.root = AnyNode(id="Root")

        parent_node = self.root
        for move in moves:
            parent_node = AnyNode(id=move, parent=parent_node)


    def to_tuple(self):
        return tuple(node.id for node in PreOrderIter(self.root))
