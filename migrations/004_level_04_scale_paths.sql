CREATE SCHEMA IF NOT EXISTS makai_level_04;

CREATE TABLE IF NOT EXISTS makai_level_04.cache_entries (
    cache_key text PRIMARY KEY,
    cache_value jsonb NOT NULL,
    expires_at timestamptz NOT NULL,
    herd_lock_until timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_makai_level_04_cache_expiry
    ON makai_level_04.cache_entries (expires_at);

CREATE TABLE IF NOT EXISTS makai_level_04.shard_map (
    shard_key text PRIMARY KEY,
    shard_name text NOT NULL,
    owner_type text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS makai_level_04.rate_limit_buckets (
    bucket_key text PRIMARY KEY,
    capacity integer NOT NULL CHECK (capacity > 0),
    tokens integer NOT NULL CHECK (tokens >= 0),
    refill_per_second integer NOT NULL CHECK (refill_per_second > 0),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS makai_level_04.bloom_filter_bits (
    filter_name text NOT NULL,
    bit_index integer NOT NULL CHECK (bit_index >= 0),
    set_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (filter_name, bit_index)
);

