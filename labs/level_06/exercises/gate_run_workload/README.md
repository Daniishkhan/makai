# Gate-Run Workload

Scenario: The full Gate Run compresses the whole realm into one day: pouches move, slots contend, shop retries happen, dispatches leave, maps heat up, and mirrors lag. The changed state crosses every earlier promise.

Prove it with the test: connect pouch conservation, gate contention, idempotent checkout, outbox delivery, map-cache pressure, and replica lag into one explanation.

Run:

```bash
uv run python -m pytest labs/level_06/tests/test_gate_run_workloads.py
```

Write through pouch conservation, gate contention, idempotent shop checkout, outbox delivery, map-cache pressure, and mirror-replica lag.
