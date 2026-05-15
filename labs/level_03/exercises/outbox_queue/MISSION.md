# Mission - Outbox Queue

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-03-outbox-queue`

`main` should stay green. The mission branch is intentionally broken so the tests become the incident spec and you repair the implementation.

## Incident Ticket

The shop confirms an order, then crashes before the dispatch scroll is written. Makai's promise is that business state and dispatch intent commit together, and downstream queue delivery can be retried safely.

The suspected areas are `src/system_design_labs/outbox.py` and `src/system_design_labs/message_queue.py`.

## Reproduce

```bash
git switch mission/level-03-outbox-queue
uv run python -m pytest labs/level_03/tests/test_outbox.py labs/level_03/tests/test_message_queue.py
```

Expected starter-branch result: the outbox atomicity test fails, or queue dedupe/redelivery behavior fails.

## Read First

Start with:

1. `labs/level_03/tests/test_outbox.py`
2. `labs/level_03/tests/test_message_queue.py`

Read the rollback test before the publisher test.

## Inspect Real Code

Open:

- `src/system_design_labs/outbox.py`
- `src/system_design_labs/message_queue.py`

Trace:

- `InMemoryOutboxDB.create_order`
- `OutboxPublisher.publish_pending`
- `AtLeastOnceQueue.receive`
- `DeduplicatingConsumer.handle`

## Concepts To Explore

- Outbox pattern
- Atomic business write plus event intent
- At-least-once delivery
- Visibility timeout
- Consumer dedupe

## Fix Constraints

- Change the implementation, not the tests.
- Keep order creation and outbox event creation all-or-nothing.
- Preserve at-least-once queue redelivery until acknowledgement.
- Keep consumer dedupe based on message identity.

## Report Template

Create `labs/level_03/exercises/outbox_queue/REPORT.md` after the fix.

```md
# Report - Outbox Queue

## Incident
What dispatch truth promise did Makai break?

## Evidence
Which test failed first, and what state proved the bug?

## Root Cause
Where did business state and dispatch intent split?

## Fix
What now commits together, and what is retried or deduped later?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What still needs poison-message handling, broker durability, or downstream idempotency?
```

## Done

- `uv run python -m pytest labs/level_03/tests/test_outbox.py labs/level_03/tests/test_message_queue.py` passes.
- `REPORT.md` explains the incident, evidence, root cause, fix, verification, and remaining risk.
- Commit message names the mechanism, for example:

```bash
git add src/system_design_labs/outbox.py src/system_design_labs/message_queue.py labs/level_03/exercises/outbox_queue/REPORT.md
git commit -m "Fix Level 3 outbox queue safety"
```
