# Mission - Replica Lag

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-05-replica-lag`

## Incident Ticket

Ava receives a confirmed shop upgrade, but failover promotes a mirror that never received the write. Makai's promise is that synchronous paths survive failover while async paths are clearly understood as risky.

Suspected area: `src/system_design_labs/primary_replica.py`.

## Reproduce

```bash
git switch mission/level-05-replica-lag
uv run python -m pytest labs/level_05/tests/test_primary_replica.py
```

Expected starter-branch result: synchronous failover does not preserve the write.

## Read First

Read `labs/level_05/tests/test_primary_replica.py`.

## Inspect Real Code

Trace `PrimaryReplicaStore.write`, `replicate_pending`, and `failover_to_replica`.

## Concepts To Explore

- Primary/replica replication
- Replica lag
- Synchronous vs asynchronous writes
- Failover
- Durability vs latency

## Fix Constraints

- Change the implementation, not the tests.
- Keep `PrimaryReplicaStore` API unchanged.
- Synchronous writes must update primary and replica before returning.
- Async writes must remain pending until `replicate_pending`.
- Failover must promote only replica-visible state.

## Report Template

Create `labs/level_05/exercises/replica_lag/REPORT.md` after the fix.

```md
# Report - Replica Lag

## Incident
What mirror-realm promise did Makai break?

## Evidence
Which test failed, and what failover state proved it?

## Root Cause
Where did synchronous replication fail to protect state?

## Fix
What now happens on synchronous and asynchronous writes?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
Which paths can tolerate stale reads, and which must coordinate?
```

## Done

- `uv run python -m pytest labs/level_05/tests/test_primary_replica.py` passes.
- `REPORT.md` is committed with the fix.
