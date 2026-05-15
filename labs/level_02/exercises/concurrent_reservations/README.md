# Concurrent Reservations

Scenario: Beau and Cleo hit the same scarce opening before either request sees the other's write. The changed state is a gate slot or pouch balance that accepts too many winners, and the broken promise is exclusive ownership under contention.

Prove it with the test: expose the interleaving, then show which locking or isolation mechanism keeps the loser from mutating state.

Run:

```bash
uv run python -m pytest labs/level_02/tests/test_concurrent_withdrawal.py
```

Write through the interleaving, which state changed twice, the invariant that failed, and the locking or isolation mechanism that prevents it.
