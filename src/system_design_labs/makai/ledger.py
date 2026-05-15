from __future__ import annotations

from dataclasses import dataclass
import os

import psycopg
from psycopg import Connection, sql
from psycopg.rows import dict_row


DEFAULT_DSN = "host=localhost dbname=postgres connect_timeout=2"


class InsufficientFunds(Exception):
    pass


@dataclass(frozen=True)
class TransferResult:
    transfer_id: int
    from_balance_cents: int
    to_balance_cents: int


def database_url() -> str:
    return (
        os.environ.get("MAKAI_DATABASE_URL")
        or os.environ.get("DATABASE_URL")
        or DEFAULT_DSN
    )


def connect(dsn: str | None = None) -> Connection:
    conn = psycopg.connect(dsn or database_url(), row_factory=dict_row)
    conn.autocommit = True
    return conn


def setup_schema(conn: Connection, schema: str = "makai_ledger_lab") -> None:
    conn.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema)))
    conn.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema)))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id BIGSERIAL PRIMARY KEY,
            owner TEXT NOT NULL,
            balance_cents BIGINT NOT NULL CHECK (balance_cents >= 0)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS transfers (
            id BIGSERIAL PRIMARY KEY,
            from_account_id BIGINT NOT NULL REFERENCES accounts(id),
            to_account_id BIGINT NOT NULL REFERENCES accounts(id),
            amount_cents BIGINT NOT NULL CHECK (amount_cents > 0),
            status TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ledger_entries (
            id BIGSERIAL PRIMARY KEY,
            transfer_id BIGINT NOT NULL REFERENCES transfers(id),
            account_id BIGINT NOT NULL REFERENCES accounts(id),
            direction TEXT NOT NULL CHECK (direction IN ('debit', 'credit')),
            amount_cents BIGINT NOT NULL CHECK (amount_cents > 0)
        )
        """
    )


def drop_schema(conn: Connection, schema: str) -> None:
    conn.execute(sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(sql.Identifier(schema)))


def create_account(conn: Connection, owner: str, balance_cents: int) -> int:
    row = conn.execute(
        """
        INSERT INTO accounts (owner, balance_cents)
        VALUES (%s, %s)
        RETURNING id
        """,
        (owner, balance_cents),
    ).fetchone()
    return int(row["id"])


def balance(conn: Connection, account_id: int) -> int:
    row = conn.execute(
        "SELECT balance_cents FROM accounts WHERE id = %s",
        (account_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown account: {account_id}")
    return int(row["balance_cents"])


def naive_transfer_without_transaction(
    conn: Connection,
    from_account_id: int,
    to_account_id: int,
    amount_cents: int,
    *,
    fail_after_debit: bool = False,
) -> None:
    if amount_cents <= 0:
        raise ValueError("amount must be positive")

    from_balance = balance(conn, from_account_id)
    if from_balance < amount_cents:
        raise InsufficientFunds("source account does not have enough balance")

    conn.execute(
        "UPDATE accounts SET balance_cents = balance_cents - %s WHERE id = %s",
        (amount_cents, from_account_id),
    )

    if fail_after_debit:
        raise RuntimeError("simulated crash after debit")

    conn.execute(
        "UPDATE accounts SET balance_cents = balance_cents + %s WHERE id = %s",
        (amount_cents, to_account_id),
    )


def transfer(
    conn: Connection,
    from_account_id: int,
    to_account_id: int,
    amount_cents: int,
    *,
    fail_after_debit: bool = False,
) -> TransferResult:
    if amount_cents <= 0:
        raise ValueError("amount must be positive")

    with conn.transaction():
        from_balance = balance(conn, from_account_id)
        if from_balance < amount_cents:
            raise InsufficientFunds("source account does not have enough balance")

        row = conn.execute(
            """
            INSERT INTO transfers (
                from_account_id, to_account_id, amount_cents, status
            )
            VALUES (%s, %s, %s, 'pending')
            RETURNING id
            """,
            (from_account_id, to_account_id, amount_cents),
        ).fetchone()
        transfer_id = int(row["id"])

        conn.execute(
            "UPDATE accounts SET balance_cents = balance_cents - %s WHERE id = %s",
            (amount_cents, from_account_id),
        )

        if fail_after_debit:
            raise RuntimeError("simulated crash after debit")

        conn.execute(
            "UPDATE accounts SET balance_cents = balance_cents + %s WHERE id = %s",
            (amount_cents, to_account_id),
        )
        conn.execute(
            """
            INSERT INTO ledger_entries (
                transfer_id, account_id, direction, amount_cents
            )
            VALUES
                (%s, %s, 'debit', %s),
                (%s, %s, 'credit', %s)
            """,
            (
                transfer_id,
                from_account_id,
                amount_cents,
                transfer_id,
                to_account_id,
                amount_cents,
            ),
        )
        conn.execute(
            "UPDATE transfers SET status = 'completed' WHERE id = %s",
            (transfer_id,),
        )

    return TransferResult(
        transfer_id=transfer_id,
        from_balance_cents=balance(conn, from_account_id),
        to_balance_cents=balance(conn, to_account_id),
    )
