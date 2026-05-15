import pytest

from system_design_labs.circuit_breaker import CircuitBreaker, CircuitOpen


def test_opens_after_failure_threshold():
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=10)

    for now in [0, 1]:
        with pytest.raises(RuntimeError):
            breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("down")), now=now)

    with pytest.raises(CircuitOpen):
        breaker.call(lambda: "ok", now=2)


def test_half_open_success_closes_circuit():
    breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=5)
    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("down")), now=0)

    assert breaker.call(lambda: "ok", now=6) == "ok"
    assert breaker.state == "closed"
