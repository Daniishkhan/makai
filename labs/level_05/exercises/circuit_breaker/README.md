# Circuit Breaker

Scenario: A final-tower dependency starts failing, and every caller keeps paying the latency cost. The changed state is breaker state, and the promise is to stop draining capacity once failure is clear.

Prove it with the test: move through closed, open, and half-open states, then name the fallback that still needs product approval.

Run:

```bash
uv run python -m pytest labs/level_05/tests/test_circuit_breaker.py
```

Write through closed, open, and half-open states, what evidence trips the breaker, and which fallback still needs product approval.
