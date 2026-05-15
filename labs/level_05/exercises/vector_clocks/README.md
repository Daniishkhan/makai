# Vector Clocks

Scenario: Two regions report different updates and the Gatehouse must decide whether one followed the other or both happened independently. The changed state is version metadata, and the promise is not to flatten concurrency into a false order.

Read the passing test as proof: it compares clocks, identifies concurrent evidence, and describes the conflict handling path and metadata cost.

Run:

```bash
uv run python -m pytest labs/level_05/tests/test_vector_clock.py
```

Write through the clock comparison, concurrent evidence, conflict handling path, and metadata costs.
