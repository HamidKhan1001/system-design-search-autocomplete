import time
from autocomplete import EdgeCache


def test_set_and_get():
    c = EdgeCache()
    c.set("py", ["python", "pytest"])
    assert c.get("py") == ["python", "pytest"]


def test_miss_returns_none():
    c = EdgeCache()
    assert c.get("missing") is None


def test_hit_rate():
    c = EdgeCache()
    c.set("k", ["v"])
    c.get("k")     # hit
    c.get("nope")  # miss
    assert c.hit_rate == 0.5


def test_lru_eviction():
    c = EdgeCache(max_size=2)
    c.set("a", [])
    c.set("b", [])
    c.set("c", [])  # evicts "a"
    assert c.size == 2


def test_invalidate():
    c = EdgeCache()
    c.set("k", ["v"])
    c.invalidate("k")
    assert c.get("k") is None


def test_ttl_expiry():
    c = EdgeCache(ttl_seconds=0.01)
    c.set("k", ["v"])
    time.sleep(0.02)
    assert c.get("k") is None
