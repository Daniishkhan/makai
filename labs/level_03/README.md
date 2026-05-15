# Level 03 - Shop Retries And Dispatch Safety

## Incident Scene

Cleo buys a key upgrade while the shop provider is slow. The browser refreshes, the same request returns, and the dispatch tower waits for a scroll that must describe committed truth. Makai's promise is sharper now: retries may repeat, but charges, upgrades, and dispatch effects must not multiply or lie.

## Outcomes

- Use idempotency keys to turn unsafe retries into safe replays.
- Publish shop-confirmed events through an outbox.
- Handle at-least-once delivery with dedupe and retry schedules.

## DSA Checkpoint

Queues, dedupe sets, and retry schedules. Track which dispatch messages have been seen, which are visible, and which should back off.

## Exercises

| Exercise | Test command |
| --- | --- |
| `exercises/checkout_idempotency` | `uv run python -m pytest labs/level_03/tests/test_checkout_idempotency.py` |
| `exercises/outbox_queue` | `uv run python -m pytest labs/level_03/tests/test_outbox.py labs/level_03/tests/test_message_queue.py` |
| `exercises/retry_schedule` | `uv run python -m pytest labs/level_03/tests/test_retry_backoff.py` |

## How To Read The Passing Tests

The tests should pass. Read them as shop and dispatch incident files: duplicate requests, mismatched idempotency keys, crashed handlers, duplicate message delivery, and synchronized retries are the risks. The passing assertions prove which state is cached, rejected, persisted, deduped, delayed, or retried.

## DB Commands

```bash
uv run sdl-db migrate
uv run sdl-db seed
psql -d system_design_labs -c "SELECT idempotency_key, status FROM makai_level_03.idempotency_keys ORDER BY created_at;"
```

## Workload Exercise

Run `uv run sdl-db workload --iterations 50`, then compare shop checkout rows, idempotency rows, outbox rows, and queue rows. Explain why duplicate attempts should not imply duplicate charges.

## Definition of Done

- [ ] I traced idempotency, outbox, queue, and retry code from tests to implementation.
- [ ] I can explain why the duplicate and retry tests pass while still describing incidents that would be dangerous without these mechanisms.
- [ ] I can diagram the checkout lifecycle: request key, fingerprint, in-progress lock, completed response, outbox row, queue delivery.
- [ ] I can explain the difference between duplicate request, duplicate business effect, and duplicate message delivery.
- [ ] I can show where the cached response and dispatch evidence are stored.
- [ ] I can name remaining risks: lock expiry, long-running handlers, poisoned messages, downstream side effects, and retry storms.
- [ ] I ran `uv run python -m pytest labs/level_03/tests`.

## Your write-up

- Which unsafe retry or dispatch path did the passing test expose?
- What shop checkout or dispatch state changed?
- What invariant broke?
- What evidence did the debugger, test, or SQL output show?
- What reference mechanism fixes it?
- What does this still not solve?

## Rubric

Strong answers separate request replay, business execution, and message delivery. They also name the remaining risks: poisoned messages, lock expiry, long-running handlers, and downstream side effects.
