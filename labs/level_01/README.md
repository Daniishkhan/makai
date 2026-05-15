# Level 01 - Coin Pouches And Invariants

## Incident Scene

Ava reaches the Gatehouse before the first door opens and moves coins into her quest pouch. The screen flashes, the process crashes, and the Gatehouse has no matching credit. Makai's first promise is basic trust: a pouch transfer may fail, but it must not create or destroy money.

## Outcomes

- Diagnose why a debit without a matching credit breaks the business invariant.
- Use a transaction to bind transfer rows and ledger rows.
- Scan pouch balances and ledger entries with maps before trusting a result.

## DSA Checkpoint

Maps, ledgers, and invariant scans. Build the habit of deriving totals from state and checking conservation after each operation.

## Exercises

| Exercise | Test command |
| --- | --- |
| `exercises/ledger_transfer` | `uv run python -m pytest labs/level_01/tests` |

## How To Read The Passing Tests

The tests should pass. Read `test_naive_transfer_can_lose_money_after_crash` as the incident evidence: the unsafe path debits Ava before the crash and leaves Makai with missing value. Then read the transaction tests as the reference proof that debit, credit, transfer row, and ledger rows now succeed or roll back together.

## DB Commands

```bash
uv run sdl-db migrate
uv run sdl-db seed
psql -d system_design_labs -c "SELECT wallet_id, balance_cents FROM makai_level_01.wallets ORDER BY wallet_id;"
```

## Workload Exercise

Run `uv run sdl-db workload --iterations 50`, then compare `SUM(balance_cents)` before and after another run. The total should stay fixed while ledger rows increase.

## Definition of Done

- [ ] I traced `naive_transfer_without_transaction` and `transfer` against the tests.
- [ ] I can explain why the naive-path test passes while still proving a real production risk.
- [ ] I can diagram the debit, credit, transfer row, ledger rows, transaction boundary, and crash window.
- [ ] I can name the money-conservation invariant and point to balance or ledger evidence.
- [ ] I can explain how rollback restores atomicity after a crash or insufficient funds.
- [ ] I can name what this fix does not solve, especially broader isolation or concurrent-write anomalies.
- [ ] I ran `uv run python -m pytest labs/level_01/tests`.

## Your write-up

- Which unsafe path or crash window did the passing test expose?
- What coin-pouch or ledger state changed?
- What invariant broke?
- What evidence did the debugger, test, or SQL output show?
- What reference mechanism fixes it?
- What does this still not solve?

## Rubric

Strong answers name the money-conservation invariant, identify the crash window between debit and credit, point to ledger row counts or balances as evidence, and explain the transaction boundary without claiming it solves every concurrent write anomaly.
