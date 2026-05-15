from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import sqlite3
import time
from typing import Any, Callable, Dict, Iterator, Tuple


class IdempotencyConflict(Exception):
    """The same idempotency key was reused with a different request."""


class RequestInProgress(Exception):
    """A duplicate request arrived while the first attempt is still running."""


Response = Tuple[int, Dict[str, Any]]


@dataclass(frozen=True)
class IdempotencyResult:
    status_code: int
    body: Dict[str, Any]
    replayed: bool


def fingerprint(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class IdempotencyMiddleware:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS idempotency_keys (
                key TEXT PRIMARY KEY,
                request_hash TEXT NOT NULL,
                status TEXT NOT NULL,
                status_code INTEGER,
                response_body TEXT,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )

    @contextmanager
    def transaction(self) -> Iterator[None]:
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield
        except Exception:
            self.conn.execute("ROLLBACK")
            raise
        else:
            self.conn.execute("COMMIT")

    def handle(
        self,
        key: str,
        payload: Dict[str, Any],
        handler: Callable[[], Response],
    ) -> IdempotencyResult:
        request_hash = fingerprint(payload)

        with self.transaction():
            row = self.conn.execute(
                "SELECT * FROM idempotency_keys WHERE key = ?",
                (key,),
            ).fetchone()

            if row is not None:
                if row["request_hash"] != request_hash:
                    raise IdempotencyConflict(
                        "same idempotency key used with a different request"
                    )
                if row["status"] == "completed":
                    return IdempotencyResult(
                        status_code=row["status_code"],
                        body=json.loads(row["response_body"]),
                        replayed=True,
                    )
                raise RequestInProgress("request is already in progress")

            now = time.time()
            self.conn.execute(
                """
                INSERT INTO idempotency_keys (
                    key, request_hash, status, created_at, updated_at
                )
                VALUES (?, ?, 'in_progress', ?, ?)
                """,
                (key, request_hash, now, now),
            )

        try:
            status_code, body = handler()
        except Exception:
            with self.transaction():
                self.conn.execute(
                    "DELETE FROM idempotency_keys WHERE key = ? AND status = 'in_progress'",
                    (key,),
                )
            raise

        with self.transaction():
            self.conn.execute(
                """
                UPDATE idempotency_keys
                   SET status = 'completed',
                       status_code = ?,
                       response_body = ?,
                       updated_at = ?
                 WHERE key = ?
                """,
                (status_code, json.dumps(body, sort_keys=True), time.time(), key),
            )

        return IdempotencyResult(status_code=status_code, body=body, replayed=False)

