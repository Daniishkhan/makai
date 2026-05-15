# Mission - Consistent Hashing

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-04-consistent-hashing`

## Incident Ticket

The shop adds capacity during a rush, but a broken ring remaps too much of the realm. Makai's promise is scale-out with limited disruption.

Suspected area: `src/system_design_labs/consistent_hashing.py`.

## Reproduce

```bash
git switch mission/level-04-consistent-hashing
uv run python -m pytest labs/level_04/tests/test_consistent_hashing.py
```

Expected starter-branch result: the limited-movement test fails.

## Read First

Read `labs/level_04/tests/test_consistent_hashing.py`.

## Inspect Real Code

Trace:

- `ConsistentHashRing.add_node`
- `ConsistentHashRing.get_node`
- `movement_ratio`

## Concepts To Explore

- Hash ring
- Virtual nodes
- Key movement
- Balance vs disruption

## Fix Constraints

- Change the implementation, not the tests.
- Keep `ConsistentHashRing` API unchanged.
- Preserve stable ownership for unchanged rings.
- Add nodes so only some keys move when capacity changes.

## Report Template

Create `labs/level_04/exercises/consistent_hashing/REPORT.md` after the fix.

```md
# Report - Consistent Hashing

## Incident
What scale-out promise did Makai break?

## Evidence
Which test failed, and what movement proved it?

## Root Cause
Where did the ring fail to limit remapping?

## Fix
How does the ring now choose owners?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What operational data movement still needs planning?
```

## Done

- `uv run python -m pytest labs/level_04/tests/test_consistent_hashing.py` passes.
- `REPORT.md` is committed with the fix.
