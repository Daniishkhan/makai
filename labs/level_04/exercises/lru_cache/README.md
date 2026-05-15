# LRU Cache

Scenario: Gate maps compete for cache space while the Gate Run keeps one route hot. The changed state is access order and eviction choice, and the promise is faster reads without pretending recency always equals value.

Read the passing test as proof: it shows the eviction evidence, cache-hit expectation, and the case where LRU chooses poorly.

Run:

```bash
uv run python -m pytest labs/level_04/tests/test_lru_cache.py
```

Write through the access order, eviction evidence, cache-hit expectation, and why recency can be the wrong signal.
