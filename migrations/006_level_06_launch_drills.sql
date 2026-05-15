CREATE SCHEMA IF NOT EXISTS makai_level_06;

CREATE TABLE IF NOT EXISTS makai_level_06.interview_drills (
    drill_id bigserial PRIMARY KEY,
    prompt text NOT NULL,
    focus_area text NOT NULL,
    difficulty integer NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    status text NOT NULL CHECK (status IN ('ready', 'attempted', 'reviewed')),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (prompt)
);

CREATE TABLE IF NOT EXISTS makai_level_06.design_tradeoffs (
    tradeoff_id bigserial PRIMARY KEY,
    drill_id bigint NOT NULL REFERENCES makai_level_06.interview_drills(drill_id),
    decision text NOT NULL,
    risk text NOT NULL,
    mitigation text NOT NULL
);

CREATE TABLE IF NOT EXISTS makai_level_06.storage_compaction_runs (
    run_id bigserial PRIMARY KEY,
    run_name text NOT NULL UNIQUE,
    input_segments integer NOT NULL CHECK (input_segments >= 0),
    output_segments integer NOT NULL CHECK (output_segments >= 0),
    notes text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS makai_level_06.consensus_commits (
    run_id bigserial PRIMARY KEY,
    run_name text NOT NULL UNIQUE,
    cluster_size integer NOT NULL CHECK (cluster_size > 0),
    votes_granted integer NOT NULL CHECK (votes_granted >= 0),
    majority_required integer NOT NULL CHECK (majority_required > 0),
    committed boolean NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

