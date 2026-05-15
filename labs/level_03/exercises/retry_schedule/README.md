# Retry Schedule

Scenario: A provider blinks during the gate rush and every stalled shop request tries again on the same beat. The changed state is the retry schedule, and the promise is that retries should heal transient failure without becoming the outage.

Read the passing test as proof: it classifies the failure, calculates backoff with jitter, and shows when attempts should stop or route to review.

Run:

```bash
uv run python -m pytest labs/level_03/tests/test_retry_backoff.py
```

Write through the failure class, next-attempt schedule, jitter evidence, and the point where retries should stop or route to review.
