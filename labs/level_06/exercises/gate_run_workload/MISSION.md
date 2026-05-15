# Mission - Gate-Run Workload

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-06-gate-run-workload`

## Incident Ticket

The final tower needs one coherent gate-run day, but a broken workload omits or misreports one of the incident summaries. Makai's promise is that the full system story can be replayed as evidence.

Suspected area: `src/system_design_labs/workloads.py`.

## Reproduce

```bash
git switch mission/level-06-gate-run-workload
uv run python -m pytest labs/level_06/tests/test_gate_run_workloads.py
```

Expected starter-branch result: a workload summary or metric test fails.

## Read First

Read `labs/level_06/tests/test_gate_run_workloads.py`.

## Inspect Real Code

Trace:

- `run_wallet_transfer_workload`
- `simulate_gate_reservation_race`
- `simulate_concurrent_withdrawals`
- `simulate_idempotent_payment_outbox_queue`
- `simulate_sharding_cache_replication`
- `run_makai_quest_day_workloads`

## Concepts To Explore

- Synthetic workload
- Conservation metric
- Contention evidence
- Idempotent dispatch
- Load and replica trade-offs

## Fix Constraints

- Change the implementation, not the tests.
- Keep `WorkloadSummary` and public function names unchanged.
- Preserve named summaries expected by the tests.
- Keep metrics truthful; do not hard-code values just to pass.

## Report Template

Create `labs/level_06/exercises/gate_run_workload/REPORT.md` after the fix.

```md
# Report - Gate-Run Workload

## Incident
What final-tower evidence promise did Makai break?

## Evidence
Which test failed, and what summary or metric proved it?

## Root Cause
Where did the workload omit or misreport system behavior?

## Fix
What workload evidence is now produced?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What real production signal would you still monitor?
```

## Done

- `uv run python -m pytest labs/level_06/tests/test_gate_run_workloads.py` passes.
- `REPORT.md` is committed with the fix.
