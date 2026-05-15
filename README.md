# Makai System Design Labs

Makai is a connected backend failure journey inspired by the shape of *Legend of Makai*: keys, doors, shop upgrades, hostile stages, time pressure, and a final rescue. The fantasy layer is not decoration. It gives every system-design concept a promise to protect.

Ava, Beau, and Cleo enter Makai through the Gatehouse. At first, the promise is simple: coin pouches should not lose money. Then the promise grows sharper: one gate slot should have one rightful holder, shop retries should not double-charge, dispatch messages should not lie about uncommitted state, hot maps should survive viral load, mirror realms should expose consistency trade-offs, and final-tower decisions should not commit without a majority.

The goal is not to memorize patterns. The goal is to debug a concrete betrayal of player trust, state the invariant, choose a mechanism, point to evidence, and explain what the mechanism still does not solve.

## Learning Contract

These labs are reading-first, but they should feel like real software engineering. Senior system work often starts with unfamiliar code, a failing behavior, and a business promise that must be restored. The practice here is to read the test, inspect the implementation, learn the system-design concept just in time, write the fix, verify it, explain it, and commit it cleanly.

`main` is the green reference implementation and source of truth. Mission branches are intentionally broken starter branches for hands-on repair. When a mission branch exists, switch to it, expect the relevant tests to fail, fix the implementation, write a short report, and commit your work.

Use mission labs in this loop:

1. Read the mission ticket and the failing test.
2. Run the failing test on the mission branch.
3. Inspect the real implementation and schema that own the state transition.
4. Explore the concept enough to explain the fix.
5. Patch the implementation.
6. Run the targeted tests, then the broader level tests.
7. Write `REPORT.md` with the incident, evidence, mechanism, verification, and remaining risk.
8. Commit the fix with a message that names the mechanism.

For levels that do not yet have a mission branch, `main` still works as a green reference workbook: read the passing tests as incident evidence, trace the implementation, diagram the mechanism, and write the diagnosis.

## Progression Map

| Level | Makai scenario | Outcomes | Exercises | Schema |
| --- | --- | --- | --- | --- |
| 1 | Gatehouse coin trust | Preserve money, diagnose partial writes, use transaction boundaries | `labs/level_01/exercises` | `makai_level_01` |
| 2 | Gate fairness under pressure | Model adventurers/gates/slots, enforce uniqueness, reason about concurrent holds | `labs/level_02/exercises` | `makai_level_02` |
| 3 | Shop retries and truthful dispatch | Make retries safe, publish dispatches through outbox/queue paths | `labs/level_03/exercises` | `makai_level_03` |
| 4 | Viral gate-run load | Use caches, shard maps, Bloom filters, coalescing, and rate limiters | `labs/level_04/exercises` | `makai_level_04` |
| 5 | Mirror-realm consistency | Compare consistency models, detect conflicts, merge counters, isolate failures | `labs/level_05/exercises` | `makai_level_05` |
| 6 | Final-tower coordination | Run the local Postgres flow, practice LSM and Raft drills, explain trade-offs | `labs/level_06/exercises` | `makai_level_06` |

## Mission Branches

| Branch | Exercise | Status |
| --- | --- | --- |
| `mission/level-01-ledger-transfer` | `labs/level_01/exercises/ledger_transfer` | Broken starter for transaction repair |

## Topics to Explore

Use [GLOSSARY.md](GLOSSARY.md) first for the project-local meaning, then search the topic names when you want deeper background. The goal is not to become encyclopedic before starting; it is to know which idea you are looking at while reading the code.

| Level | Start with these topics |
| --- | --- |
| 1 | [Invariant](GLOSSARY.md#invariant), [Atomicity](GLOSSARY.md#atomicity), [Transaction](GLOSSARY.md#transaction), concurrency, crash consistency, rollback, double-entry ledger |
| 2 | [Isolation](GLOSSARY.md#isolation), resource modeling, uniqueness constraints, race conditions, locks, optimistic vs pessimistic concurrency control |
| 3 | [Idempotency](GLOSSARY.md#idempotency), [Outbox](GLOSSARY.md#outbox), [At-Least-Once Delivery](GLOSSARY.md#at-least-once-delivery), request fingerprinting, retry backoff, jitter, consumer dedupe |
| 4 | [Cache Stampede](GLOSSARY.md#cache-stampede), [Consistent Hashing](GLOSSARY.md#consistent-hashing), [Bloom Filter](GLOSSARY.md#bloom-filter), [Backpressure](GLOSSARY.md#backpressure), cache-aside, request coalescing, LRU, token bucket, leaky bucket, bounded queue |
| 5 | [Replica Lag](GLOSSARY.md#replica-lag), [Vector Clock](GLOSSARY.md#vector-clock), [CRDT](GLOSSARY.md#crdt), primary/replica replication, multi-leader conflict, last-write-wins, circuit breaker, failover |
| 6 | [LSM Compaction](GLOSSARY.md#lsm-compaction), [Raft Majority Commit](GLOSSARY.md#raft-majority-commit), migration runners, seed data, workload design, consensus, storage read/write amplification |

## Run Everything

```bash
uv run python -m pytest
```

## Local Postgres

The public CLI stays `sdl-db`. It manages the six Makai schemas and resets old local schemas from the previous structure.

```bash
createdb system_design_labs || true
uv run sdl-db reset
uv run sdl-db migrate
uv run sdl-db seed
uv run sdl-db workload --iterations 50
uv run sdl-db status
```

The seed data creates one coherent Makai quest dataset: adventurers, coin pouches, a gate run, passage slots, reservations, shop idempotency records, dispatch messages, cache rows, shard rows, mirror-realm events, conflict notes, and final-tower drills. Treat those rows as evidence from the realm, not as fixtures to trust blindly.

## Definition of Done

A level is done when you can:

- Reproduce the failure, unsafe path, or pressure case with tests or the Postgres workload.
- Name the promise Makai made to the player or operator.
- Name the Makai state that changed: coin pouch, gate slot, key, shop checkout, dispatch, cache ward, shard route, mirror replica, or final-tower drill.
- State the invariant in one sentence.
- Point to evidence from a test, debugger session, SQL query, or workload row count.
- Draw the smallest useful diagram of the state transition, data flow, or failure window.
- Explain the mechanism that fixes, prevents, or contains the issue.
- Explain what the mechanism does not solve.
- For mission branches, commit the fix with a short `REPORT.md`.
- For reference-only levels, write a short diagnosis in your own words before reading any review notes.

## Project Map

| Path | Purpose |
| --- | --- |
| `labs/level_01` through `labs/level_06` | Level workbooks, exercises, and tests |
| `migrations` | Six narrative Makai migrations |
| `src/system_design_labs/makai` | Ledger, checkout, workload, and DB-facing Makai helpers |
| `src/system_design_labs` | Reusable system primitives and DSA checkpoints |
| `GLOSSARY.md` | Practical project-local vocabulary |

## Backlog

Future labs should be planned here before code exists.

| Idea | Makai hook | Likely level |
| --- | --- | --- |
| Quest search | Adventurers search gates by danger, reward, and region | 4 |
| Curse scoring | Risk holds a shop checkout before confirmation | 5 |
| Guild rollups | Final-tower dashboards need approximate counters | 6 |
