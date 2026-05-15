# Mission - LRU Cache

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-04-lru-cache`

## Incident Ticket

Gate maps compete for cache space, but the cache evicts a recently used route. Makai's promise is that reads refresh recency before eviction decisions.

Suspected area: `src/system_design_labs/lru_cache.py`.

## Reproduce

```bash
git switch mission/level-04-lru-cache
uv run python -m pytest labs/level_04/tests/test_lru_cache.py
```

Expected starter-branch result: the least-recently-used eviction test fails.

## Read First

Read `labs/level_04/tests/test_lru_cache.py`.

## Inspect Real Code

Trace `LRUCache.get`, `LRUCache.put`, and `keys_lru_to_mru`.

## Concepts To Explore

- Recency
- Eviction policy
- Ordered map
- Cache hit behavior

## Fix Constraints

- Change the implementation, not the tests.
- Keep the `LRUCache` API unchanged.
- Refresh recency on `get`.
- Refresh recency when updating an existing key.

## Report Template

Create `labs/level_04/exercises/lru_cache/REPORT.md` after the fix.

```md
# Report - LRU Cache

## Incident
What cache promise did Makai break?

## Evidence
Which test failed, and what key order proved it?

## Root Cause
Where did recency stop being updated?

## Fix
How does the cache now maintain LRU order?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
When can LRU still be the wrong eviction signal?
```

## Done

- `uv run python -m pytest labs/level_04/tests/test_lru_cache.py` passes.
- `REPORT.md` is committed with the fix.
