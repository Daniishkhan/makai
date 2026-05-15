# Postgres Runner

Scenario: The final-tower operators need to rebuild Makai from scratch, seed the realm, and run a real workload before trusting the drills. The changed state spans all six schemas, and the promise is reproducible evidence across the quest dataset.

Read the passing commands as proof: rebuild, seed, run the workload, and inspect rows that show schemas exist, work happened, and pouch totals survived.

Run:

```bash
createdb system_design_labs || true
uv run sdl-db reset
uv run sdl-db migrate
uv run sdl-db seed
uv run sdl-db workload --iterations 50
uv run sdl-db status
```

Write through which schemas exist, which rows prove the workload ran, and how pouch totals show the ledger invariant survived.
