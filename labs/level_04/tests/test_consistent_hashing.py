from system_design_labs.consistent_hashing import ConsistentHashRing, movement_ratio


def test_keys_have_stable_owner_until_ring_changes():
    ring = ConsistentHashRing(["a", "b", "c"], replicas=20)

    assert ring.get_node("user-1") == ring.get_node("user-1")


def test_adding_node_moves_only_some_keys():
    keys = [f"key-{index}" for index in range(200)]
    before = ConsistentHashRing(["a", "b", "c"], replicas=40)
    after = ConsistentHashRing(["a", "b", "c", "d"], replicas=40)

    moved = movement_ratio(keys, before, after)

    assert 0 < moved < 0.5
