# Mission - Vector Clocks

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-05-vector-clocks`

## Incident Ticket

Two regions report different updates, and the Gatehouse incorrectly flattens concurrent events into a false order. Makai's promise is to detect concurrency before choosing a conflict path.

Suspected area: `src/system_design_labs/vector_clock.py`.

## Reproduce

```bash
git switch mission/level-05-vector-clocks
uv run python -m pytest labs/level_05/tests/test_vector_clock.py
```

Expected starter-branch result: concurrent clock detection fails.

## Read First

Read `labs/level_05/tests/test_vector_clock.py`.

## Inspect Real Code

Trace `VectorClock.tick`, `merge`, and `compare`.

## Concepts To Explore

- Vector clock
- Causal order
- Concurrent update
- Version metadata
- Conflict detection

## Fix Constraints

- Change the implementation, not the tests.
- Keep `VectorClock` API unchanged.
- Compare all nodes from both clocks.
- Return `concurrent` when each clock is ahead on at least one node.
- Merge by keeping the max version per node.

## Report Template

Create `labs/level_05/exercises/vector_clocks/REPORT.md` after the fix.

```md
# Report - Vector Clocks

## Incident
What ordering promise did Makai break?

## Evidence
Which test failed, and what clocks proved concurrency?

## Root Cause
Where did comparison collapse independent updates?

## Fix
How does comparison now separate before, after, equal, and concurrent?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What metadata cost or conflict-resolution work remains?
```

## Done

- `uv run python -m pytest labs/level_05/tests/test_vector_clock.py` passes.
- `REPORT.md` is committed with the fix.
