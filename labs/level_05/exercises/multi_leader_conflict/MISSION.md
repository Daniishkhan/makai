# Mission - Multi-Leader Conflict

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-05-multi-leader-conflict`

## Incident Ticket

Two mirror realms update the same gate note during a partition. When they reconnect, Makai silently chooses the wrong winner. The promise is explicit, deterministic conflict handling, not accidental overwrite.

Suspected area: `src/system_design_labs/multi_leader_lww.py`.

## Reproduce

```bash
git switch mission/level-05-multi-leader-conflict
uv run python -m pytest labs/level_05/tests/test_multi_leader_lww.py
```

Expected starter-branch result: timestamp tie handling fails.

## Read First

Read `labs/level_05/tests/test_multi_leader_lww.py`.

## Inspect Real Code

Trace `LWWRegister.write` and `LWWRegister.merge`.

## Concepts To Explore

- Multi-leader replication
- Last-write-wins
- Tie breaker
- Silent data loss
- Conflict resolution policy

## Fix Constraints

- Change the implementation, not the tests.
- Keep `LWWRegister` API unchanged.
- Later timestamps must win.
- Equal timestamps must use deterministic node-id tie breaking.
- Be explicit in the report about why LWW is unsafe for some fields.

## Report Template

Create `labs/level_05/exercises/multi_leader_conflict/REPORT.md` after the fix.

```md
# Report - Multi-Leader Conflict

## Incident
What conflict-handling promise did Makai break?

## Evidence
Which test failed, and what versions proved it?

## Root Cause
Where did the resolver become non-deterministic or lossy?

## Fix
What winner rule now applies?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
Which Makai fields should never use LWW?
```

## Done

- `uv run python -m pytest labs/level_05/tests/test_multi_leader_lww.py` passes.
- `REPORT.md` is committed with the fix.
