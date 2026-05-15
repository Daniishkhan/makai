from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from threading import Barrier, Lock, Thread
from typing import Iterable, Mapping, Protocol

from system_design_labs.api_resource_modeling import (
    GateReservationStore,
    GateSlotAlreadyReserved,
)
from system_design_labs.cache_stampede import CacheAside
from system_design_labs.concurrent_withdrawal import Account
from system_design_labs.hash_sharding import ModuloSharder, movement_ratio
from system_design_labs.message_queue import AtLeastOnceQueue, DeduplicatingConsumer
from system_design_labs.outbox import InMemoryOutboxDB, OutboxPublisher
from system_design_labs.primary_replica import PrimaryReplicaStore


class WalletTransfer(Protocol):
    def __call__(
        self,
        conn: object,
        from_account_id: int,
        to_account_id: int,
        amount_cents: int,
    ) -> object: ...


class BalanceReader(Protocol):
    def __call__(self, conn: object, account_id: int) -> int: ...


@dataclass(frozen=True)
class WorkloadSummary:
    name: str
    attempts: int
    successes: int
    failures: int
    metrics: Mapping[str, int | float | str | bool] = field(default_factory=dict)


@dataclass(frozen=True)
class WalletStep:
    from_account_id: int
    to_account_id: int
    amount_cents: int


def run_wallet_transfer_workload(
    conn: object,
    steps: Iterable[WalletStep],
    *,
    transfer: WalletTransfer,
    balance: BalanceReader,
    account_ids: Iterable[int],
) -> WorkloadSummary:
    """Drive Makai coin-pouch transfers with conservation checks."""

    account_ids = list(account_ids)
    before_total = sum(balance(conn, account_id) for account_id in account_ids)
    attempts = 0
    successes = 0
    failures = 0

    for step in steps:
        attempts += 1
        try:
            transfer(conn, step.from_account_id, step.to_account_id, step.amount_cents)
        except Exception:
            failures += 1
        else:
            successes += 1

    after_balances = {
        f"account_{account_id}_balance_cents": balance(conn, account_id)
        for account_id in account_ids
    }
    after_total = sum(after_balances.values())

    return WorkloadSummary(
        name="wallet_transfers",
        attempts=attempts,
        successes=successes,
        failures=failures,
        metrics={
            "before_total_cents": before_total,
            "after_total_cents": after_total,
            "money_conserved": before_total == after_total,
            **after_balances,
        },
    )


