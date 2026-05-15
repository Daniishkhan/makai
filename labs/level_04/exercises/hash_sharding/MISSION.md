# Mission - Hash Sharding

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-04-hash-sharding`

## Incident Ticket

Adventurer and shop keys need predictable routes, but a broken sharder sends traffic without respecting the key space. Makai's promise is deterministic routing with clear capacity-change trade-offs.

Suspected area: `src/system_design_labs/hash_sharding.py`.

## Reproduce

```bash
git switch mission/level-04-hash-sharding
uv run python -m pytest labs/level_04/tests/test_hash_sharding.py
```

Expected starter-branch result: the movement or routing test fails.

## Read First

Read `labs/level_04/tests/test_hash_sharding.py`.

## Inspect Real Code

Trace `ModuloSharder.shard_for` and `movement_ratio`.

## Concepts To Explore

- Stable hash
- Modulo sharding
- Rebalancing cost
- Hot-key risk

## Fix Constraints

- Change the implementation, not the tests.
- Keep `ModuloSharder` API unchanged.
- Use stable hashing so the same key maps consistently.
- Preserve the expected high movement when bucket count changes.

## Report Template

Create `labs/level_04/exercises/hash_sharding/REPORT.md` after the fix.

```md
# Report - Hash Sharding

## Incident
What routing promise did Makai break?

## Evidence
Which test failed, and what distribution or movement proved it?

## Root Cause
Where did key-to-shard assignment go wrong?

## Fix
How does the sharder now route keys?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What does modulo sharding still do badly during capacity changes?
```

## Done

- `uv run python -m pytest labs/level_04/tests/test_hash_sharding.py` passes.
- `REPORT.md` is committed with the fix.
