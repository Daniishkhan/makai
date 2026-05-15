# Mission - Circuit Breaker

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-05-circuit-breaker`

## Incident Ticket

A final-tower dependency starts failing, but callers keep paying the latency cost. Makai's promise is to stop sending work once failure is clear, then probe recovery carefully.

Suspected area: `src/system_design_labs/circuit_breaker.py`.

## Reproduce

```bash
git switch mission/level-05-circuit-breaker
uv run python -m pytest labs/level_05/tests/test_circuit_breaker.py
```

Expected starter-branch result: threshold or half-open behavior fails.

## Read First

Read `labs/level_05/tests/test_circuit_breaker.py`.

## Inspect Real Code

Trace `CircuitBreaker.call`.

## Concepts To Explore

- Circuit breaker
- Closed/open/half-open states
- Failure threshold
- Recovery timeout
- Fallback behavior

## Fix Constraints

- Change the implementation, not the tests.
- Keep `CircuitBreaker` API unchanged.
- Open the circuit as soon as the failure threshold is reached.
- Reject calls while open until recovery timeout elapses.
- Close the circuit after a successful half-open probe.

## Report Template

Create `labs/level_05/exercises/circuit_breaker/REPORT.md` after the fix.

```md
# Report - Circuit Breaker

## Incident
What dependency-failure promise did Makai break?

## Evidence
Which test failed, and what breaker state proved it?

## Root Cause
Where did threshold or recovery handling go wrong?

## Fix
How do closed, open, and half-open transitions now work?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What fallback decision still needs product approval?
```

## Done

- `uv run python -m pytest labs/level_05/tests/test_circuit_breaker.py` passes.
- `REPORT.md` is committed with the fix.