def simulate_gate_reservation_race(contenders: int = 8) -> WorkloadSummary:
    store = GateReservationStore()
    store.create_gate("gate_A1", "A", 1)
    for index in range(contenders):
        store.create_user(f"usr_{index}", f"user-{index}@example.com")

    lock = Lock()
    barrier = Barrier(contenders)
    outcomes: Counter[str] = Counter()

    def reserve(index: int) -> None:
        barrier.wait()
        try:
            with lock:
                store.reserve_gate(f"res_{index}", f"usr_{index}", "gate_A1")
        except GateSlotAlreadyReserved:
            outcomes["gate_already_reserved"] += 1
        else:
            outcomes["reserved"] += 1

    threads = [Thread(target=reserve, args=(index,)) for index in range(contenders)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return WorkloadSummary(
        name="gate_reservation_race",
        attempts=contenders,
        successes=outcomes["reserved"],
        failures=outcomes["gate_already_reserved"],
        metrics={
            "reservations_created": len(store.reservations),
            "single_owner": len(store.reservations) == 1,
        },
    )


def simulate_concurrent_withdrawals(
    *,
    opening_balance_cents: int = 100,
    withdrawal_cents: int = 80,
    contenders: int = 2,
    use_lock: bool = True,
) -> WorkloadSummary:
    account = Account(opening_balance_cents)
    barrier = Barrier(contenders) if not use_lock else None
    results: list[bool] = []
    results_lock = Lock()

    def withdraw() -> None:
        if use_lock:
            result = account.locked_withdraw(withdrawal_cents)
        else:
            result = account.naive_withdraw(withdrawal_cents, barrier)
        with results_lock:
            results.append(result)

    threads = [Thread(target=withdraw) for _ in range(contenders)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    successes = sum(1 for result in results if result)
    debited_cents = successes * withdrawal_cents
    return WorkloadSummary(
        name="coin_pouch_withdrawal_pressure",
        attempts=contenders,
        successes=successes,
        failures=contenders - successes,
        metrics={
            "opening_balance_cents": opening_balance_cents,
            "ending_balance_cents": account.balance_cents,
            "debited_cents": debited_cents,
            "ledger_matches_balance": opening_balance_cents - debited_cents
            == account.balance_cents,
            "used_lock": use_lock,
        },
    )


def simulate_idempotent_payment_outbox_queue() -> WorkloadSummary:
    outbox_db = InMemoryOutboxDB()
    publisher = OutboxPublisher(outbox_db)
    queue = AtLeastOnceQueue(visibility_timeout=5.0)
    consumer = DeduplicatingConsumer()

    attempts = 3
    outbox_db.create_order("order-1", 2500)
    for _ in range(attempts - 1):
        if "order-1" not in outbox_db.orders:
            outbox_db.create_order("order-1", 2500)

    publisher.publish_pending()
    for event in publisher.published:
        queue.send(f"{event.topic}:{event.payload['order_id']}")

    first_delivery = queue.receive(now=0.0)
    first_processed = consumer.handle(first_delivery) if first_delivery is not None else False
    redelivery = queue.receive(now=6.0)
    duplicate_suppressed = (
        not consumer.handle(redelivery) if redelivery is not None else False
    )
    if redelivery is not None:
        queue.ack(redelivery.id)

    return WorkloadSummary(
        name="shop_retry_dispatch_queue",
        attempts=attempts,
        successes=1,
        failures=attempts - 1,
        metrics={
            "orders_created": len(outbox_db.orders),
            "outbox_events": len(outbox_db.outbox),
            "published_events": len(publisher.published),
            "first_processed": first_processed,
            "duplicate_delivery_suppressed": duplicate_suppressed,
        },
    )


def simulate_sharding_cache_replication(
    keys: Iterable[str] | None = None,
) -> WorkloadSummary:
    keys = list(keys or (f"user-{index}" for index in range(200)))
    before = ModuloSharder(("shard-a", "shard-b", "shard-c"))
    after = ModuloSharder(("shard-a", "shard-b", "shard-c", "shard-d"))
    distribution = Counter(before.shard_for(key) for key in keys)

    cache = CacheAside(ttl_seconds=60)
    loader_calls = 0

    def loader() -> str:
        nonlocal loader_calls
        loader_calls += 1
        return "profile:user-42"

    cache.get("user-42", now=0, loader=loader)
    cache.get("user-42", now=1, loader=loader)

    replica_store = PrimaryReplicaStore(synchronous=False)
    replica_store.write("order-1", "paid")
    stale_before_replay = replica_store.replica.get("order-1") != "paid"
    replica_store.replicate_pending()

    return WorkloadSummary(
        name="map_shard_mirror_pressure",
        attempts=len(keys),
        successes=len(keys),
        failures=0,
        metrics={
            "shards": len(distribution),
            "largest_shard_load": max(distribution.values()),
            "smallest_shard_load": min(distribution.values()),
            "movement_ratio_after_adding_shard": movement_ratio(keys, before, after),
            "cache_loader_calls": loader_calls,
            "cache_hit_avoided_loader": loader_calls == 1,
            "stale_read_before_async_replay": stale_before_replay,
            "replica_caught_up": replica_store.replica.get("order-1") == "paid",
        },
    )


def run_makai_quest_day_workloads() -> list[WorkloadSummary]:
    # Mission starter bug: the final tower is missing the map/shard/mirror
    # pressure summary, so the full gate-run day is incomplete.
    return [
        simulate_gate_reservation_race(),
        simulate_concurrent_withdrawals(use_lock=True),
        simulate_idempotent_payment_outbox_queue(),
    ]
