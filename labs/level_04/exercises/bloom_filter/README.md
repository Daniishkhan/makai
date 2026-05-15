# Bloom Filter

Scenario: Bad retry keys hammer the Gatehouse lookup path while real adventurers wait. The changed state is the Bloom filter bitset, and the promise is cheap rejection for definite misses without treating maybe-present as final truth.

Prove it with the test: separate definitely-absent from maybe-present results and name the false-positive risk.

Run:

```bash
uv run python -m pytest labs/level_04/tests/test_bloom_filter.py
```

Write through definitely-absent results, maybe-present results, false-positive risk, and why a Bloom filter cannot be the final authority.
