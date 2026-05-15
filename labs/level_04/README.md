# Level 04 - Maps, Shards, And Load Shaping

## Incident Scene

The Makai Gate Run goes viral overnight. Every adventurer hammers the same map, the shop line surges, shard routes wobble, and bad retry keys chew through capacity before real players reach the door. Makai's promise shifts from single-request correctness to survival under pressure: shape load without confusing scale tools for the source of truth.

## Outcomes

- Use cache-aside, request coalescing, and LRU eviction for hot map paths.
- Compare modulo sharding with a consistent hash ring.
- Use Bloom filters and rate limiters to shape load before it reaches core state.

## DSA Checkpoint

LRU, Bloom filters, consistent hash rings, token buckets, leaky buckets, and bounded queues.

## Exercises

| Exercise | Test command |
| --- | --- |
| `exercises/hash_sharding` and `exercises/consistent_hashing` | `uv run python -m pytest labs/level_04/tests/test_hash_sharding.py labs/level_04/tests/test_consistent_hashing.py` |
| `exercises/cache_stampede` and `exercises/lru_cache` | `uv run python -m pytest labs/level_04/tests/test_cache_stampede.py labs/level_04/tests/test_lru_cache.py labs/level_04/tests/test_request_coalescing.py` |
| `exercises/rate_limiters` and `exercises/backpressure` | `uv run python -m pytest labs/level_04/tests/test_token_bucket.py labs/level_04/tests/test_leaky_bucket.py labs/level_04/tests/test_bounded_queue.py` |
| `exercises/bloom_filter` | `uv run python -m pytest labs/level_04/tests/test_bloom_filter.py` |

## DB Commands

```bash
uv run sdl-db migrate
uv run sdl-db seed
psql -d system_design_labs -c "SELECT cache_key, expires_at FROM makai_level_04.cache_entries;"
```

## Workload Exercise

Run `uv run sdl-db workload --iterations 50`, then inspect cache rows, shard rows, and rate-limit buckets. Explain which paths are correctness mechanisms and which are load-shaping mechanisms.

## Definition of Done

- [ ] I can explain what happens when the gate-map cache expires under load.
- [ ] I can calculate why adding a modulo shard moves many keys.
- [ ] I can explain Bloom filter false positives without treating them as corruption.
- [ ] I can choose between token bucket, leaky bucket, and bounded queue for a gate-run path.
- [ ] I ran `uv run python -m pytest labs/level_04/tests`.

## Your write-up

- What failed?
- What cache, shard, or queue state changed?
- What invariant or service objective broke?
- What evidence did the debugger, test, or SQL output show?
- What mechanism fixes or contains it?
- What does this still not solve?

## Rubric

Strong answers avoid using scale tools as correctness tools. They state where correctness still lives, then describe how load-shaping protects the dependency that owns the truth.
