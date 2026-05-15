# Ledger Transfer

Scenario: Ava funds her quest pouch, but the process crashes after the debit and before the Gatehouse credit. The changed state is wallet balance plus ledger evidence, and the broken promise is money conservation.

Read the passing test as proof: it shows the naive transfer can leak value, then shows how the reference path binds the debit, credit, and ledger rows inside one transaction.

Run:

```bash
uv run python -m pytest labs/level_01/tests/test_ledger_transfer.py
```

Write through the exposed crash window, the money-conservation invariant, the debugger or SQL evidence, the transaction fix, and the concurrency issues this does not cover.
