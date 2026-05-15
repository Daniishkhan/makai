# Ledger Transfer

Scenario: Ava funds her quest pouch, but the process crashes after the debit and before the Gatehouse credit. The changed state is wallet balance plus ledger evidence, and the broken promise is money conservation.

This exercise has a broken starter branch: `mission/level-01-ledger-transfer`.

Use [MISSION.md](MISSION.md) for the engineering loop: read the incident, run the failing tests, inspect the real implementation, explore atomicity and transactions, write the fix, verify it, write `REPORT.md`, and commit.

Run:

```bash
uv run python -m pytest labs/level_01/tests/test_ledger_transfer.py
```

Write through the exposed crash window, the money-conservation invariant, the debugger or SQL evidence, the transaction fix, and the concurrency issues this does not cover.
