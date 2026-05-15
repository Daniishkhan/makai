CREATE SCHEMA IF NOT EXISTS makai_level_05;

CREATE TABLE IF NOT EXISTS makai_level_05.replica_events (
    event_id bigserial PRIMARY KEY,
    aggregate_id text NOT NULL,
    payload jsonb NOT NULL,
    primary_lsn bigint NOT NULL,
    replicated_lsn bigint NOT NULL,
    replicated_to_secondary boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_makai_level_05_replica_lag
    ON makai_level_05.replica_events (replicated_to_secondary, created_at);

CREATE TABLE IF NOT EXISTS makai_level_05.conflict_versions (
    aggregate_id text NOT NULL,
    replica_id text NOT NULL,
    version_clock jsonb NOT NULL,
    payload jsonb NOT NULL,
    resolved_by text NOT NULL DEFAULT 'pending',
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (aggregate_id, replica_id)
);

CREATE TABLE IF NOT EXISTS makai_level_05.crdt_counters (
    counter_id text NOT NULL,
    replica_id text NOT NULL,
    increments bigint NOT NULL DEFAULT 0 CHECK (increments >= 0),
    decrements bigint NOT NULL DEFAULT 0 CHECK (decrements >= 0),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (counter_id, replica_id)
);

CREATE TABLE IF NOT EXISTS makai_level_05.incident_notes (
    note_id bigserial PRIMARY KEY,
    incident_key text NOT NULL,
    note text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

