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

- [ ] I traced cache-aside, request coalescing, LRU, sharding, Bloom filter, rate limiter, and bounded queue tests.
- [ ] I can diagram the hot gate-map read path and mark where load is shaped before it reaches source-of-truth state.
- [ ] I can explain what happens when the cache expires under load and how coalescing changes backend pressure.
- [ ] I can compare modulo sharding with consistent hashing using movement evidence from the tests.
- [ ] I can explain Bloom filter false positives and rate-limit decisions without treating them as correctness mechanisms.
- [ ] I can choose between token bucket, leaky bucket, and bounded queue for a specific gate-run pressure case.
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
