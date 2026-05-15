# Ledger Transfer

Scenario: Ava funds her quest pouch, but the process crashes after the debit and before the Gatehouse credit. The changed state is wallet balance plus ledger evidence, and the broken promise is money conservation.

Prove it with the test: show the naive transfer can leak value, then bind the debit, credit, and ledger rows inside one transaction.

Run:

```bash
uv run python -m pytest labs/level_01/tests/test_ledger_transfer.py
```

Write through the failed state, the money-conservation invariant, the debugger or SQL evidence, the transaction fix, and the concurrency issues this does not cover.
