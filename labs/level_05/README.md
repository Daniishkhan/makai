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

| Exercise | Mission | Starter branch | Test command |
| --- | --- | --- | --- |
| `exercises/replica_lag` | `exercises/replica_lag/MISSION.md` | `mission/level-05-replica-lag` | `uv run python -m pytest labs/level_05/tests/test_primary_replica.py` |
| `exercises/multi_leader_conflict` | `exercises/multi_leader_conflict/MISSION.md` | `mission/level-05-multi-leader-conflict` | `uv run python -m pytest labs/level_05/tests/test_multi_leader_lww.py` |
| `exercises/crdt_counters` | `exercises/crdt_counters/MISSION.md` | `mission/level-05-crdt-counters` | `uv run python -m pytest labs/level_05/tests/test_crdts.py` |
| `exercises/vector_clocks` | `exercises/vector_clocks/MISSION.md` | `mission/level-05-vector-clocks` | `uv run python -m pytest labs/level_05/tests/test_vector_clock.py` |
| `exercises/circuit_breaker` | `exercises/circuit_breaker/MISSION.md` | `mission/level-05-circuit-breaker` | `uv run python -m pytest labs/level_05/tests/test_circuit_breaker.py` |

## How To Work The Missions

`main` is the green reference. To practice the real repair loop, switch to the starter branch in the table, read the mission ticket, run the failing tests, inspect the named implementation, repair the mechanism, write `REPORT.md`, and commit the fix.

## DB Commands

```bash
uv run sdl-db migrate
uv run sdl-db seed
psql -d system_design_labs -c "SELECT aggregate_id, replicated_to_secondary FROM makai_level_05.replica_events ORDER BY event_id;"
```

## Workload Exercise

Run `uv run sdl-db workload --iterations 50`, then inspect replica lag and conflict rows. Decide which quest paths can tolerate stale reads and which require coordination.

## Definition of Done

- [ ] I traced primary/replica lag, last-write-wins, vector clocks, CRDT counters, and circuit breaker tests.
- [ ] On the mission branch, I reproduced the failing test before changing code.
- [ ] I can diagram a primary write, pending replica visibility, stale read, and failover consequence.
- [ ] I can decide which Makai paths tolerate stale reads and which must read primary or coordinate.
- [ ] I can detect concurrent updates and explain why last-write-wins can lose data.
- [ ] I can separate mergeable counters from exclusive ownership state such as gate claims.
- [ ] I can describe the circuit breaker states, the evidence that trips it, and the fallback question it does not answer.
- [ ] I ran `uv run python -m pytest labs/level_05/tests`.
- [ ] I wrote the exercise `REPORT.md` and committed the fix.

## Your write-up

- Which consistency, conflict, or dependency risk did the failing test expose?
- What mirror replica or conflict state changed?
- What invariant or user promise broke?
- What evidence did the debugger, test, or SQL output show?
- What mechanism fixes or contains it?
- What does this still not solve?

## Rubric

Strong answers are explicit about consistency needs per path. They do not apply CRDTs to exclusive gate ownership, and they do not treat failover as a substitute for conflict resolution.
