# Circuit Breaker

Scenario: A final-tower dependency starts failing, and every caller keeps paying the latency cost. The changed state is breaker state, and the promise is to stop draining capacity once failure is clear.

Read the passing test as proof: it moves through closed, open, and half-open states, then names the fallback that still needs product approval.

Run:

```bash
uv run python -m pytest labs/level_05/tests/test_circuit_breaker.py
```

Write through closed, open, and half-open states, what evidence trips the breaker, and which fallback still needs product approval.
