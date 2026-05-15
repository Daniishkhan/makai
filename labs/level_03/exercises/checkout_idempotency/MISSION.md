# Mission - Checkout Idempotency

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-03-checkout-idempotency`

`main` should stay green. The mission branch is intentionally broken so the tests become the incident spec and you repair the implementation.

## Incident Ticket

Cleo refreshes a slow shop checkout after a provider timeout. The same idempotency key returns with the same payload, then later someone reuses the key with a different payload. Makai's promise is duplicate request without duplicate business effect.

The suspected area is `src/system_design_labs/makai/checkout.py`.

## Reproduce

```bash
git switch mission/level-03-checkout-idempotency
uv run python -m pytest labs/level_03/tests/test_checkout_idempotency.py
```

Expected starter-branch result: at least one replay, conflict, retry, or in-progress test fails.

## Read First

Start with `labs/level_03/tests/test_checkout_idempotency.py`.

Read in this order:

1. `test_duplicate_request_replays_cached_response`
2. `test_same_key_with_different_payload_is_rejected`
3. `test_failed_handler_allows_retry`
4. `test_in_progress_request_blocks_duplicate`

## Inspect Real Code

Open `src/system_design_labs/makai/checkout.py`.

Trace:

- `fingerprint`
- `IdempotencyMiddleware.transaction`
- `IdempotencyMiddleware.handle`

## Concepts To Explore

- Idempotency key
- Request fingerprint
- Cached response replay
- In-progress lock
- Retry after failed handler

## Fix Constraints

- Change the implementation, not the tests.
- Keep `IdempotencyMiddleware.handle(...)` and `IdempotencyResult` unchanged.
- Replay completed responses without calling the handler again.
- Reject same-key/different-payload reuse.
- Delete an in-progress key when the handler fails so the same request can retry.

## Report Template

Create `labs/level_03/exercises/checkout_idempotency/REPORT.md` after the fix.

```md
# Report - Checkout Idempotency

## Incident
What duplicate checkout promise did Makai break?

## Evidence
Which test failed first, and what state proved the bug?

## Root Cause
Where did request identity stop protecting business effects?

## Fix
What state is now stored, replayed, rejected, or cleared?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What still needs lock expiry, downstream idempotency, or provider-side care?
```

## Done

- `uv run python -m pytest labs/level_03/tests/test_checkout_idempotency.py` passes.
- `REPORT.md` explains the incident, evidence, root cause, fix, verification, and remaining risk.
- Commit message names the mechanism, for example:

```bash
git add src/system_design_labs/makai/checkout.py labs/level_03/exercises/checkout_idempotency/REPORT.md
git commit -m "Fix Level 3 checkout idempotency"
```
