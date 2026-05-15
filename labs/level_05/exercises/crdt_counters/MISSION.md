# Mission - CRDT Counters

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-05-crdt-counters`

## Incident Ticket

Mirror realms count final-tower events independently, but repeated merges inflate the count. Makai's promise is eventual convergence for merge-safe data.

Suspected area: `src/system_design_labs/crdts.py`.

## Reproduce

```bash
git switch mission/level-05-crdt-counters
uv run python -m pytest labs/level_05/tests/test_crdts.py
```

Expected starter-branch result: idempotent merge fails.

## Read First

Read `labs/level_05/tests/test_crdts.py`.

## Inspect Real Code

Trace `GCounter.merge`, `PNCounter.merge`, and `value`.

## Concepts To Explore

- CRDT
- G-Counter
- PN-Counter
- Idempotent merge
- Monotonic state

## Fix Constraints

- Change the implementation, not the tests.
- Keep counter APIs unchanged.
- Merging the same replica state repeatedly must not inflate counts.
- PN-Counter must merge positive and negative components separately.

## Report Template

Create `labs/level_05/exercises/crdt_counters/REPORT.md` after the fix.

```md
# Report - CRDT Counters

## Incident
What convergence promise did Makai break?

## Evidence
Which test failed, and what count proved it?

## Root Cause
Where did merge stop being idempotent?

## Fix
How are replica-local counts now merged?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
Why is this safe for counters but not exclusive gate ownership?
```

## Done

- `uv run python -m pytest labs/level_05/tests/test_crdts.py` passes.
- `REPORT.md` is committed with the fix.
