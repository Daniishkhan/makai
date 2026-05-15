from system_design_labs.multi_leader_lww import LWWRegister


def test_later_timestamp_wins():
    east = LWWRegister("east")
    west = LWWRegister("west")
    east.write("old-email", timestamp=10)
    west.write("new-email", timestamp=11)

    east.merge(west)

    assert east.current is not None
    assert east.current.value == "new-email"


def test_tie_breaker_loses_one_concurrent_write():
    east = LWWRegister("east")
    west = LWWRegister("west")
    east.write("alice@example.com", timestamp=10)
    west.write("alice@new.example", timestamp=10)

    east.merge(west)
    west.merge(east)

    assert east.current == west.current
    assert east.current.value == "alice@new.example"
