CREATE SCHEMA IF NOT EXISTS makai_level_02;

CREATE TABLE IF NOT EXISTS makai_level_02.events (
    event_id text PRIMARY KEY,
    name text NOT NULL,
    venue text NOT NULL,
    starts_at timestamptz NOT NULL,
    total_seats integer NOT NULL CHECK (total_seats > 0),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS makai_level_02.seats (
    seat_id text PRIMARY KEY,
    event_id text NOT NULL REFERENCES makai_level_02.events(event_id),
    section text NOT NULL,
    row_label text NOT NULL,
    seat_number integer NOT NULL CHECK (seat_number > 0),
    status text NOT NULL CHECK (status IN ('available', 'held', 'sold')) DEFAULT 'available',
    UNIQUE (event_id, section, row_label, seat_number)
);

CREATE TABLE IF NOT EXISTS makai_level_02.reservations (
    reservation_id text PRIMARY KEY,
    user_id text NOT NULL REFERENCES makai_level_01.users(user_id),
    seat_id text NOT NULL REFERENCES makai_level_02.seats(seat_id),
    status text NOT NULL CHECK (status IN ('active', 'expired', 'confirmed', 'cancelled')),
    expires_at timestamptz NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_makai_level_02_one_active_reservation_per_seat
    ON makai_level_02.reservations (seat_id)
    WHERE status = 'active';

CREATE TABLE IF NOT EXISTS makai_level_02.reservation_attempts (
    attempt_id bigserial PRIMARY KEY,
    user_id text NOT NULL REFERENCES makai_level_01.users(user_id),
    seat_id text NOT NULL REFERENCES makai_level_02.seats(seat_id),
    outcome text NOT NULL,
    observed_at timestamptz NOT NULL DEFAULT now()
);

