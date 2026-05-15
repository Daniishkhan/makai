# Mission - Retry Schedule

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-03-retry-schedule`

`main` should stay green. The mission branch is intentionally broken so the tests become the incident spec and you repair the implementation.

## Incident Ticket

A shop provider blinks during the gate rush, and every stalled request retries too aggressively. Makai's promise is that retries should heal transient failure without becoming the outage.

The suspected area is `src/system_design_labs/retry_backoff.py`.

## Reproduce

```bash
git switch mission/level-03-retry-schedule
uv run python -m pytest labs/level_03/tests/test_retry_backoff.py
```

Expected starter-branch result: retry delays or max-attempt handling fails.

## Read First

Start with `labs/level_03/tests/test_retry_backoff.py`.

Read in this order:

1. `test_retries_transient_failure_with_backoff`
2. `test_stops_after_max_attempts`
3. `test_full_jitter_is_bounded_by_delay`

## Inspect Real Code

Open `src/system_design_labs/retry_backoff.py`.

Trace:

- `RetryPolicy.delay_for`
- `retry`

## Concepts To Explore

- Exponential backoff
- Retry budget
- Full jitter
- Transient vs permanent failure
- Retry storm

## Fix Constraints

- Change the implementation, not the tests.
- Preserve `RetryPolicy` fields and the `retry(...)` API.
- Calculate exponential delay by retry index.
- Stop after `max_attempts`.
- Keep full jitter bounded by the calculated delay.

## Report Template

Create `labs/level_03/exercises/retry_schedule/REPORT.md` after the fix.

```md
# Report - Retry Schedule

## Incident
What retry pressure promise did Makai break?

## Evidence
Which test failed first, and what timing proved the bug?

## Root Cause
Where did retry timing or stop behavior drift?

## Fix
What delay and attempt rules now protect the dependency?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What still needs dead-lettering, alerting, or caller cancellation?
```

## Done

- `uv run python -m pytest labs/level_03/tests/test_retry_backoff.py` passes.
- `REPORT.md` explains the incident, evidence, root cause, fix, verification, and remaining risk.
- Commit message names the mechanism, for example:

```bash
git add src/system_design_labs/retry_backoff.py labs/level_03/exercises/retry_schedule/REPORT.md
git commit -m "Fix Level 3 retry backoff schedule"
```
