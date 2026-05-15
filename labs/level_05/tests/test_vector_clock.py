from system_design_labs.vector_clock import VectorClock


def test_clock_orders_causal_updates():
    first = VectorClock().tick("a")
    second = first.tick("a")

    assert first.compare(second) == "before"
    assert second.compare(first) == "after"


def test_clock_detects_concurrent_updates():
    left = VectorClock().tick("a")
    right = VectorClock().tick("b")

    assert left.compare(right) == "concurrent"
    assert left.merge(right).versions == {"a": 1, "b": 1}
