# Mission - Postgres Runner

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-06-postgres-runner`

## Incident Ticket

Final-tower operators reset Makai, but stale migration metadata survives and future runs become untrustworthy. Makai's promise is reproducible rebuild evidence across all six schemas.

Suspected area: `src/system_design_labs/db/runner.py`.

## Reproduce

```bash
git switch mission/level-06-postgres-runner
uv run python -m pytest labs/level_06/tests/test_db_runner.py
```

Expected starter-branch result: reset, migration discovery, seed, or workload runner tests fail.

## Read First

Read `labs/level_06/tests/test_db_runner.py`.

## Inspect Real Code

Trace:

- `discover_migrations`
- `apply_migrations`
- `drop_lab_schemas`
- `seed_sample_data`
- `workload`

## Concepts To Explore

- Migration runner
- Reset safety
- Schema metadata
- Seed data
- Workload evidence

## Fix Constraints

- Change the implementation, not the tests.
- Keep the `sdl-db` public commands unchanged.
- Reset must drop Makai schemas, legacy schemas, and migration metadata when requested.
- Migration discovery must be deterministic by numeric prefix.
- Seed/workload functions must continue writing across the expected Makai levels.

## Report Template

Create `labs/level_06/exercises/postgres_runner/REPORT.md` after the fix.

```md
# Report - Postgres Runner

## Incident
What rebuild promise did Makai break?

## Evidence
Which test failed, and what runner call proved it?

## Root Cause
Where did reset, migration, seed, or workload behavior drift?

## Fix
What runner behavior is now trustworthy again?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What would you verify against a real local Postgres instance?
```

## Done

- `uv run python -m pytest labs/level_06/tests/test_db_runner.py` passes.
- `REPORT.md` is committed with the fix.
