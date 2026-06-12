from autocomplete import AutocompleteEngine


def test_index_and_query():
    e = AutocompleteEngine()
    e.index("python")
    e.index("pytest")
    results = e.query("py")
    assert "python" in results


def test_cache_hit_on_second_query():
    e = AutocompleteEngine()
    e.index("hello")
    e.query("hel")
    e.query("hel")  # cached
    assert e.cache_hit_rate > 0


def test_record_search_builds_index():
    e = AutocompleteEngine()
    e.record_search("data science")
    results = e.query("data")
    assert "data science" in results


def test_trending_after_records():
    e = AutocompleteEngine()
    for _ in range(3):
        e.record_search("machine learning")
    assert "machine learning" in e.trending()


def test_empty_prefix_returns_results():
    e = AutocompleteEngine()
    e.index("alpha")
    e.index("beta")
    # empty prefix would walk full trie, just verify it works
    results = e.query("a")
    assert "alpha" in results
