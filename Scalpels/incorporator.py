from anytree import AnyNode, RenderTree, PreOrderIter

from Scalpels.util import Root, WhiteMove, BlackMove


class Incorporator:
    """
    An incorporator that can merge various game moves into a tree-like structure.

    >>> from Scalpels.util import BlackMove, WhiteMove, Root
    >>> moves = [BlackMove(10, 10), WhiteMove(0, 0), BlackMove(10, 11)]
    >>> incorporator = Incorporator(moves)
    >>> incorporator.print_tree()
    <BLANKLINE>
    └── B[KK]
        └── W[AA]
            └── B[KL]


    >>> moves2 = [BlackMove(10, 10), WhiteMove(1, 1), BlackMove(10, 11)]
    >>> incorporator.incorporate(moves2)
    >>> incorporator.print_tree()
    <BLANKLINE>
    └── B[KK]
        ├── W[AA]
        │   └── B[KL]
        └── W[BB]
            └── B[KL]

    """

    def __init__(self, moves=None, url="_sample_url_"):
        self.root = AnyNode(data=Root(), visit_cnt=1, urls=[], is_terminate_node=False)
        if moves:
            self.incorporate(moves, url)

    def incorporate(self, moves: list, url="_sample_url_"):
        """
        This algorithm incorporate moves into the tree.
        """

        # Define the root node
        current_node = self.root

        while moves:
            current_mv = moves.pop(0)

            # Get the specific child from current_node which's content is identical to current_mv
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
        return tuple(node.data for node in PreOrderIter(self.root))

    def to_sgf(self):
        """
        Convert the internal tree into a sgf string.

        :return: the sgf string
        """

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

        return depth_first_traversal(self.root, "")

    def print_tree(self):
        for pre, _, node in RenderTree(self.root):
            print(f"{pre}{node.data}")
