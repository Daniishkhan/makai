# Cache Stampede

Scenario: The hot gate-map cache expires while thousands of adventurers refresh the same route. The changed state is cache entries and in-flight loaders, and the promise is that one expired map should not stampede the database.

Prove it with the tests: show cache miss evidence, coalesced loader calls, and where the source of truth still lives.

Run:

```bash
uv run python -m pytest labs/level_04/tests/test_cache_stampede.py labs/level_04/tests/test_request_coalescing.py
```

Write through cache miss evidence, coalesced loader calls, stale-data risk, and where the source of truth still lives.
