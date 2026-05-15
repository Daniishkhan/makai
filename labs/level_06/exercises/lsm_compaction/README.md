# LSM Compaction

Scenario: Gate-run writes pile up as many small sorted segments, and final-tower reads begin paying for yesterday's fragments. The changed state is memtable flushes and segment layout, and the promise is that write speed will not leave reads trapped forever.

Read the passing test as proof: it traces flushes, segment reads, compaction evidence, and the read/write trade-off.

Run:

```bash
uv run python -m pytest labs/level_06/tests/test_mini_lsm.py
```

Write through memtable flushes, segment reads, compaction evidence, and the read/write trade-off.
