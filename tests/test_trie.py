from autocomplete import Trie


def test_insert_and_search():
    t = Trie()
    t.insert("hello")
    assert t.search("hello") is True


def test_search_missing():
    t = Trie()
    assert t.search("missing") is False


def test_starts_with():
    t = Trie()
    t.insert("python")
    assert t.starts_with("pyt") is True
    assert t.starts_with("java") is False


def test_autocomplete_basic():
    t = Trie()
    for word in ["apple", "app", "application", "apply"]:
        t.insert(word)
    results = t.autocomplete("app")
    assert "app" in results
    assert "apple" in results


def test_autocomplete_top_k():
    t = Trie()
    for word in ["a1", "a2", "a3", "a4", "a5", "a6"]:
        t.insert(word)
    results = t.autocomplete("a", top_k=3)
    assert len(results) == 3


def test_autocomplete_no_prefix_match():
    t = Trie()
    t.insert("hello")
    assert t.autocomplete("xyz") == []


def test_score_prioritizes_results():
    t = Trie()
    t.insert("apple", score=1)
    t.insert("app", score=100)
    results = t.autocomplete("app", top_k=2)
    assert results[0] == "app"


def test_case_insensitive():
    t = Trie()
    t.insert("Python")
    assert t.search("python") is True
    assert t.starts_with("pyt") is True
