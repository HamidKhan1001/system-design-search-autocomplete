from autocomplete import TrendingEngine


def test_record_and_trending():
    e = TrendingEngine()
    for _ in range(5):
        e.record("python")
    for _ in range(3):
        e.record("java")
    assert e.trending()[0] == "python"


def test_rebuild_trie_enables_suggest():
    e = TrendingEngine()
    e.record("machine learning")
    e.record("machine vision")
    e.rebuild_trie()
    results = e.suggest("machine")
    assert len(results) >= 1


def test_window_evicts_old():
    e = TrendingEngine(window_size=3)
    e.record("old")
    e.record("new1")
    e.record("new2")
    e.record("new3")  # "old" should be evicted
    assert e.trending()[0] != "old" or e._counts.get("old", 0) == 0


def test_case_normalized():
    e = TrendingEngine()
    e.record("Python")
    e.record("python")
    assert e._counts.get("python", 0) == 2


def test_empty_trending():
    e = TrendingEngine()
    assert e.trending() == []
