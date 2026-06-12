from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TrieNode:
    children: dict = field(default_factory=dict)
    is_end: bool = False
    score: int = 0


class Trie:
    def __init__(self):
        self._root = TrieNode()

    def insert(self, word: str, score: int = 1) -> None:
        node = self._root
        for ch in word.lower():
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True
        node.score = max(node.score, score)

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def autocomplete(self, prefix: str, top_k: int = 5) -> list:
        node = self._find_node(prefix)
        if node is None:
            return []
        results: list = []
        self._dfs(node, prefix.lower(), results)
        results.sort(key=lambda x: -x[1])
        return [word for word, _ in results[:top_k]]

    def _find_node(self, prefix: str):
        node = self._root
        for ch in prefix.lower():
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _dfs(self, node: TrieNode, prefix: str, results: list) -> None:
        if node.is_end:
            results.append((prefix, node.score))
        for ch, child in node.children.items():
            self._dfs(child, prefix + ch, results)
