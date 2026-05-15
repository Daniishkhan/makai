# Mission - Bloom Filter

## Branches

- Reference branch: `main`
- Starter branch: `mission/level-04-bloom-filter`

## Incident Ticket

Bad retry keys hammer the lookup path, but a broken Bloom filter loses values that were definitely inserted. Makai's promise is cheap rejection for definite misses with no false negatives.

Suspected area: `src/system_design_labs/bloom_filter.py`.

## Reproduce

```bash
git switch mission/level-04-bloom-filter
uv run python -m pytest labs/level_04/tests/test_bloom_filter.py
```

Expected starter-branch result: inserted values are not always recognized.

## Read First

Read `labs/level_04/tests/test_bloom_filter.py`.

## Inspect Real Code

Trace `BloomFilter._indexes`, `add`, `__contains__`, and `estimated_false_positive_rate`.

## Concepts To Explore

- Bloom filter
- False positive
- False negative
- Hash functions
- Bitset membership

## Fix Constraints

- Change the implementation, not the tests.
- Keep the `BloomFilter` API unchanged.
- Set every hash-derived bit when adding a value.
- Membership should require every hash-derived bit to be present.
- False positives are acceptable; false negatives are not.

## Report Template

Create `labs/level_04/exercises/bloom_filter/REPORT.md` after the fix.

```md
# Report - Bloom Filter

## Incident
What lookup promise did Makai break?

## Evidence
Which test failed, and what membership result proved it?

## Root Cause
Where did the bitset lose inserted values?

## Fix
How does add and membership now use hash indexes?

## Verification
Which commands did you run, and what passed?

## Remaining Risk
Why can this still not be the final source of truth?
```

## Done

- `uv run python -m pytest labs/level_04/tests/test_bloom_filter.py` passes.
- `REPORT.md` is committed with the fix.
