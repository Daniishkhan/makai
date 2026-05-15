# CRDT Counters

Scenario: Mirror realms count final-tower events while partitions come and go. The changed state is replica-local counters, and the promise is eventual convergence for data that is safe to merge.

Prove it with the test: merge increments and decrements, show convergence, and explain why exclusive gate ownership is not this kind of data.

Run:

```bash
uv run python -m pytest labs/level_05/tests/test_crdts.py
```

Write through increments, decrements, merge evidence, convergence, and why exclusive gate ownership is not this kind of data.
