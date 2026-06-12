from .trie import Trie
from .trending import TrendingEngine
from .cache import EdgeCache


class AutocompleteEngine:
    def __init__(self, cache_ttl: float = 5.0, top_k: int = 5):
        self.top_k = top_k
        self._trie = Trie()
        self._trending = TrendingEngine()
        self._cache = EdgeCache(ttl_seconds=cache_ttl)

    def index(self, query: str, score: int = 1) -> None:
        self._trie.insert(query, score)

    def query(self, prefix: str) -> list:
        cached = self._cache.get(prefix)
        if cached is not None:
            return cached
        results = self._trie.autocomplete(prefix, self.top_k)
        self._cache.set(prefix, results)
        return results

    def record_search(self, query: str) -> None:
        self._trending.record(query)
        self._trie.insert(query)

    def rebuild_trending(self) -> None:
        self._trending.rebuild_trie()

    def trending(self) -> list:
        return self._trending.trending()

    @property
    def cache(self) -> EdgeCache:
        return self._cache

    @property
    def cache_hit_rate(self) -> float:
        return self._cache.hit_rate
