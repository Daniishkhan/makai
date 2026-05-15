# Concurrent Reservations

Scenario: Beau and Cleo hit the same scarce opening before either request sees the other's write. The changed state is a gate slot or pouch balance that accepts too many winners, and the broken promise is exclusive ownership under contention.

Read the passing test as proof: it exposes the interleaving, then shows which locking or isolation mechanism keeps the loser from mutating state.

Run:

```bash
uv run python -m pytest labs/level_02/tests/test_concurrent_withdrawal.py
```

Write through the interleaving, which state would change twice, the invariant at risk, and the locking or isolation mechanism that prevents it.
