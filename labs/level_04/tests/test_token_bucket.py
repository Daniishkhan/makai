from system_design_labs.token_bucket import TokenBucket


def test_allows_burst_up_to_capacity():
    bucket = TokenBucket(capacity=2, refill_rate_per_second=1)

    assert bucket.allow(now=0)
    assert bucket.allow(now=0)
    assert not bucket.allow(now=0)


def test_refills_over_time():
    bucket = TokenBucket(capacity=2, refill_rate_per_second=1)
    bucket.allow(now=0)
    bucket.allow(now=0)

    assert not bucket.allow(now=0.5)
    assert bucket.allow(now=1.0)
