from __future__ import annotations

import pytest

from system_design_labs.workloads import (
    WalletStep,
    run_makai_quest_day_workloads,
    run_wallet_transfer_workload,
    simulate_concurrent_withdrawals,
    simulate_idempotent_payment_outbox_queue,
    simulate_sharding_cache_replication,
    simulate_gate_reservation_race,
)


def test_wallet_transfer_workload_tracks_conservation_with_injected_database_api():
    balances = {1: 1000, 2: 200, 3: 0}

    def transfer(_conn: object, from_account_id: int, to_account_id: int, amount: int) -> None:
        if balances[from_account_id] < amount:
            raise ValueError("insufficient funds")
        balances[from_account_id] -= amount
        balances[to_account_id] += amount

    def balance(_conn: object, account_id: int) -> int:
        return balances[account_id]

    summary = run_wallet_transfer_workload(
        object(),
        [
            WalletStep(1, 2, 300),
            WalletStep(2, 3, 50),
            WalletStep(3, 1, 9999),
        ],
        transfer=transfer,
        balance=balance,
        account_ids=[1, 2, 3],
    )

    assert summary.attempts == 3
    assert summary.successes == 2
    assert summary.failures == 1
    assert summary.metrics["before_total_cents"] == 1200
    assert summary.metrics["after_total_cents"] == 1200
    assert summary.metrics["money_conserved"] is True


def test_ticket_reservation_race_allows_exactly_one_winner():
    summary = simulate_gate_reservation_race(contenders=12)

    assert summary.attempts == 12
    assert summary.successes == 1
    assert summary.failures == 11
    assert summary.metrics["reservations_created"] == 1
    assert summary.metrics["single_owner"] is True


def test_concurrent_withdrawal_workload_exposes_lost_update_and_locked_fix():
    naive = simulate_concurrent_withdrawals(use_lock=False)
    locked = simulate_concurrent_withdrawals(use_lock=True)

    assert naive.successes == 2
    assert naive.metrics["ledger_matches_balance"] is False
    assert locked.successes == 1
    assert locked.failures == 1
    assert locked.metrics["ledger_matches_balance"] is True


def test_idempotent_payment_outbox_queue_suppresses_duplicate_delivery():
    summary = simulate_idempotent_payment_outbox_queue()

    assert summary.attempts == 3
    assert summary.successes == 1
    assert summary.metrics["orders_created"] == 1
    assert summary.metrics["outbox_events"] == 1
    assert summary.metrics["published_events"] == 1
    assert summary.metrics["first_processed"] is True
    assert summary.metrics["duplicate_delivery_suppressed"] is True


def test_sharding_cache_replication_workload_reports_tradeoffs():
    summary = simulate_sharding_cache_replication(keys=[f"user-{index}" for index in range(300)])

    assert summary.successes == 300
    assert summary.metrics["shards"] == 3
    assert summary.metrics["movement_ratio_after_adding_shard"] > 0.5
    assert summary.metrics["cache_loader_calls"] == 1
    assert summary.metrics["cache_hit_avoided_loader"] is True
    assert summary.metrics["stale_read_before_async_replay"] is True
    assert summary.metrics["replica_caught_up"] is True


def test_gate_run_workloads_return_named_summaries():
    summaries = run_makai_quest_day_workloads()

    assert {summary.name for summary in summaries} == {
        "gate_reservation_race",
        "coin_pouch_withdrawal_pressure",
        "shop_retry_dispatch_queue",
        "map_shard_mirror_pressure",
    }
    assert all(summary.attempts > 0 for summary in summaries)


def test_postgres_wallet_workload_smoke_skips_when_database_is_unavailable():
    psycopg = pytest.importorskip("psycopg")
    from uuid import uuid4

    from system_design_labs.makai.ledger import (
        balance,
        connect,
        create_account,
        drop_schema,
        setup_schema,
        transfer,
    )

    try:
        conn = connect()
    except psycopg.OperationalError as exc:
        pytest.skip(f"Postgres is not reachable: {exc}")

    schema = f"makai_workload_test_{uuid4().hex}"
    setup_schema(conn, schema)
    try:
        alice = create_account(conn, "alice", 1000)
        bob = create_account(conn, "bob", 200)

        summary = run_wallet_transfer_workload(
            conn,
            [WalletStep(alice, bob, 250), WalletStep(bob, alice, 75)],
            transfer=transfer,
            balance=balance,
            account_ids=[alice, bob],
        )

        assert summary.successes == 2
        assert summary.metrics["money_conserved"] is True
        assert summary.metrics[f"account_{alice}_balance_cents"] == 825
        assert summary.metrics[f"account_{bob}_balance_cents"] == 375
    finally:
        drop_schema(conn, schema)
        conn.close()
