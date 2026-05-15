from system_design_labs.primary_replica import PrimaryReplicaStore


def test_async_replication_can_lose_unreplicated_write_on_failover():
    store = PrimaryReplicaStore(synchronous=False)

    store.write("profile:1", "v1")
    promoted = store.failover_to_replica()

    assert "profile:1" not in promoted


def test_sync_replication_survives_failover():
    store = PrimaryReplicaStore(synchronous=True)

    store.write("profile:1", "v1")
    promoted = store.failover_to_replica()

    assert promoted["profile:1"] == "v1"


def test_async_replication_survives_after_pending_replication():
    store = PrimaryReplicaStore(synchronous=False)

    store.write("profile:1", "v1")
    store.replicate_pending()

    assert store.failover_to_replica()["profile:1"] == "v1"
