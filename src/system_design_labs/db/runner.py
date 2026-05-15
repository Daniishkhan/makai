from __future__ import annotations

import argparse
import os
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol

import psycopg


MAKAI_SCHEMAS = tuple(f"makai_level_{level:02d}" for level in range(1, 7))
PREVIOUS_NARRATIVE_SCHEMA_PREFIXES = ("lu" + "men", "ce" + "dar")
PREVIOUS_NARRATIVE_SCHEMAS = tuple(
    f"{prefix}_level_{level:02d}"
    for prefix in PREVIOUS_NARRATIVE_SCHEMA_PREFIXES
    for level in range(1, 7)
)
LEGACY_SCHEMA_PREFIX = "lab" + "_" + "we" + "ek"
LEGACY_SCHEMAS = tuple(f"{LEGACY_SCHEMA_PREFIX}_{index:02d}" for index in range(1, 9))
MIGRATION_SCHEMA = "system_design_labs"
MIGRATION_TABLE = "schema_migrations"
DEFAULT_DSN = "postgresql:///system_design_labs"


class Connection(Protocol):
    def execute(self, query: str, params: object | None = None) -> object:
        ...

    def commit(self) -> None:
        ...


@dataclass(frozen=True)
class Migration:
    version: str
    name: str
    path: Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_migrations_dir() -> Path:
    return repo_root() / "migrations"


def discover_migrations(migrations_dir: Path | None = None) -> list[Migration]:
    root = migrations_dir or default_migrations_dir()
    migrations: list[Migration] = []
    for path in sorted(root.glob("*.sql")):
        version, _, name = path.stem.partition("_")
        if not version.isdigit() or not name:
            raise ValueError(f"migration filename must start with a numeric version: {path.name}")
        migrations.append(Migration(version=version, name=name, path=path))
    return migrations


