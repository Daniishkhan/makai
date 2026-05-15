# Mission - Backpressure

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-04-backpressure`

## Incident Ticket

Producers keep adding work after the dispatch queue is full, hiding overload until latency explodes. Makai's promise is visible overload instead of silent collapse.

Suspected area: `src/system_design_labs/bounded_queue.py`.

## Reproduce

```bash
git switch mission/level-04-backpressure
uv run python -m pytest labs/level_04/tests/test_bounded_queue.py
```

Expected starter-branch result: an overflow-policy test fails.

## Read First

Read `labs/level_04/tests/test_bounded_queue.py`.

## Inspect Real Code

Trace `BoundedQueue.enqueue`, `dequeue`, and `snapshot`.

## Concepts To Explore

- Backpressure
- Bounded queue
- Reject-new policy
- Drop-oldest policy
- Overload signaling

## Fix Constraints

- Change the implementation, not the tests.
- Keep `BoundedQueue` API unchanged.
- `reject_new` must refuse new work without mutating the queue.
- `drop_oldest` must preserve newest work by evicting the oldest item.

## Report Template

Create `labs/level_04/exercises/backpressure/REPORT.md` after the fix.

```md
# Report - Backpressure

## Incident
What overload promise did Makai break?

## Evidence
Which test failed, and what queue state proved it?

## Root Cause
Where did the overflow policy mutate the wrong state?

## Fix
How does the queue now signal or absorb overload?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What caller behavior or retry policy still needs design?
```

## Done

- `uv run python -m pytest labs/level_04/tests/test_bounded_queue.py` passes.
- `REPORT.md` is committed with the fix.
