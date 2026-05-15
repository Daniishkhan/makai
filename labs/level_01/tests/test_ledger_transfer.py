from uuid import uuid4

import psycopg
import pytest

from system_design_labs.makai.ledger import (
    InsufficientFunds,
    balance,
    connect,
    create_account,
    drop_schema,
    naive_transfer_without_transaction,
    setup_schema,
    transfer,
)


@pytest.fixture
def wallet_db():
    try:
        conn = connect()
    except psycopg.OperationalError as exc:
        pytest.skip(
            "Postgres is not reachable. Start Postgres or set "
            "MAKAI_DATABASE_URL."
        )
        raise exc

    schema = f"makai_ledger_test_{uuid4().hex}"
    setup_schema(conn, schema)
    alice = create_account(conn, "alice", 1000)
    bob = create_account(conn, "bob", 200)

    try:
        yield conn, alice, bob
    finally:
        drop_schema(conn, schema)
        conn.close()


def test_naive_transfer_can_lose_money_after_crash(wallet_db):
    conn, alice, bob = wallet_db

    with pytest.raises(RuntimeError):
        naive_transfer_without_transaction(
            conn,
            alice,
            bob,
            300,
            fail_after_debit=True,
        )

    assert balance(conn, alice) == 700
    assert balance(conn, bob) == 200


def test_successful_transfer_debits_and_credits(wallet_db):
    conn, alice, bob = wallet_db

    result = transfer(conn, alice, bob, 300)

    assert result.from_balance_cents == 700
    assert result.to_balance_cents == 500

    row = conn.execute("SELECT COUNT(*) AS count FROM ledger_entries").fetchone()
    assert row["count"] == 2


def test_insufficient_funds_rolls_back_everything(wallet_db):
    conn, alice, bob = wallet_db

    with pytest.raises(InsufficientFunds):
        transfer(conn, bob, alice, 500)

    assert balance(conn, alice) == 1000
    assert balance(conn, bob) == 200

    row = conn.execute("SELECT COUNT(*) AS count FROM transfers").fetchone()
    assert row["count"] == 0


def test_crash_after_debit_rolls_back_debit(wallet_db):
    conn, alice, bob = wallet_db

    with pytest.raises(RuntimeError):
        transfer(
            conn,
            alice,
            bob,
            300,
            fail_after_debit=True,
        )

    assert balance(conn, alice) == 1000
    assert balance(conn, bob) == 200

    ledger_row = conn.execute("SELECT COUNT(*) AS count FROM ledger_entries").fetchone()
    assert ledger_row["count"] == 0

    transfer_row = conn.execute("SELECT COUNT(*) AS count FROM transfers").fetchone()
    assert transfer_row["count"] == 0
