# Makai System Design Labs

Makai is a connected backend failure journey inspired by the shape of *Legend of Makai*: keys, doors, shop upgrades, hostile stages, time pressure, and a final rescue. The fantasy layer is not decoration. It gives every system-design concept a promise to protect.

Ava, Beau, and Cleo enter Makai through the Gatehouse. At first, the promise is simple: coin pouches should not lose money. Then the promise grows sharper: one gate slot should have one rightful holder, shop retries should not double-charge, dispatch messages should not lie about uncommitted state, hot maps should survive viral load, mirror realms should expose consistency trade-offs, and final-tower decisions should not commit without a majority.

The goal is not to memorize patterns. The goal is to debug a concrete betrayal of player trust, state the invariant, choose a mechanism, point to evidence, and explain what the mechanism still does not solve.

## Learning Contract

These labs are reading-first. They are not fill-in-the-blank kata, and the reference implementations are intentionally present. Senior system work often starts with unfamiliar code that already runs; the practice here is to read it, trace it, diagram it, diagnose it, and explain the trade-offs clearly enough that implementation becomes the easy part.

The test suite is expected to pass. Green tests do not mean there is nothing to find. In this repo, tests are completed incident files: some expose an unsafe path, some prove the safer mechanism, and some compare trade-offs under pressure. Your job is to read the passing test, locate the production risk in the implementation, and explain why the reference path keeps Makai's promise.

Use each lab in this loop:

1. Run the test or workload to collect green evidence, not to wait for a red suite.
2. Read the test as the incident report: what promise is being checked, and what state proves it?
3. Trace the implementation and schema that own the state transition.
4. Find the unsafe path, pressure case, or trade-off the test is pointing at.
5. Draw a small diagram: data flow, state transition, contention window, queue path, replica path, or consensus path.
6. Write the diagnosis in your own words: risk, invariant, evidence, reference mechanism, and remaining risk.
7. Treat code changes as optional experiments. If syntax or boilerplate is the only blocker, use Codex for that part after you understand the mechanism.

## Progression Map

| Level | Makai scenario | Outcomes | Exercises | Schema |
| --- | --- | --- | --- | --- |
| 1 | Gatehouse coin trust | Preserve money, diagnose partial writes, use transaction boundaries | `labs/level_01/exercises` | `makai_level_01` |
| 2 | Gate fairness under pressure | Model adventurers/gates/slots, enforce uniqueness, reason about concurrent holds | `labs/level_02/exercises` | `makai_level_02` |
| 3 | Shop retries and truthful dispatch | Make retries safe, publish dispatches through outbox/queue paths | `labs/level_03/exercises` | `makai_level_03` |
| 4 | Viral gate-run load | Use caches, shard maps, Bloom filters, coalescing, and rate limiters | `labs/level_04/exercises` | `makai_level_04` |
| 5 | Mirror-realm consistency | Compare consistency models, detect conflicts, merge counters, isolate failures | `labs/level_05/exercises` | `makai_level_05` |
| 6 | Final-tower coordination | Run the local Postgres flow, practice LSM and Raft drills, explain trade-offs | `labs/level_06/exercises` | `makai_level_06` |

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

A level is done when a passing test file is no longer just green; you can explain why each important assertion exists. That means you can:

- Reproduce the failure, unsafe path, or pressure case inside the passing tests or Postgres workload.
- Name the promise Makai made to the player or operator.
- Name the Makai state that changed: coin pouch, gate slot, key, shop checkout, dispatch, cache ward, shard route, mirror replica, or final-tower drill.
- State the invariant in one sentence.
- Point to evidence from a test, debugger session, SQL query, or workload row count.
- Draw the smallest useful diagram of the state transition, data flow, or failure window.
- Explain the reference mechanism that fixes, prevents, or contains the issue.
- Explain what the mechanism does not solve.
- Run the level tests and write a short diagnosis in your own words before reading any review notes.

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
