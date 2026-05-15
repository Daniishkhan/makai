# Agent Guide

## Repo Purpose

Makai System Design Labs is a reading-first senior engineering practice repo. The goal is to help learners read unfamiliar working code, trace state transitions, draw useful diagrams, diagnose failures, repair implementation bugs, and explain system-design trade-offs. Do not treat this as a fill-in-the-blank kata unless the user explicitly asks for that mode.

`main` is the green reference implementation. Mission branches such as `mission/level-01-ledger-transfer` are allowed to be intentionally red so learners can practice the natural engineering loop: read the incident, reproduce the failure, inspect code, explore the concept, patch the implementation, verify, write a report, and commit.

For levels without a mission branch, treat a green test as a completed incident file, not as proof that there is nothing to diagnose. The learner should read the passing assertions, find the unsafe path, pressure case, or trade-off in the implementation, then explain why the reference mechanism protects the promise.

## Default Workflow

When helping in this repo:

1. Start by reading the relevant level README, exercise `MISSION.md`, tests, and implementation.
2. If the exercise has a `MISSION.md`, follow that mission workflow and expect the starter branch to fail before the fix.
3. Use tests and Postgres workload rows as evidence, not just pass/fail signals.
4. When a test includes both unsafe and safe behavior, explicitly contrast the risky implementation path with the reference path.
5. Prefer explanations that name the player/operator promise, changed state, invariant, evidence, mechanism, and remaining risk.
6. Encourage small diagrams for data flow, state transitions, contention windows, queue paths, replica paths, or consensus paths.
7. On mission branches, finish with the targeted tests, `REPORT.md`, and a meaningful commit.

## Important Paths

- `README.md`: learning contract, progression map, and root definition of done.
- `GLOSSARY.md`: project-local vocabulary and Makai promises.
- `labs/level_01` through `labs/level_06`: level workbooks, exercise prompts, and tests.
- `labs/**/exercises/**/MISSION.md`: mission-branch repair workflow for each exercise.
- `src/system_design_labs`: runnable reference implementations of system primitives.
- `src/system_design_labs/makai`: Makai-facing helpers for ledger, checkout, workload, and Postgres access.
- `migrations`: six Postgres schemas used by `sdl-db`.

## Commands

Run all tests:

```bash
uv run python -m pytest
```

Run one level:

```bash
uv run python -m pytest labs/level_03/tests
```

Run the local Postgres flow:

```bash
createdb system_design_labs || true
uv run sdl-db reset
uv run sdl-db migrate
uv run sdl-db seed
uv run sdl-db workload --iterations 50
uv run sdl-db status
```

## Change Guidelines

- Preserve the reading-first contract unless the user explicitly changes the repo's direction.
- Keep narrative details tied to concrete system behavior; avoid lore that does not clarify an invariant, failure mode, or trade-off.
- Keep exercise commands, schema names, and test paths stable unless a change is intentional and verified.
- Do not commit editor state, caches, local database metadata, or virtualenv files.
- For docs-only changes, run at least the relevant `rg` checks and preferably the full test suite if quick.
- For code or migration changes, run the affected tests and the full suite when feasible.
