from __future__ import annotations

from pathlib import Path

from system_design_labs.db import runner


class FakeResult(list):
    def __init__(self, rows=None, rowcount: int = 1) -> None:
        super().__init__(rows or [])
        self.rowcount = rowcount

    def fetchone(self):
        return self[0] if self else None


class FakeConnection:
    def __init__(self, applied: set[str] | None = None) -> None:
        self.applied = applied or set()
        self.calls: list[tuple[str, object | None]] = []
        self.commits = 0

    def execute(self, query: str, params: object | None = None):
        self.calls.append((query, params))
        normalized = " ".join(query.split())
        if normalized.startswith("SELECT version FROM"):
            return FakeResult([(version,) for version in sorted(self.applied)])
        if normalized.startswith("INSERT INTO system_design_labs.schema_migrations"):
            assert isinstance(params, tuple)
            self.applied.add(params[0])
        if "ON CONFLICT (idempotency_key) DO NOTHING" in normalized:
            return FakeResult(rowcount=1)
        if "RETURNING transfer_id" in normalized:
            return FakeResult([(101,)])
        if "RETURNING event_id" in normalized:
            return FakeResult([(202,)])
        return FakeResult()

    def commit(self) -> None:
        self.commits += 1


def write_migration(path: Path, version: str, name: str, body: str) -> None:
    path.joinpath(f"{version}_{name}.sql").write_text(body, encoding="utf-8")


def test_discover_migrations_sorts_by_numeric_prefix(tmp_path):
    write_migration(tmp_path, "002", "second", "SELECT 2;")
    write_migration(tmp_path, "001", "first", "SELECT 1;")

    migrations = runner.discover_migrations(tmp_path)

    assert [migration.version for migration in migrations] == ["001", "002"]
    assert [migration.name for migration in migrations] == ["first", "second"]


def test_apply_migrations_skips_versions_already_recorded(tmp_path):
    write_migration(tmp_path, "001", "first", "SELECT 'old';")
    write_migration(tmp_path, "002", "second", "SELECT 'new';")
    conn = FakeConnection(applied={"001"})

    applied = runner.apply_migrations(conn, tmp_path)

    assert [migration.version for migration in applied] == ["002"]
    executed_sql = "\n".join(query for query, _ in conn.calls)
    assert "SELECT 'old';" not in executed_sql
    assert "SELECT 'new';" in executed_sql
    assert conn.applied == {"001", "002"}
    assert conn.commits == 1


def test_drop_lab_schemas_targets_makai_legacy_and_metadata_schemas():
    conn = FakeConnection()

    runner.drop_lab_schemas(conn)

    executed = [query.strip() for query, _ in conn.calls]
    assert executed[:6] == [
        f"DROP SCHEMA IF EXISTS makai_level_{level:02d} CASCADE;"
        for level in range(1, 7)
    ]
    previous_start = 6
    previous_end = previous_start + len(runner.PREVIOUS_NARRATIVE_SCHEMAS)
    legacy_end = previous_end + len(runner.LEGACY_SCHEMAS)
    assert executed[previous_start:previous_end] == [
        f"DROP SCHEMA IF EXISTS {schema} CASCADE;"
        for schema in runner.PREVIOUS_NARRATIVE_SCHEMAS
    ]
    assert executed[previous_end:legacy_end] == [
        f"DROP SCHEMA IF EXISTS {schema} CASCADE;"
        for schema in runner.LEGACY_SCHEMAS
    ]
    assert executed[legacy_end] == "DROP SCHEMA IF EXISTS system_design_labs CASCADE;"
    assert conn.commits == 1


def test_seed_sample_data_writes_across_all_makai_levels():
    conn = FakeConnection()

    runner.seed_sample_data(conn)

    executed_sql = "\n".join(query for query, _ in conn.calls)
    for level in range(1, 7):
        assert f"makai_level_{level:02d}" in executed_sql
    assert conn.commits == 1


def test_workload_records_transfer_outbox_cache_and_replica_activity():
    conn = FakeConnection()

    runner.workload(conn, iterations=3)

    executed_sql = "\n".join(query for query, _ in conn.calls)
    assert executed_sql.count("UPDATE makai_level_01.wallets") >= 6
    assert executed_sql.count("INSERT INTO makai_level_03.outbox_events") == 3
    assert executed_sql.count("INSERT INTO makai_level_03.queue_messages") == 3
    assert executed_sql.count("INSERT INTO makai_level_04.cache_entries") == 3
    assert executed_sql.count("INSERT INTO makai_level_05.replica_events") == 3
    assert conn.commits == 1
