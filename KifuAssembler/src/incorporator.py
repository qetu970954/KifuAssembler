from itertools import product
from typing import TextIO

from anytree import AnyNode, PreOrderIter

from KifuAssembler.src.utils import Root, WhiteMove, BlackMove, gogui_style_str, build_symmetric_lookup_table, \
    all_possible_actions, GAME_CONFIG
import copy


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


def detailed_str(a_node: AnyNode):
    result = str(a_node.data)
    result += "C["
    if a_node.visit_cnt >= 2:
        result += f"Visit Count = {a_node.visit_cnt}\n"
    result += f"BWin count  = {a_node.bwin}\n"
    result += f"WWin count  = {a_node.wwin}\n"
    result += f"Draw count  = {a_node.draw}\n"
    if isinstance(a_node.data, BlackMove):
        win_rate = format(
            100 * ((a_node.bwin + a_node.draw / 2) / (
                    a_node.bwin + a_node.wwin + a_node.draw)),
            '3.2f'
        )
        result += f"WinRate     = {win_rate}%\n"

    elif isinstance(a_node.data, WhiteMove):
        win_rate = format(
            100 * ((a_node.wwin + a_node.draw / 2) / (
                    a_node.bwin + a_node.wwin + a_node.draw)),
            '3.2f'
        )
        result += f"WinRate     = {win_rate}%\n"

    if a_node.urls and a_node.is_terminate_node:
        result += f"Game urls   = "
        result += ", ".join(a_node.urls)
    result += "]"
    return result


def rearrange(moves):
    r"""
    Rearrange a sequence of moves, so that moves with smaller idx will always appear before larger one.

    This is useful to merge moves in connect6, where two same-color moves with different order are consider the same.

    # WhiteMove(9, 8) has bigger index than WhiteMove(8, 8), so they are swapped.
    >>> rearrange( [BlackMove(9, 9), WhiteMove(9, 8), WhiteMove(8, 8)] )
    [BlackMove(x=9, y=9), WhiteMove(x=8, y=8), WhiteMove(x=9, y=8)]
    >>> rearrange( [BlackMove(9, 9), WhiteMove(8, 8), WhiteMove(9, 8)] )
    [BlackMove(x=9, y=9), WhiteMove(x=8, y=8), WhiteMove(x=9, y=8)]
    >>> rearrange( [BlackMove(9, 9), WhiteMove(1, 1), WhiteMove(8, 8)] )
    [BlackMove(x=9, y=9), WhiteMove(x=1, y=1), WhiteMove(x=8, y=8)]
    """
    result = []
    for mv in moves:
        if len(result) >= 1 and type(result[-1]) == type(mv):
            if result[-1] > mv:
                result[-1], mv = mv, result[-1]
        result.append(mv)
    return result


