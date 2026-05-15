# Consistent Hashing

Scenario: The shop adds capacity during the rush, but moving every key would shake the whole realm. The changed state is ring placement and key ownership, and the promise is scaling with limited disruption.

Read the passing test as proof: it measures remapped keys, describes the balance trade-off, and names the operational work still needed for data movement.

Run:

```bash
uv run python -m pytest labs/level_04/tests/test_consistent_hashing.py
```

Write through the ring placement, remapped keys, balance trade-off, and operational work still needed for data movement.
