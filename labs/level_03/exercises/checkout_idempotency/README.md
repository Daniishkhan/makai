# Checkout Idempotency

Scenario: Cleo refreshes a slow shop checkout after a provider timeout, sending the same intent twice. The changed state is the checkout, charge, and key upgrade record, and the broken promise is duplicate request without duplicate effect.

Prove it with the test: store the request fingerprint, replay the completed response, and reject mismatched reuse of the same idempotency key.

Run:

```bash
uv run python -m pytest labs/level_03/tests/test_checkout_idempotency.py
```

Write through the duplicate request, stored fingerprint, replayed response, and the cases where idempotency still needs lock expiry and downstream care.
