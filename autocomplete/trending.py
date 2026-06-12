from collections import Counter
from .trie import Trie


class TrendingEngine:
    """
    Tracks query frequency and rebuilds Trie scores via map-reduce style aggregation.
    Window: fixed count of recent queries.
    """

    def __init__(self, window_size: int = 1000, top_k: int = 10):
        self.window_size = window_size
        self.top_k = top_k
        self._log: list = []
        self._counts: Counter = Counter()
        self._trie = Trie()

    def record(self, query: str) -> None:
        q = query.lower().strip()
        self._log.append(q)
        if len(self._log) > self.window_size:
            evicted = self._log.pop(0)
            self._counts[evicted] -= 1
            if self._counts[evicted] <= 0:
                del self._counts[evicted]
        self._counts[q] += 1

    def rebuild_trie(self) -> None:
        """Map-reduce: aggregate counts → insert into Trie with frequency scores."""
        self._trie = Trie()
        for query, count in self._counts.items():
            self._trie.insert(query, score=count)

    def suggest(self, prefix: str, top_k: int = 5) -> list:
        return self._trie.autocomplete(prefix, top_k)

    def trending(self) -> list:
        return [q for q, _ in self._counts.most_common(self.top_k)]

    @property
    def trie(self) -> Trie:
        return self._trie
