# Mission - Concurrent Reservations

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-02-concurrent-reservations`

`main` should stay green. The mission branch is intentionally broken so the tests become the incident spec and you repair the implementation.

## Incident Ticket

Beau and Cleo hit the same scarce opening at the same time. Both requests observe enough balance before either write completes. Makai's promise is that only one contender can mutate scarce state when the balance can fund only one winner.

The suspected area is `src/system_design_labs/concurrent_withdrawal.py`.

## Reproduce

```bash
git switch mission/level-02-concurrent-reservations
uv run python -m pytest labs/level_02/tests/test_concurrent_withdrawal.py
```

Expected starter-branch result: the locked withdrawal test fails because both callers can succeed.

## Read First

Start with `labs/level_02/tests/test_concurrent_withdrawal.py`.

Read in this order:

1. `test_locked_withdraw_preserves_the_invariant`
2. `test_naive_withdraw_allows_two_successes_from_one_balance`

The naive test is a contrast path. Do not fix `naive_withdraw`; use it to understand the race.

## Inspect Real Code

Open `src/system_design_labs/concurrent_withdrawal.py`.

Trace:

- `Account.locked_withdraw`
- `Account.naive_withdraw`

## Concepts To Explore

- Critical section
- Race condition
- Mutual exclusion
- Check-then-act hazards
- Pessimistic locking

## Fix Constraints

- Change the implementation, not the tests.
- Keep the public `Account` API unchanged.
- Keep `naive_withdraw` unsafe as the teaching contrast.
- Make the balance check and mutation one protected critical section in `locked_withdraw`.

## Report Template

Create `labs/level_02/exercises/concurrent_reservations/REPORT.md` after the fix.

```md
# Report - Concurrent Reservations

## Incident
What fairness or ownership promise did Makai break?

## Evidence
Which test failed first, and what state proved the race?

## Root Cause
Where did check and mutation become separable?

## Fix
What critical section now protects the invariant?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What changes if this moves from an in-process lock to multiple processes or a database?
```

## Done

- `uv run python -m pytest labs/level_02/tests/test_concurrent_withdrawal.py` passes.
- `REPORT.md` explains the incident, root cause, fix, verification, and remaining risk.
- Commit message names the mechanism, for example:

```bash
git add src/system_design_labs/concurrent_withdrawal.py labs/level_02/exercises/concurrent_reservations/REPORT.md
git commit -m "Fix Level 2 concurrent reservation locking"
```
