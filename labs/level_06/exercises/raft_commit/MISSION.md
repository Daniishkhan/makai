# Mission - Raft Commit

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-06-raft-commit`

## Incident Ticket

A rescue-control entry reaches the leader but not enough tower nodes. Makai announces commitment anyway. The promise is that minority belief never becomes a committed decision.

Suspected area: `src/system_design_labs/toy_raft.py`.

## Reproduce

```bash
git switch mission/level-06-raft-commit
uv run python -m pytest labs/level_06/tests/test_toy_raft.py
```

Expected starter-branch result: the no-majority commit test fails.

## Read First

Read `labs/level_06/tests/test_toy_raft.py`.

## Inspect Real Code

Trace `ToyRaftCluster.majority`, `elect_leader`, `set_online`, and `append`.

## Concepts To Explore

- Raft majority
- Leader election
- Log replication
- Commit index
- Minority partition

## Fix Constraints

- Change the implementation, not the tests.
- Keep `ToyRaftCluster` API unchanged.
- A leader needs majority votes to be elected.
- A log entry commits only after replication to a majority of nodes.
- Minority acknowledgement must leave `commit_index` unchanged.

## Report Template

Create `labs/level_06/exercises/raft_commit/REPORT.md` after the fix.

```md
# Report - Raft Commit

## Incident
What coordination promise did Makai break?

## Evidence
Which test failed, and what commit index proved it?

## Root Cause
Where did minority acknowledgement become commitment?

## Fix
How does the cluster now count majority?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
What real Raft behavior is still outside this toy model?
```

## Done

- `uv run python -m pytest labs/level_06/tests/test_toy_raft.py` passes.
- `REPORT.md` is committed with the fix.
