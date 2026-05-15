# Replica Lag

Scenario: Ava receives a confirmed shop upgrade, but the nearby mirror still shows the old state. The changed state is primary write plus pending replica visibility, and the promise is to recognize lag instead of declaring the upgrade lost.

Read the passing test as proof: it shows the stale read, pending replication state, and when a path must read from primary or coordinate.

Run:

```bash
uv run python -m pytest labs/level_05/tests/test_primary_replica.py
```

Write through the stale read, the pending replication state, when it is acceptable, and when the request must read from primary or coordinate.
