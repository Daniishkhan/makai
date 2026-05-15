from system_design_labs.hash_sharding import ModuloSharder, movement_ratio


def test_same_key_maps_to_same_shard():
    sharder = ModuloSharder(("a", "b", "c"))

    assert sharder.shard_for("user-1") == sharder.shard_for("user-1")


def test_modulo_sharding_moves_many_keys_when_bucket_count_changes():
    keys = [f"key-{index}" for index in range(500)]
    before = ModuloSharder(("a", "b", "c"))
    after = ModuloSharder(("a", "b", "c", "d"))

    assert movement_ratio(keys, before, after) > 0.5
