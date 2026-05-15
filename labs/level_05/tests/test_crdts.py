from system_design_labs.crdts import GCounter, PNCounter


def test_g_counter_merge_is_monotonic_and_idempotent():
    a = GCounter()
    b = GCounter()
    a.increment("a", 2)
    b.increment("b", 3)

    merged = a.merge(b).merge(b)

    assert merged.value() == 5


def test_pn_counter_can_decrement_and_merge():
    a = PNCounter()
    b = PNCounter()
    a.increment("a", 5)
    b.decrement("b", 2)

    assert a.merge(b).value() == 3
