# system-design-search-autocomplete

Real-time search typeahead (Google Suggest style) with sub-30ms responses via an in-memory Trie, frequency-weighted trending, and LRU/TTL edge cache.

## Architecture

```
User types "py..."
    │
EdgeCache.get("py")  ──hit──► return cached results immediately
    │ miss
    ▼
Trie.autocomplete("py", top_k=5)
    │  DFS from "py" node → collect all suffixes → sort by score → top-5
    ▼
EdgeCache.set("py", results, ttl=5s)
    │
return ["python", "pytest", "pypi", ...]
```

## Trending (map-reduce)

```
record_search(query)
    │
sliding window (last N queries) → Counter
    │
rebuild_trie()  ← map-reduce aggregate: count → score
    │
Trie reloaded with frequency-weighted scores
```

## Why sub-30ms

- Trie lookup: O(prefix_len + output_count), typically microseconds in-process
- Edge cache (CDN): prefixes like "py" cached at TTL=5s → 0ms after first hit
- No database round-trip on cache hit

## Running tests

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v   # 24 tests
```
