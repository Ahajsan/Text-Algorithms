class End:
    def __init__(self, end):
        self.end = end

class Node:
    def __init__(self, start=-1, end=None):
        self.children = {}
        self.suffix_link = None
        self.start = start
        self.end = end
        self.id = -1
        self.parent = None
        self.suffix_index = -1  # <-- potrzebne do poprawnego zapisu pozycji

    def edge_length(self, current_position):
        if self.start == -1:
            return 0
        return (self.end.end if isinstance(self.end, End) else self.end) - self.start + 1

class SuffixTree:
    def __init__(self, text: str):
        self.text = text + "$"
        self.root = Node()
        self.root.suffix_link = self.root
        self.size = len(self.text)
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remaining_suffix_count = 0
        self.last_new_node = None
        self.leaf_end = End(-1)
        self.position = -1
        self.build_tree()

    def _edge_char(self, pos):
        return self.text[pos]

    def build_tree(self):
        for i in range(self.size):
            self._extend_suffix_tree(i)

    def _extend_suffix_tree(self, pos):
        self.leaf_end.end = pos
        self.remaining_suffix_count += 1
        self.last_new_node = None

        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = pos

            edge_char = self._edge_char(self.active_edge)
            if edge_char not in self.active_node.children:
                # Rule 2: tworzenie nowego liścia
                leaf = Node(start=pos, end=self.leaf_end)
                leaf.parent = self.active_node
                leaf.suffix_index = pos - self.remaining_suffix_count + 1
                self.active_node.children[edge_char] = leaf

                if self.last_new_node is not None:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None
            else:
                next_node = self.active_node.children[edge_char]
                edge_length = next_node.edge_length(pos)
                if self.active_length >= edge_length:
                    self.active_edge += edge_length
                    self.active_length -= edge_length
                    self.active_node = next_node
                    continue  # Skip/Count

                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    # Rule 3: przedłużenie istniejącego sufiksu
                    if self.last_new_node is not None and self.active_node != self.root:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None

                    self.active_length += 1
                    break

                # Rule 2: rozszczepienie krawędzi i dodanie nowego liścia
                split_end = next_node.start + self.active_length - 1
                split = Node(start=next_node.start, end=split_end)
                split.parent = self.active_node
                split.suffix_link = self.root
                self.active_node.children[edge_char] = split

                leaf = Node(start=pos, end=self.leaf_end)
                leaf.parent = split
                leaf.suffix_index = pos - self.remaining_suffix_count + 1
                split.children[self._edge_char(pos)] = leaf

                next_node.start += self.active_length
                split.children[self._edge_char(next_node.start)] = next_node
                next_node.parent = split

                if self.last_new_node is not None:
                    self.last_new_node.suffix_link = split

                self.last_new_node = split

            self.remaining_suffix_count -= 1

            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remaining_suffix_count + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link

    def find_pattern(self, pattern: str) -> list[int]:
        node = self.root
        i = 0
        while i < len(pattern):
            if pattern[i] not in node.children:
                return []
            child = node.children[pattern[i]]
            j = 0
            edge_len = child.edge_length(self.leaf_end.end)
            while j < edge_len and i < len(pattern):
                if pattern[i] != self.text[child.start + j]:
                    return []
                i += 1
                j += 1
            node = child

        results = []
        self._collect_leaf_positions(node, results)
        return sorted(results)

    def _collect_leaf_positions(self, node, results):
        if node.suffix_index != -1:
            results.append(node.suffix_index)
            return
        for child in node.children.values():
            self._collect_leaf_positions(child, results)


import unittest

class TestSuffixTree(unittest.TestCase):

    def assertPattern(self, text, pattern, expected):
        tree = SuffixTree(text)
        result = tree.find_pattern(pattern)
        self.assertEqual(sorted(result), sorted(expected),
                         msg=f"Text: '{text}', Pattern: '{pattern}' → Expected {expected}, got {result}")

    def test_basic_patterns(self):
        self.assertPattern("bananas", "ana", [1, 3])
        self.assertPattern("mississippi", "issi", [1, 4])
        self.assertPattern("abcabxabcd", "ab", [0, 3, 6])
        self.assertPattern("aaaaa", "aa", [0, 1, 2, 3])
        self.assertPattern("abcdef", "gh", [])
        self.assertPattern("abcabcabc", "abc", [0, 3, 6])
        self.assertPattern("ababab", "aba", [0, 2])
        self.assertPattern("abcdabscabcdabcabcd", "abcd", [0, 8, 15])
        self.assertPattern("xyzxyzxyz", "yzx", [1, 4])
        self.assertPattern("xyzxyzxyz", "xyzx", [0, 3])
        self.assertPattern("mississippi", "ppi", [8])
        self.assertPattern("mississippi", "ss", [2, 5])
        self.assertPattern("mississippi", "i", [1, 4, 7, 10])
        self.assertPattern("aaaaa", "a", [0, 1, 2, 3, 4])
        self.assertPattern("abc", "abc", [0])
        self.assertPattern("abc", "bc", [1])
        self.assertPattern("abc", "c", [2])
        self.assertPattern("abc", "d", [])

if __name__ == "__main__":
    unittest.main()


