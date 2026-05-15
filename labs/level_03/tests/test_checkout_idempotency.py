import pytest

from system_design_labs.makai.checkout import (
    IdempotencyConflict,
    IdempotencyMiddleware,
    RequestInProgress,
    fingerprint,
)


def test_duplicate_request_replays_cached_response():
    middleware = IdempotencyMiddleware()
    calls = []
    payload = {"amount_cents": 2599, "currency": "USD"}

    def create_payment():
        calls.append("called")
        return 201, {"payment_id": "pay_123", "status": "created"}

    first = middleware.handle("key-1", payload, create_payment)
    second = middleware.handle("key-1", payload, create_payment)

    assert first.status_code == 201
    assert first.replayed is False
    assert second.status_code == 201
    assert second.replayed is True
    assert second.body == {"payment_id": "pay_123", "status": "created"}
    assert calls == ["called"]


def test_same_key_with_different_payload_is_rejected():
    middleware = IdempotencyMiddleware()

    middleware.handle(
        "key-1",
        {"amount_cents": 1000},
        lambda: (201, {"payment_id": "pay_123"}),
    )

    with pytest.raises(IdempotencyConflict):
        middleware.handle(
            "key-1",
            {"amount_cents": 2000},
            lambda: (201, {"payment_id": "pay_456"}),
        )


def test_failed_handler_allows_retry():
    middleware = IdempotencyMiddleware()
    calls = []

    def fails_once():
        calls.append("failed")
        raise RuntimeError("provider timeout")

    with pytest.raises(RuntimeError):
        middleware.handle("key-1", {"amount_cents": 1000}, fails_once)

    result = middleware.handle(
        "key-1",
        {"amount_cents": 1000},
        lambda: (201, {"payment_id": "pay_123"}),
    )

    assert result.status_code == 201
    assert result.replayed is False
    assert calls == ["failed"]


def test_in_progress_request_blocks_duplicate():
    middleware = IdempotencyMiddleware()
    payload = {"amount_cents": 1000}
    request_hash = fingerprint(payload)

    middleware.conn.execute(
        """
        INSERT INTO idempotency_keys (
            key, request_hash, status, created_at, updated_at
        )
        VALUES (?, ?, 'in_progress', 0, 0)
        """,
        ("key-1", request_hash),
    )

    with pytest.raises(RequestInProgress):
        middleware.handle(
            "key-1",
            payload,
            lambda: (201, {"payment_id": "pay_123"}),
        )
