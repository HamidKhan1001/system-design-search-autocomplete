import time
from collections import OrderedDict


class EdgeCache:
    """
    LRU cache simulating browser/CDN edge caching for autocomplete results.
    TTL-based expiry + capacity eviction.
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: float = 5.0):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self._store: OrderedDict = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> list | None:
        entry = self._store.get(key)
        if entry is None:
            self._misses += 1
            return None
        value, exp = entry
        if time.monotonic() > exp:
            del self._store[key]
            self._misses += 1
            return None
        self._store.move_to_end(key)
        self._hits += 1
        return value

    def set(self, key: str, value: list) -> None:
        self._store[key] = (value, time.monotonic() + self.ttl)
        self._store.move_to_end(key)
        if len(self._store) > self.max_size:
            self._store.popitem(last=False)

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    @property
    def size(self) -> int:
        return len(self._store)
