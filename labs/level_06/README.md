# Level 06 - Final Tower Synthesis

## Incident Scene

The final tower opens and every earlier promise comes due at once: pouches must balance, slots must stay exclusive, retries must be safe, dispatches must follow committed state, hot paths must hold, mirrors must be understood, and rescue-control entries must not commit on minority belief. This level asks you to operate Makai as one system, then explain which mechanisms protected trust and which only bought time.

## Outcomes

- Run migrations, seed data, workload, and status checks against local Postgres.
- Explain how LSM compaction changes read/write trade-offs.
- Explain Raft majority commit and why minority acknowledgements are not enough.

## DSA Checkpoint

LSM compaction and Raft majority commit. Practice reading state transitions, not just naming the algorithms.

## Exercises

| Exercise | Test command |
| --- | --- |
| `exercises/lsm_compaction` | `uv run python -m pytest labs/level_06/tests/test_mini_lsm.py` |
| `exercises/raft_commit` | `uv run python -m pytest labs/level_06/tests/test_toy_raft.py` |
| `exercises/gate_run_workload` | `uv run python -m pytest labs/level_06/tests/test_gate_run_workloads.py` |
| `exercises/postgres_runner` | `uv run python -m pytest labs/level_06/tests/test_db_runner.py` |

## How To Read The Passing Tests

The tests should pass. Read this level as a synthesis drill: the workload proves the realm can be rebuilt and exercised, MiniLSM proves storage trade-offs, and ToyRaft proves majority commit boundaries. Green assertions are the evidence you use to write the final tower incident note.

## DB Commands

```bash
createdb system_design_labs || true
uv run sdl-db reset
uv run sdl-db migrate
uv run sdl-db seed
uv run sdl-db workload --iterations 50
uv run sdl-db status
```

## Workload Exercise

After the workload, verify six Makai schemas exist, no legacy schemas remain, pouch total is preserved, and ledger/outbox/queue rows exist. Then write a final-tower incident note: what degraded first, what protected correctness, and what you would monitor next.

## Definition of Done

- [ ] I rebuilt the local database with reset, migrate, seed, workload, and status commands.
- [ ] I traced `sdl-db` runner behavior, the in-memory workload, MiniLSM, and ToyRaft from tests to implementation.
- [ ] I can explain why a passing synthesis test still represents operational risk and coordination limits.
- [ ] I can diagram the full gate-run day across ledger, reservation, checkout, outbox, queue, cache, shard, replica, and final-tower state.
- [ ] I can point to workload evidence that schemas exist, legacy schemas are gone, pouch totals survived, and async rows were produced.
- [ ] I can explain LSM compaction using Makai write pressure and name the read/write trade-off.
- [ ] I can explain why Raft needs a majority for a committed rescue-control decision and what minority acknowledgement leaves unresolved.
- [ ] I can write a final incident note naming what degraded first, what protected correctness, and what I would monitor next.
- [ ] I ran `uv run python -m pytest labs/level_06/tests`.

## Your write-up

- Which operational risk, degradation, or coordination limit did the passing test expose?
- What final-tower state changed?
- What invariant or coordination rule mattered?
- What evidence did the debugger, test, or SQL output show?
- What reference mechanism fixes or contains it?
- What does this still not solve?

## Rubric

Strong answers synthesize the whole system: protected writes, scarce gate slots, safe retries, async delivery, load shaping, mirror-replica behavior, storage costs, and coordination limits.
