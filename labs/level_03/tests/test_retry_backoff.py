import random

import pytest

from system_design_labs.retry_backoff import RetryPolicy, retry


def test_retries_transient_failure_with_backoff():
    attempts = 0
    delays: list[float] = []

    def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise TimeoutError("try again")
        return "ok"

    result = retry(flaky, RetryPolicy(max_attempts=4, base_delay=0.5), sleeper=delays.append)

    assert result == "ok"
    assert delays == [0.5, 1.0]


def test_stops_after_max_attempts():
    with pytest.raises(TimeoutError):
        retry(
            lambda: (_ for _ in ()).throw(TimeoutError("still down")),
            RetryPolicy(max_attempts=2, base_delay=1),
        )


def test_full_jitter_is_bounded_by_delay():
    policy = RetryPolicy(max_attempts=3, base_delay=10, jitter="full")

    delay = policy.delay_for(0, random.Random(1))

    assert 0 <= delay <= 10
