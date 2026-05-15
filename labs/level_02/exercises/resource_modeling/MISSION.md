# Mission - Gate Resource Modeling

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-02-resource-modeling`

`main` should stay green. The mission branch is intentionally broken so the tests become the incident spec and you repair the implementation.

## Incident Ticket

The Gatehouse allows the same player identity to appear twice when email casing changes, or lets a scarce gate slot drift away from one clear owner. Makai's promise is that users, gate slots, and reservations have explicit resource boundaries and uniqueness rules.

The suspected area is `src/system_design_labs/api_resource_modeling.py`.

## Reproduce

```bash
git switch mission/level-02-resource-modeling
uv run python -m pytest labs/level_02/tests/test_api_resource_modeling.py
```

Expected starter-branch result: at least one uniqueness or ownership test fails.

## Read First

Start with `labs/level_02/tests/test_api_resource_modeling.py`.

Read in this order:

1. `test_unique_email_constraint_is_enforced`
2. `test_gate_cannot_be_reserved_twice`
3. `test_reservation_links_user_and_gate`

## Inspect Real Code

Open `src/system_design_labs/api_resource_modeling.py`.

Trace:

- `GateReservationStore.create_user`
- `GateReservationStore.create_gate`
- `GateReservationStore.reserve_gate`

## Concepts To Explore

- Resource modeling
- Unique constraint
- Ownership boundary
- Case normalization
- Application checks vs database constraints

## Fix Constraints

- Change the implementation, not the tests.
- Keep the public dataclasses and method signatures unchanged.
- Enforce case-insensitive email uniqueness.
- Preserve the one-active-reservation-per-gate-slot invariant.
- Keep unknown user/gate checks explicit.

## Report Template

Create `labs/level_02/exercises/resource_modeling/REPORT.md` after the fix.

```md
# Report - Gate Resource Modeling

## Incident
What ownership or uniqueness promise did Makai break?

## Evidence
Which test failed first, and what state proved the bug?

## Root Cause
Where did the model fail to enforce the resource boundary?

## Fix
What rule now protects the user or gate slot?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What would still need database constraints or isolation in production?
```

## Done

- `uv run python -m pytest labs/level_02/tests/test_api_resource_modeling.py` passes.
- `REPORT.md` explains the incident, root cause, fix, verification, and remaining risk.
- Commit message names the mechanism, for example:

```bash
git add src/system_design_labs/api_resource_modeling.py labs/level_02/exercises/resource_modeling/REPORT.md
git commit -m "Fix Level 2 gate resource modeling"
```
