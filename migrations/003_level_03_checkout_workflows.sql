CREATE SCHEMA IF NOT EXISTS makai_level_03;

CREATE TABLE IF NOT EXISTS makai_level_03.checkouts (
    checkout_id text PRIMARY KEY,
    user_id text NOT NULL REFERENCES makai_level_01.users(user_id),
    reservation_id text NOT NULL,
    amount_cents bigint NOT NULL CHECK (amount_cents > 0),
    status text NOT NULL CHECK (status IN ('started', 'confirmed', 'failed', 'cancelled')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS makai_level_03.idempotency_keys (
    idempotency_key text PRIMARY KEY,
    user_id text NOT NULL REFERENCES makai_level_01.users(user_id),
    request_hash text NOT NULL,
    status text NOT NULL CHECK (status IN ('in_progress', 'completed', 'failed')),
    status_code integer,
    response_body jsonb,
    locked_until timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_makai_level_03_idempotency_locked_until
    ON makai_level_03.idempotency_keys (locked_until);

CREATE TABLE IF NOT EXISTS makai_level_03.outbox_events (
    event_id bigserial PRIMARY KEY,
    topic text NOT NULL,
    payload jsonb NOT NULL,
    status text NOT NULL CHECK (status IN ('pending', 'published', 'failed')) DEFAULT 'pending',
    attempts integer NOT NULL DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now(),
    published_at timestamptz
);

CREATE INDEX IF NOT EXISTS idx_makai_level_03_outbox_pending
    ON makai_level_03.outbox_events (status, created_at);

CREATE TABLE IF NOT EXISTS makai_level_03.queue_messages (
    message_id bigserial PRIMARY KEY,
    outbox_event_id bigint REFERENCES makai_level_03.outbox_events(event_id),
    topic text NOT NULL,
    payload jsonb NOT NULL,
    visible_at timestamptz NOT NULL DEFAULT now(),
    delivery_count integer NOT NULL DEFAULT 0,
    acked_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_makai_level_03_queue_visible
    ON makai_level_03.queue_messages (visible_at)
    WHERE acked_at IS NULL;