def ensure_migration_table(conn: Connection) -> None:
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {MIGRATION_SCHEMA};")
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {MIGRATION_SCHEMA}.{MIGRATION_TABLE} (
            version text PRIMARY KEY,
            name text NOT NULL,
            applied_at timestamptz NOT NULL DEFAULT now()
        );
        """
    )


def applied_versions(conn: Connection) -> set[str]:
    result = conn.execute(
        f"SELECT version FROM {MIGRATION_SCHEMA}.{MIGRATION_TABLE} ORDER BY version;"
    )
    return {row[0] for row in result}  # type: ignore[union-attr]


def apply_migrations(conn: Connection, migrations_dir: Path | None = None) -> list[Migration]:
    ensure_migration_table(conn)
    applied = applied_versions(conn)
    applied_now: list[Migration] = []

    for migration in discover_migrations(migrations_dir):
        if migration.version in applied:
            continue
        sql = migration.path.read_text(encoding="utf-8")
        conn.execute(sql)
        conn.execute(
            f"""
            INSERT INTO {MIGRATION_SCHEMA}.{MIGRATION_TABLE} (version, name)
            VALUES (%s, %s);
            """,
            (migration.version, migration.name),
        )
        applied_now.append(migration)

    conn.commit()
    return applied_now


def seed_sample_data(conn: Connection) -> None:
    statements = [
        (
            """
            INSERT INTO makai_level_01.users (user_id, email, display_name)
            VALUES
                ('user_ava', 'ava@makai.local', 'Ava'),
                ('user_beau', 'beau@makai.local', 'Beau'),
                ('user_cleo', 'cleo@makai.local', 'Cleo'),
                ('user_system', 'system@makai.local', 'Makai')
            ON CONFLICT (user_id) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_01.wallets (wallet_id, user_id, balance_cents)
            VALUES
                ('wallet_ava', 'user_ava', 10000),
                ('wallet_beau', 'user_beau', 7500),
                ('wallet_cleo', 'user_cleo', 12000),
                ('wallet_platform', 'user_system', 1000000)
            ON CONFLICT (wallet_id) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_02.events (
                event_id, name, venue, starts_at, total_seats
            )
            VALUES (
                'event_makai_gate', 'Makai Gate Run', 'Gatehouse Bazaar',
                now() + interval '14 days', 20
            )
            ON CONFLICT (event_id) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_02.seats (
                seat_id, event_id, section, row_label, seat_number, status
            )
            SELECT
                'gate_A' || seat_number,
                'event_makai_gate',
                'A',
                'A',
                seat_number,
                'available'
            FROM generate_series(1, 20) AS seat_number
            ON CONFLICT (seat_id) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_02.reservations (
                reservation_id, user_id, seat_id, status, expires_at
            )
            VALUES (
                'res_seed_ava_a1', 'user_ava', 'gate_A1', 'active',
                now() + interval '10 minutes'
            )
            ON CONFLICT (reservation_id) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_03.idempotency_keys (
                idempotency_key, user_id, request_hash, status,
                status_code, response_body
            )
            VALUES (
                'checkout_seed_ava_a1', 'user_ava', 'hash-gate-a1',
                'completed', 201,
                '{"checkout_id":"checkout_seed_ava_a1","status":"confirmed"}'::jsonb
            )
            ON CONFLICT (idempotency_key) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_03.checkouts (
                checkout_id, user_id, reservation_id, amount_cents, status
            )
            VALUES (
                'checkout_seed_ava_a1', 'user_ava', 'res_seed_ava_a1', 2500, 'confirmed'
            )
            ON CONFLICT (checkout_id) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_03.outbox_events (topic, payload)
            VALUES (
                'shop.confirmed',
                '{"checkout_id":"checkout_seed_ava_a1","user_id":"user_ava"}'::jsonb
            )
            ON CONFLICT DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_03.queue_messages (topic, payload)
            VALUES (
                'dispatch.scroll',
                '{"checkout_id":"checkout_seed_ava_a1","template":"key_ready"}'::jsonb
            )
            ON CONFLICT DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_04.cache_entries (
                cache_key, cache_value, expires_at
            )
            VALUES (
                'realm:event_makai_gate:gate_map',
                '{"available":19,"reserved":1}'::jsonb,
                now() + interval '5 minutes'
            )
            ON CONFLICT (cache_key) DO UPDATE
            SET cache_value = EXCLUDED.cache_value,
                expires_at = EXCLUDED.expires_at,
                updated_at = now();
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_04.shard_map (shard_key, shard_name, owner_type)
            VALUES
                ('user_ava', 'shard_a', 'user'),
                ('user_beau', 'shard_b', 'user'),
                ('event_makai_gate', 'shard_event_hot', 'event')
            ON CONFLICT (shard_key) DO UPDATE
            SET shard_name = EXCLUDED.shard_name,
                owner_type = EXCLUDED.owner_type;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_04.rate_limit_buckets (
                bucket_key, capacity, tokens, refill_per_second
            )
            VALUES ('shop:event_makai_gate', 100, 100, 25)
            ON CONFLICT (bucket_key) DO UPDATE
            SET tokens = EXCLUDED.tokens,
                updated_at = now();
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_04.bloom_filter_bits (filter_name, bit_index)
            VALUES ('known_bad_idempotency_keys', 17), ('known_bad_idempotency_keys', 42)
            ON CONFLICT DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_05.replica_events (
                aggregate_id, payload, primary_lsn, replicated_lsn, replicated_to_secondary
            )
            VALUES (
                'checkout_seed_ava_a1',
                '{"status":"confirmed","replica":"primary"}'::jsonb,
                100, 96, false
            )
            ON CONFLICT DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_05.conflict_versions (
                aggregate_id, replica_id, version_clock, payload, resolved_by
            )
            VALUES
                (
                    'gate_A1', 'replica_a', '{"replica_a":2}'::jsonb,
                    '{"status":"reserved","user_id":"user_ava"}'::jsonb, 'pending'
                ),
                (
                    'gate_A1', 'replica_b', '{"replica_b":1}'::jsonb,
                    '{"status":"available"}'::jsonb, 'pending'
                )
            ON CONFLICT (aggregate_id, replica_id) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_05.crdt_counters (
                counter_id, replica_id, increments, decrements
            )
            VALUES
                ('keys_collected', 'replica_a', 1, 0),
                ('keys_collected', 'replica_b', 0, 0)
            ON CONFLICT (counter_id, replica_id) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_06.interview_drills (
                prompt, focus_area, difficulty, status
            )
            VALUES
                (
                    'Makai Gate Run is double-claiming gate slots during retries. Design the fix.',
                    'idempotency and constraints', 4, 'ready'
                ),
                (
                    'The gate map cache stampedes when the tower horn sounds.',
                    'cache and load shaping', 5, 'ready'
                )
            ON CONFLICT (prompt) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_06.storage_compaction_runs (
                run_name, input_segments, output_segments, notes
            )
            VALUES (
                'tower-gate-map-lsm', 8, 3,
                'Compact high-churn gate-map writes before the final tower review.'
            )
            ON CONFLICT (run_name) DO NOTHING;
            """,
            None,
        ),
        (
            """
            INSERT INTO makai_level_06.consensus_commits (
                run_name, cluster_size, votes_granted, majority_required, committed
            )
            VALUES ('rescue-lock-raft', 5, 3, 3, true)
            ON CONFLICT (run_name) DO NOTHING;
            """,
            None,
        ),
    ]
    for sql, params in statements:
        conn.execute(sql, params)
    conn.commit()


def drop_lab_schemas(conn: Connection, *, include_migrations: bool = True) -> None:
    for schema in (*MAKAI_SCHEMAS, *PREVIOUS_NARRATIVE_SCHEMAS, *LEGACY_SCHEMAS):
        conn.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE;")
    if include_migrations:
        conn.execute(f"DROP SCHEMA IF EXISTS {MIGRATION_SCHEMA} CASCADE;")
    conn.commit()


def _fetch_scalar(result: object, default: int | str | None = None) -> int | str | None:
    row = result.fetchone() if hasattr(result, "fetchone") else None
    if row is None:
        return default
    return row[0]


def workload(conn: Connection, iterations: int = 25, sleep_seconds: float = 0.0) -> None:
    users = ("user_ava", "user_beau", "user_cleo")
    wallets = {
        "user_ava": "wallet_ava",
        "user_beau": "wallet_beau",
        "user_cleo": "wallet_cleo",
    }
    seats = tuple(f"gate_A{number}" for number in range(1, 21))

    for user_id, wallet_id in wallets.items():
        funding_cents = 500
        debit_result = conn.execute(
            """
            UPDATE makai_level_01.wallets
            SET balance_cents = balance_cents - %s,
                updated_at = now()
            WHERE wallet_id = 'wallet_platform' AND balance_cents >= %s;
            """,
            (funding_cents, funding_cents),
        )
        if getattr(debit_result, "rowcount", 1) != 1:
            continue
        conn.execute(
            """
            UPDATE makai_level_01.wallets
            SET balance_cents = balance_cents + %s,
                updated_at = now()
            WHERE wallet_id = %s;
            """,
            (funding_cents, wallet_id),
        )
        transfer_result = conn.execute(
            """
            INSERT INTO makai_level_01.wallet_transfers (
                from_wallet_id, to_wallet_id, amount_cents, reason, status
            )
            VALUES ('wallet_platform', %s, %s, 'wallet_funding', 'completed')
            RETURNING transfer_id;
            """,
            (wallet_id, funding_cents),
        )
        transfer_id = _fetch_scalar(transfer_result, 0)
        conn.execute(
            """
            INSERT INTO makai_level_01.ledger_entries (
                transfer_id, wallet_id, direction, amount_cents
            )
            VALUES
                (%s, 'wallet_platform', 'debit', %s),
                (%s, %s, 'credit', %s);
            """,
            (transfer_id, funding_cents, transfer_id, wallet_id, funding_cents),
        )

    for index in range(iterations):
        user_id = random.choice(users)
        wallet_id = wallets[user_id]
        seat_id = seats[index % len(seats)]
        reservation_id = f"res_workload_{index}_{user_id}_{seat_id}"
        checkout_id = f"checkout_workload_{index}_{user_id}_{seat_id}"
        idempotency_key = f"idem_gate_retry_{index // 3}_{user_id}"
        amount_cents = random.randint(1200, 4500)

        idem_result = conn.execute(
            """
            INSERT INTO makai_level_03.idempotency_keys (
                idempotency_key, user_id, request_hash, status, locked_until
            )
            VALUES (%s, %s, %s, 'in_progress', now() + interval '30 seconds')
            ON CONFLICT (idempotency_key) DO NOTHING;
            """,
            (idempotency_key, user_id, f"{user_id}:{seat_id}:{amount_cents}"),
        )
        if getattr(idem_result, "rowcount", 1) != 1:
            conn.execute(
                """
                UPDATE makai_level_03.queue_messages
                SET delivery_count = delivery_count + 1,
                    visible_at = now() + interval '5 seconds'
                WHERE acked_at IS NULL;
                """
            )
            conn.execute(
                """
                INSERT INTO makai_level_05.incident_notes (incident_key, note)
                VALUES (%s, %s);
                """,
                (
                    "shop-retry",
                    f"Duplicate gate-run retry safely replayed for {idempotency_key}.",
                ),
            )
            continue

        conn.execute(
            """
            INSERT INTO makai_level_02.reservations (
                reservation_id, user_id, seat_id, status, expires_at
            )
            VALUES (%s, %s, %s, 'active', now() + interval '10 minutes')
            ON CONFLICT DO NOTHING;
            """,
            (reservation_id, user_id, seat_id),
        )

        debit_result = conn.execute(
            """
            UPDATE makai_level_01.wallets
            SET balance_cents = balance_cents - %s,
                updated_at = now()
            WHERE wallet_id = %s AND balance_cents >= %s;
            """,
            (amount_cents, wallet_id, amount_cents),
        )
        if getattr(debit_result, "rowcount", 1) != 1:
            conn.execute(
                """
                UPDATE makai_level_03.idempotency_keys
                SET status = 'failed',
                    status_code = 402,
                    response_body = '{"error":"insufficient_funds"}'::jsonb,
                    locked_until = NULL,
                    updated_at = now()
                WHERE idempotency_key = %s;
                """,
                (idempotency_key,),
            )
            continue

        conn.execute(
            """
            UPDATE makai_level_01.wallets
            SET balance_cents = balance_cents + %s,
                updated_at = now()
            WHERE wallet_id = 'wallet_platform';
            """,
            (amount_cents,),
        )
        transfer_result = conn.execute(
            """
            INSERT INTO makai_level_01.wallet_transfers (
                from_wallet_id, to_wallet_id, amount_cents, reason, status
            )
            VALUES (%s, 'wallet_platform', %s, 'shop_upgrade', 'completed')
            RETURNING transfer_id;
            """,
            (wallet_id, amount_cents),
        )
        transfer_id = _fetch_scalar(transfer_result, 0)
        conn.execute(
            """
            INSERT INTO makai_level_01.ledger_entries (
                transfer_id, wallet_id, direction, amount_cents
            )
            VALUES
                (%s, %s, 'debit', %s),
                (%s, 'wallet_platform', 'credit', %s);
            """,
            (transfer_id, wallet_id, amount_cents, transfer_id, amount_cents),
        )
        conn.execute(
            """
            INSERT INTO makai_level_03.checkouts (
                checkout_id, user_id, reservation_id, amount_cents, status
            )
            VALUES (%s, %s, %s, %s, 'confirmed')
            ON CONFLICT (checkout_id) DO NOTHING;
            """,
            (checkout_id, user_id, reservation_id, amount_cents),
        )
        conn.execute(
            """
            UPDATE makai_level_03.idempotency_keys
            SET status = 'completed',
                status_code = 201,
                response_body = jsonb_build_object(
                    'checkout_id', %s::text,
                    'status', 'confirmed'
                ),
                locked_until = NULL,
                updated_at = now()
            WHERE idempotency_key = %s;
            """,
            (checkout_id, idempotency_key),
        )
        event_result = conn.execute(
            """
            INSERT INTO makai_level_03.outbox_events (topic, payload)
            VALUES (
                'shop.confirmed',
                jsonb_build_object(
                    'checkout_id', %s::text,
                    'user_id', %s::text,
                    'gate_id', %s::text,
                    'amount_cents', %s::integer
                )
            )
            RETURNING event_id;
            """,
            (checkout_id, user_id, seat_id, amount_cents),
        )
        outbox_event_id = _fetch_scalar(event_result, 0)
        conn.execute(
            """
            INSERT INTO makai_level_03.queue_messages (
                outbox_event_id, topic, payload, visible_at
            )
            VALUES (
                %s, 'dispatch.key_ready',
                jsonb_build_object('checkout_id', %s::text, 'user_id', %s::text),
                now()
            );
            """,
            (outbox_event_id, checkout_id, user_id),
        )
        conn.execute(
            """
            INSERT INTO makai_level_04.cache_entries (
                cache_key, cache_value, expires_at
            )
            VALUES (
                'realm:event_makai_gate:gate_map',
                jsonb_build_object('last_checkout', %s::text, 'hot_gate', %s::text),
                now() + interval '30 seconds'
            )
            ON CONFLICT (cache_key) DO UPDATE
            SET cache_value = EXCLUDED.cache_value,
                expires_at = EXCLUDED.expires_at,
                updated_at = now();
            """,
            (checkout_id, seat_id),
        )
        conn.execute(
            """
            INSERT INTO makai_level_04.shard_map (shard_key, shard_name, owner_type)
            VALUES (%s, %s, 'shop')
            ON CONFLICT (shard_key) DO UPDATE
            SET shard_name = EXCLUDED.shard_name,
                owner_type = EXCLUDED.owner_type;
            """,
            (checkout_id, f"shop_shard_{index % 4}"),
        )
        conn.execute(
            """
            UPDATE makai_level_04.rate_limit_buckets
            SET tokens = GREATEST(tokens - 1, 0),
                updated_at = now()
            WHERE bucket_key = 'shop:event_makai_gate';
            """
        )
        conn.execute(
            """
            INSERT INTO makai_level_05.replica_events (
                aggregate_id, payload, primary_lsn, replicated_lsn, replicated_to_secondary
            )
            VALUES (
                %s,
                jsonb_build_object('checkout_id', %s::text, 'gate_id', %s::text),
                %s,
                %s,
                %s
            );
            """,
            (
                checkout_id,
                checkout_id,
                seat_id,
                1000 + index,
                1000 + index - random.randint(0, 3),
                index % 2 == 0,
            ),
        )
        if index % 5 == 0:
            conn.execute(
                """
                INSERT INTO makai_level_05.conflict_versions (
                    aggregate_id, replica_id, version_clock, payload, resolved_by
                )
                VALUES (
                    %s, %s,
                    jsonb_build_object(%s::text, %s::integer),
                    jsonb_build_object('status', 'reserved', 'user_id', %s::text),
                    'manual-review'
                )
                ON CONFLICT (aggregate_id, replica_id) DO UPDATE
                SET version_clock = EXCLUDED.version_clock,
                    payload = EXCLUDED.payload,
                    resolved_by = EXCLUDED.resolved_by,
                    updated_at = now();
                """,
                (
                    seat_id,
                    f"replica_{index % 3}",
                    f"replica_{index % 3}",
                    index,
                    user_id,
                ),
            )

        if sleep_seconds:
            time.sleep(sleep_seconds)

    conn.commit()


def migration_status(conn: Connection, migrations_dir: Path | None = None) -> list[tuple[Migration, bool]]:
    ensure_migration_table(conn)
    applied = applied_versions(conn)
    return [(migration, migration.version in applied) for migration in discover_migrations(migrations_dir)]


def connect(dsn: str):
    return psycopg.connect(dsn)


def dsn_from_env_or_arg(value: str | None) -> str:
    return value or os.environ.get("DATABASE_URL") or DEFAULT_DSN


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage local Postgres schemas for Makai labs.")
    parser.add_argument("--dsn", help=f"Postgres DSN. Defaults to DATABASE_URL or {DEFAULT_DSN}.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("migrate", help="Apply all unapplied SQL migrations.")
    subparsers.add_parser("seed", help="Insert deterministic Makai sample data.")
    subparsers.add_parser("status", help="Show migration status.")
    subparsers.add_parser("reset", help="Drop Makai and legacy lab schemas plus metadata.")

    workload_parser = subparsers.add_parser("workload", help="Run the Makai Gate Run workload.")
    workload_parser.add_argument("--iterations", type=int, default=25)
    workload_parser.add_argument("--sleep-seconds", type=float, default=0.0)
    return parser


def print_status(rows: Iterable[tuple[Migration, bool]]) -> None:
    for migration, is_applied in rows:
        marker = "applied" if is_applied else "pending"
        print(f"{migration.version} {migration.name}: {marker}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    dsn = dsn_from_env_or_arg(args.dsn)

    with connect(dsn) as conn:
        if args.command == "migrate":
            applied = apply_migrations(conn)
            print(f"Applied {len(applied)} migration(s).")
        elif args.command == "seed":
            seed_sample_data(conn)
            print("Seeded Makai data.")
        elif args.command == "reset":
            drop_lab_schemas(conn)
            print("Dropped Makai lab schemas.")
        elif args.command == "workload":
            workload(conn, iterations=args.iterations, sleep_seconds=args.sleep_seconds)
            print(f"Ran {args.iterations} Makai workload iteration(s).")
        elif args.command == "status":
            print_status(migration_status(conn))
        else:
            raise AssertionError(f"unknown command: {args.command}")
    return 0
