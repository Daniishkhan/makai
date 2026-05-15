# Mission - LSM Compaction

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-06-lsm-compaction`

## Incident Ticket

Gate-run writes pile up as sorted fragments, and final-tower reads return stale values. Makai's promise is that newest writes and tombstones are respected before compaction cleans up storage.

Suspected area: `src/system_design_labs/mini_lsm.py`.

## Reproduce

```bash
git switch mission/level-06-lsm-compaction
uv run python -m pytest labs/level_06/tests/test_mini_lsm.py
```

Expected starter-branch result: newest-value reads or compaction fails.

## Read First

Read `labs/level_06/tests/test_mini_lsm.py`.

## Inspect Real Code

Trace `MiniLSM.put`, `delete`, `get`, `flush`, and `compact`.

## Concepts To Explore

- LSM tree
- Memtable
- SSTable
- Tombstone
- Compaction

## Fix Constraints

- Change the implementation, not the tests.
- Keep `MiniLSM` API unchanged.
- Reads must prefer memtable over sstables.
- Reads across sstables must prefer newest segments.
- Compaction must keep newest live values and drop tombstones.

## Report Template

Create `labs/level_06/exercises/lsm_compaction/REPORT.md` after the fix.

```md
# Report - LSM Compaction

## Incident
What storage promise did Makai break?

## Evidence
Which test failed, and what read or segment state proved it?

## Root Cause
Where did newest-value or tombstone handling go wrong?

## Fix
How does the store now read and compact segments?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What read/write amplification trade-off remains?
```

## Done

- `uv run python -m pytest labs/level_06/tests/test_mini_lsm.py` passes.
- `REPORT.md` is committed with the fix.
