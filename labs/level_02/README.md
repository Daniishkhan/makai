# Level 02 - Gates, Keys, And Contention

## Incident Scene

The Gatehouse announces a narrow passage and Beau grabs the last open slot. At the same moment, another adventurer sees the same stale opening and claims it too. Makai's fairness promise is now on trial: a scarce door needs one rightful holder, not two lucky requests.

## Outcomes

- Model adventurers, gate runs, passage slots, and reservations as resources with clear ownership.
- Use uniqueness to enforce one active reservation per gate slot.
- Distinguish atomic writes from isolation problems under contention.

## DSA Checkpoint

Sets, unique indexes, gate maps, and contention. Treat a gate map as a finite set where membership and ownership must be unambiguous.

## Exercises

| Exercise | Mission | Starter branch | Test command |
| --- | --- | --- | --- |
| `exercises/resource_modeling` | `exercises/resource_modeling/MISSION.md` | `mission/level-02-resource-modeling` | `uv run python -m pytest labs/level_02/tests/test_api_resource_modeling.py` |
| `exercises/concurrent_reservations` | `exercises/concurrent_reservations/MISSION.md` | `mission/level-02-concurrent-reservations` | `uv run python -m pytest labs/level_02/tests/test_concurrent_withdrawal.py` |

## How To Work The Missions

`main` is the green reference. To practice the real repair loop, switch to the starter branch in the table, read the mission ticket, run the failing tests, inspect the named implementation, repair the mechanism, write `REPORT.md`, and commit the fix.

## DB Commands

```bash
uv run sdl-db migrate
uv run sdl-db seed
psql -d system_design_labs -c "SELECT seat_id, status FROM makai_level_02.seats ORDER BY seat_id LIMIT 10;"
```

## Workload Exercise

Run `uv run sdl-db workload --iterations 50`, then inspect `makai_level_02.reservations`. Explain why failed reservation attempts are not necessarily system failures.

## Definition of Done

- [ ] I traced the resource model in `GateReservationStore` and the contention model in `Account`.
- [ ] On the mission branch, I reproduced the failing test before changing code.
- [ ] I can diagram the boundary between adventurer, gate run, passage slot, reservation, and checkout.
- [ ] I can identify the state that grants ownership and the uniqueness rule that protects a gate slot.
- [ ] I can reproduce the contention case, name the single winner, and explain why the loser must not mutate state.
- [ ] I can explain why API shape and application checks still need database constraints or isolation under pressure.
- [ ] I ran `uv run python -m pytest labs/level_02/tests`.
- [ ] I wrote the exercise `REPORT.md` and committed the fix.

## Your write-up

- Which unsafe path or contention window did the failing test expose?
- What gate-slot or pouch state changed?
- What invariant broke?
- What evidence did the debugger, test, or SQL output show?
- What mechanism fixes it?
- What does this still not solve?

## Rubric

Strong answers connect resource modeling to enforcement: the API shape names the resource, but the unique active reservation rule protects the gate slot under pressure.
