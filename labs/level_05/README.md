# Level 05 - Mirror Realms And Failure Handling

## Incident Scene

Makai opens mirror realms so distant players can keep moving. Ava sees a confirmed upgrade disappear from a nearby mirror, two regions rewrite the same gate note during a partition, and a flaky final-tower dependency starts draining callers. The promise is no longer that every view is fresh. The promise is that the system can name stale reads, conflicts, mergeable data, and dependency failure without pretending they are the same problem.

## Outcomes

- Reason about primary/replica lag and stale reads.
- Detect multi-leader conflicts with version metadata.
- Merge safe counters and isolate failing dependencies.

## DSA Checkpoint

Vector clocks, CRDT maps, topology reasoning, and failover state machines.

## Exercises

| Exercise | Test command |
| --- | --- |
| `exercises/replica_lag` | `uv run python -m pytest labs/level_05/tests/test_primary_replica.py` |
| `exercises/multi_leader_conflict` | `uv run python -m pytest labs/level_05/tests/test_multi_leader_lww.py` |
| `exercises/crdt_counters` | `uv run python -m pytest labs/level_05/tests/test_crdts.py` |
| `exercises/vector_clocks` | `uv run python -m pytest labs/level_05/tests/test_vector_clock.py` |
| `exercises/circuit_breaker` | `uv run python -m pytest labs/level_05/tests/test_circuit_breaker.py` |

## DB Commands

```bash
uv run sdl-db migrate
uv run sdl-db seed
psql -d system_design_labs -c "SELECT aggregate_id, replicated_to_secondary FROM makai_level_05.replica_events ORDER BY event_id;"
```

## Workload Exercise

Run `uv run sdl-db workload --iterations 50`, then inspect replica lag and conflict rows. Decide which quest paths can tolerate stale reads and which require coordination.

## Definition of Done

- [ ] I can explain when a stale replica read is acceptable.
- [ ] I can detect when two updates are concurrent instead of older/newer.
- [ ] I can explain why some counters merge safely and gate ownership does not.
- [ ] I can describe how the circuit breaker protects the caller.
- [ ] I ran `uv run python -m pytest labs/level_05/tests`.

## Your write-up

- What failed?
- What mirror replica or conflict state changed?
- What invariant or user promise broke?
- What evidence did the debugger, test, or SQL output show?
- What mechanism fixes or contains it?
- What does this still not solve?

## Rubric

Strong answers are explicit about consistency needs per path. They do not apply CRDTs to exclusive gate ownership, and they do not treat failover as a substitute for conflict resolution.
