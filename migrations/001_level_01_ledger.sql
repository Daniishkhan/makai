CREATE SCHEMA IF NOT EXISTS makai_level_01;

CREATE TABLE IF NOT EXISTS makai_level_01.users (
    user_id text PRIMARY KEY,
    email text NOT NULL UNIQUE,
    display_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS makai_level_01.wallets (
    wallet_id text PRIMARY KEY,
    user_id text NOT NULL REFERENCES makai_level_01.users(user_id),
    balance_cents bigint NOT NULL CHECK (balance_cents >= 0),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS makai_level_01.wallet_transfers (
    transfer_id bigserial PRIMARY KEY,
    from_wallet_id text NOT NULL REFERENCES makai_level_01.wallets(wallet_id),
    to_wallet_id text NOT NULL REFERENCES makai_level_01.wallets(wallet_id),
    amount_cents bigint NOT NULL CHECK (amount_cents > 0),
    reason text NOT NULL,
    status text NOT NULL CHECK (status IN ('pending', 'completed', 'failed')),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS makai_level_01.ledger_entries (
    entry_id bigserial PRIMARY KEY,
    transfer_id bigint NOT NULL REFERENCES makai_level_01.wallet_transfers(transfer_id),
    wallet_id text NOT NULL REFERENCES makai_level_01.wallets(wallet_id),
    direction text NOT NULL CHECK (direction IN ('debit', 'credit')),
    amount_cents bigint NOT NULL CHECK (amount_cents > 0),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_makai_level_01_ledger_wallet
    ON makai_level_01.ledger_entries (wallet_id, created_at);

