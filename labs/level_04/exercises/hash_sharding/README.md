# Hash Sharding

Scenario: Adventurer and shop keys need routes before one shard becomes the only crowded gate. The changed state is key-to-shard assignment, and the promise is predictable routing that does not replace correctness constraints.

Prove it with the test: inspect distribution, calculate movement when capacity changes, and call out hot-key risk.

Run:

```bash
uv run python -m pytest labs/level_04/tests/test_hash_sharding.py
```

Write through the key distribution, movement ratio, hot-key risk, and why sharding does not replace correctness constraints.
