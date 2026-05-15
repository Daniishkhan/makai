# Multi-Leader Conflict

Scenario: Two mirror realms update the same gate or shop metadata while separated, then reconnect with different truths. The changed state is competing versions, and the promise is explicit conflict handling instead of silent overwrite.

Prove it with the test: compare both versions, apply the resolver, and identify which Makai fields are unsafe for last-write-wins.

Run:

```bash
uv run python -m pytest labs/level_05/tests/test_multi_leader_lww.py
```

Write through both versions, the chosen resolver, data-loss risk, and which Makai fields are unsafe for last-write-wins.
