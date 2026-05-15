# Mission - Cache Stampede

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-04-cache-stampede`

## Incident Ticket

The hot gate-map cache expires while multiple adventurers refresh the same route. Makai's promise is that one expired key should not stampede the database.

Suspected areas:

- `src/system_design_labs/cache_stampede.py`
- `src/system_design_labs/request_coalescing.py`

## Reproduce

```bash
git switch mission/level-04-cache-stampede
uv run python -m pytest labs/level_04/tests/test_cache_stampede.py labs/level_04/tests/test_request_coalescing.py
```

Expected starter-branch result: the loader-call count test fails.

## Read First

Read:

1. `labs/level_04/tests/test_cache_stampede.py`
2. `labs/level_04/tests/test_request_coalescing.py`

## Inspect Real Code

Trace `CacheAside.get` and `RequestCoalescer.get`.

## Concepts To Explore

- Cache-aside
- TTL expiry
- Single-flight request coalescing
- Source of truth

## Fix Constraints

- Change the implementation, not the tests.
- Keep public APIs unchanged.
- Re-check cache state after acquiring the per-key lock.
- Ensure concurrent identical misses trigger one loader call.

## Report Template

Create `labs/level_04/exercises/cache_stampede/REPORT.md` after the fix.

```md
# Report - Cache Stampede

## Incident
What load promise did Makai break?

## Evidence
Which test failed, and what loader count proved it?

## Root Cause
Where did duplicate work slip through?

## Fix
What now coalesces identical in-flight work?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What source-of-truth and stale-data risks remain?
```

## Done

- `uv run python -m pytest labs/level_04/tests/test_cache_stampede.py labs/level_04/tests/test_request_coalescing.py` passes.
- `REPORT.md` is committed with the fix.
