from system_design_labs.lru_cache import LRUCache


def test_evicts_least_recently_used_key():
    cache: LRUCache[str, int] = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1

    cache.put("c", 3)

    assert cache.get("b") is None
    assert cache.keys_lru_to_mru() == ["a", "c"]


def test_updating_key_refreshes_recency():
    cache: LRUCache[str, int] = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)

    assert cache.get("a") == 10
    assert cache.get("b") is None
