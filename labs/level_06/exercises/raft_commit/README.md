# Raft Commit

Scenario: A rescue-control entry reaches some tower nodes but not enough to rule the realm. The changed state is leader term, votes, and replicated log entries, and the promise is that Makai never announces commitment on minority belief.

Read the passing test as proof: it counts acknowledgements, identifies majority evidence, and explains what remains uncommitted when only a minority accepts.

Run:

```bash
uv run python -m pytest labs/level_06/tests/test_toy_raft.py
```

Write through leader term, votes, log replication, majority evidence, and what happens when only a minority acknowledges.
