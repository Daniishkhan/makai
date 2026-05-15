# Mission - Rate Limiters

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-04-rate-limiters`

## Incident Ticket

The shop receives bursts faster than downstream systems can absorb. A broken limiter rejects later traffic even after time has passed. Makai's promise is controlled pressure with predictable refill or leak behavior.

Suspected areas:

- `src/system_design_labs/token_bucket.py`
- `src/system_design_labs/leaky_bucket.py`

## Reproduce

```bash
git switch mission/level-04-rate-limiters
uv run python -m pytest labs/level_04/tests/test_token_bucket.py labs/level_04/tests/test_leaky_bucket.py
```

Expected starter-branch result: refill or leak-over-time behavior fails.

## Read First

Read:

1. `labs/level_04/tests/test_token_bucket.py`
2. `labs/level_04/tests/test_leaky_bucket.py`

## Inspect Real Code

Trace `TokenBucket.allow`, `TokenBucket._refill`, `LeakyBucket.allow`, and `LeakyBucket._leak`.

## Concepts To Explore

- Token bucket
- Leaky bucket
- Burst allowance
- Smoothing
- Refill rate

## Fix Constraints

- Change the implementation, not the tests.
- Keep public APIs unchanged.
- Refill tokens based on elapsed time.
- Leak queued pressure based on elapsed time.
- Preserve rejection when capacity is exhausted.

## Report Template

Create `labs/level_04/exercises/rate_limiters/REPORT.md` after the fix.

```md
# Report - Rate Limiters

## Incident
What load-shaping promise did Makai break?

## Evidence
Which test failed, and what timing proved it?

## Root Cause
Where did elapsed time stop affecting capacity?

## Fix
How do tokens or leaked work now change over time?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What user experience trade-off remains when requests are rejected?
```

## Done

- `uv run python -m pytest labs/level_04/tests/test_token_bucket.py labs/level_04/tests/test_leaky_bucket.py` passes.
- `REPORT.md` is committed with the fix.