class Incorporator:
    r"""
    An incorporator that can merge various game moves into a tree-like structure.

    This class is used by json_to_tree.py for assembling different kifus.
    """

    def __init__(self, moves=None, url="_sample_url_", *, game_results="Draw", merge_symmetric_moves=False,
                 use_c6_merge_rules=False):
        self.root = AnyNode(
            data=Root(),
            parent=None,
            visit_cnt=0,
            urls=[],
            bwin=0,
            wwin=0,
            draw=0,
            is_terminate_node=False
        )

        self.merge_symmetric_moves = merge_symmetric_moves
        self.use_c6_merge_rules = use_c6_merge_rules

        if moves:
            self.incorporate(moves, url, game_results)

    def incorporate(self, moves: list, url="_sample_url_", game_results="Draw"):
        if self.merge_symmetric_moves:
            self._symmetrical_incorporate(moves, url, game_results)
        else:
            self._incorporate(moves, url, game_results)

    def _incorporate(self, moves: list, url="_sample_url_", game_results="Draw"):
        # Start from root node
        current_node = self.root

        while True:
            current_node.visit_cnt += 1

            if len(moves) == 0:
                current_node.urls.append(url)
                current_node.is_terminate_node = True

            if game_results == "BWin":
                current_node.bwin += 1
            elif game_results == "WWin":
                current_node.wwin += 1
            elif game_results == "Draw":
                current_node.draw += 1

            if not moves:
                break

            current_mv = moves.pop(0)
            # Find the child from current_node which's content is identical to current_mv
            results = [c for c in current_node.children if c.data == current_mv]

            if results:
                # If such child exists, replace `current_node` to that child
                # This makes us walk to the deeper tree node to search for the first never-seen moves
                current_node = results[0]
            else:
                # Otherwise, attach a new node to the tree
                new_node = AnyNode(
                    data=current_mv,
                    parent=current_node,
                    visit_cnt=0,
                    urls=[],
                    bwin=0,
                    wwin=0,
                    draw=0,
                    is_terminate_node=False
                )
                current_node = new_node

    def _symmetrical_incorporate(self, moves: list, url="_sample_url_", game_results="Draw"):
        def find_game_turns_that_is_not_present_on_the_tree(mvs):
            current_node = self.root
            idx, turns = 0, 0

            while idx < len(mvs):
                children = [c for c in current_node.children if c.data == mvs[idx]]
                if children:
                    chosen_child = min(children)
                    idx += 1
                    if (idx - GAME_CONFIG.p) % GAME_CONFIG.q == 0:
                        turns += 1
                    current_node = chosen_child
                else:
                    break

            return turns

        if len(moves) == 0:
            return

        # Start checks the first moves which is NOT presented on the tree
        if self.use_c6_merge_rules:
            idx1 = find_game_turns_that_is_not_present_on_the_tree(rearrange(moves))
        else:
            idx1 = find_game_turns_that_is_not_present_on_the_tree(rearrange(moves))

        symmetric_moves_lists = []
        if self.use_c6_merge_rules:
            # Get all possible symmetrical moves, including rearranged
            for action in all_possible_actions():
                sym_mvs = moves[0:idx1] + [action(mv) for mv in moves[idx1:]]
                symmetric_moves_lists.append(rearrange(sym_mvs))

            # Find one of the symmetric moves that maximize the similarity of moves inside the tree.
            # The 'similarity' is calculated by finding the first index of move that does not show on the tree.
            # The higher the index is, the more similarity it gets.
            mvs = min(symmetric_moves_lists,
                key=lambda mvs: (-find_game_turns_that_is_not_present_on_the_tree(mvs), mvs))

            # Merge the result with moves rearranged
            self._incorporate(
                rearrange(mvs), url, game_results
            )

        else:
            table = build_symmetric_lookup_table()
            for action in table[(moves[idx1].i, moves[idx1].j)]:
                sym_mvs = moves[0:idx1] + [action(mv) for mv in moves[idx1:]]
                symmetric_moves_lists.append(sym_mvs)

            mvs = max(symmetric_moves_lists, key=lambda mvs: find_game_turns_that_is_not_present_on_the_tree(mvs))
            self._incorporate(
                mvs, url, game_results
            )

    def top_n_moves(self, amount):
        def dfs(current_node, depth, sgf: str):
            sgf += str(current_node.data)
            valid_children = [child for child in current_node.children if child.visit_cnt >= visit_cnt_threshold]
            valid_children = sorted(valid_children, key=lambda node: node.visit_cnt)

            original_length = len(result)

            for child in valid_children:
                dfs(child, depth + 1, sgf)

            if sgf and is_end_of_turn(depth):
                if original_length == len(result):
                    result.append((sgf, current_node.visit_cnt))
                elif original_length + 1 == len(result):
                    result.pop(-1)
                    result.append((sgf, current_node.visit_cnt))

        if amount == 0:
            return []

        for visit_cnt_threshold in range(self.root.visit_cnt, 0, -1):
            result = []
            dfs(self.root, 0, "")
            print(f"Current threshold is {visit_cnt_threshold : >5}, result has length {len(result): >5} ")
            if len(result) >= amount or visit_cnt_threshold == 0:
                return result


def to_tuple(an_Incorporator: Incorporator):
    """Returns a pre-order tree traversal node sequence"""
    return copy.deepcopy(tuple(node.data for node in PreOrderIter(an_Incorporator.root)))


def is_end_of_turn(d):
    if d == 0 or d == GAME_CONFIG.p:
        return True
    elif d > GAME_CONFIG.p and (d - GAME_CONFIG.p) % GAME_CONFIG.q == 0:
        return True
    else:
        return False


def dump_to(an_Incorporator: Incorporator, file: TextIO, *, editor_style):
    """Dump the content in an incorporator to a file (in sgf format)."""

    def simple_tree_traverse(current_node, file: TextIO):
        file.write(detailed_str(current_node))

        for child in current_node.children:
            if len(current_node.children) >= 2:
                file.write("(;")
            else:
                file.write(";")

            simple_tree_traverse(child, file)

            if len(current_node.children) >= 2:
                file.write(")")


    def editor_style_tree_traverse(current_node: AnyNode, depth: int, branch_flag: bool, sgf: str, file: TextIO):
        depth += 1
        if is_end_of_turn(depth):
            for child in current_node.children:
                if branch_flag: file.write("(")
                file.write(f"{sgf};{detailed_str(child)}")
                editor_style_tree_traverse(child, depth, len(child.children) > 1, "", file)
                if branch_flag: file.write(")")

        else:
            for child in current_node.children:
                child_branch_flag = branch_flag or len(child.children) > 1
                editor_style_tree_traverse(child, depth, child_branch_flag, sgf + ";" + detailed_str(child), file)

    file.write("(;GM[511]")
    if editor_style:
        editor_style_tree_traverse(an_Incorporator.root, 0, len(an_Incorporator.root.children) > 1, "", file)
    else:
        simple_tree_traverse(an_Incorporator.root, file)
    file.write(")")
    file.write(detailed_str(an_Incorporator.root))


def to_GoGui_sgf(a_str):
    moves = [gogui_style_str(mv) for mv in KifuParser.parse(a_str)][1:]
    return "(;FF[4]CA[UTF-8]AP[GoGui:1.5.1];" + ";".join(moves) + ")"