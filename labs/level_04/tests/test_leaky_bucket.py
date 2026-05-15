from system_design_labs.leaky_bucket import LeakyBucket


def test_rejects_when_bucket_is_full():
    bucket = LeakyBucket(capacity=2, leak_rate_per_second=1)

    assert bucket.allow(now=0)
    assert bucket.allow(now=0)
    assert not bucket.allow(now=0)


def test_leaks_over_time_before_accepting_more():
    bucket = LeakyBucket(capacity=2, leak_rate_per_second=1)
    bucket.allow(now=0)
    bucket.allow(now=0)

    assert bucket.allow(now=1.0)
    assert bucket.level == 2
