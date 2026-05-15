# Bloom Filter

Scenario: Bad retry keys hammer the Gatehouse lookup path while real adventurers wait. The changed state is the Bloom filter bitset, and the promise is cheap rejection for definite misses without treating maybe-present as final truth.

Read the passing test as proof: it separates definitely-absent from maybe-present results and names the false-positive risk.

Run:

```bash
uv run python -m pytest labs/level_04/tests/test_bloom_filter.py
```

Write through definitely-absent results, maybe-present results, false-positive risk, and why a Bloom filter cannot be the final authority.
