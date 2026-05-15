# Rate Limiters

Scenario: The shop and dispatch tower receive bursts faster than downstream systems can absorb. The changed state is request allowance over time, and the promise is controlled pressure instead of cascading failure.

Read the passing tests as proof: they compare burst behavior, smoothing behavior, rejected requests, and the user experience trade-off.

Run:

```bash
uv run python -m pytest labs/level_04/tests/test_token_bucket.py labs/level_04/tests/test_leaky_bucket.py
```

Write through allowed requests, rejected requests, burst behavior, smoothing behavior, and the user experience trade-off.
