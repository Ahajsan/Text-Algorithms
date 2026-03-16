from collections import deque
from typing import List, Tuple, Optional


class AhoCorasickNode:
    def __init__(self):
        # TODO: Zainicjalizuj struktury potrzebne dla węzła w drzewie Aho-Corasick
        self.children = {}
        self.fail = None
        self.output = []
        self.parent = None
        self.char_from_parent = None


class AhoCorasick:
    def __init__(self, patterns: List[str]):
        # TODO: Zainicjalizuj strukturę Aho-Corasick i usuń puste wzorce
        self.root = AhoCorasickNode()
        self.patterns = [p for p in patterns if p]
        self._build_trie()
        self._build_failure_links()

    def _build_trie(self):
        """Builds the trie structure for the given patterns."""
        # TODO: Zaimplementuj budowanie drzewa typu trie dla podanych wzorców
        for pattern in self.patterns:
            node = self.root
            for char in pattern:
                if char not in node.children:
                    child = AhoCorasickNode()
                    child.parent = node
                    child.char_from_parent = char
                    node.children[char] = child
                node = node.children[char]
            node.output.append(pattern)

    def _build_failure_links(self):
        """Builds failure links and propagates outputs through them."""
        # TODO: Zaimplementuj tworzenie failure links
        # TODO: Utwórz kolejkę do przechodzenia przez drzewo w szerokość (BFS)
        queue = deque()
        self.root.fail = self.root

        # TODO: Zainicjalizuj łącza awaryjne dla węzłów na głębokości 1
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        # TODO: Użyj BFS do ustawienia łączy awaryjnych dla głębszych węzłów
        while queue:
            current_node = queue.popleft()
            for char, child in current_node.children.items():
                queue.append(child)

                fallback = current_node.fail
                while fallback is not self.root and char not in fallback.children:
                    fallback = fallback.fail
                child.fail= fallback.children[char] if char in fallback.children else self.root

                # TODO: Propaguj wyjścia przez łącza awaryjne
                child.output += child.fail.output

    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        Searches for all occurrences of patterns in the given text.

        Returns:
            List of tuples (start_index, pattern).
        """
        # TODO: Zaimplementuj wyszukiwanie wzorców w tekście
        # TODO: Zwróć listę krotek (indeks_początkowy, wzorzec)
        node = self.root
        results = []

        for index, char in enumerate(text):
            while node is not self.root and char not in node.children:
                node = node.fail
            node = node.children[char] if char in node.children else self.root

            for pattern in node.output:
                results.append((index - len(pattern) + 1, pattern))

        return results
