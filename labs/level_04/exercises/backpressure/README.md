# Backpressure

Scenario: Viral gate-run traffic creates more shop and dispatch work than workers can drain. The changed state is bounded queue capacity and producer acceptance, and the promise is visible overload instead of hidden collapse.

Prove it with the test: show which producers are accepted, which are rejected, and what signal callers receive before latency explodes.

Run:

```bash
uv run python -m pytest labs/level_04/tests/test_bounded_queue.py
```

Write through queue capacity, rejected producers, latency risk, and the signal you would expose to callers.
