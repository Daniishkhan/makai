from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal, TypeVar


T = TypeVar("T")
State = Literal["closed", "open", "half_open"]


class CircuitOpen(Exception):
    pass


@dataclass
class CircuitBreaker:
    failure_threshold: int
    recovery_timeout: float
    state: State = "closed"
    failure_count: int = 0
    opened_at: float | None = None

    def call(self, operation: Callable[[], T], now: float) -> T:
        if self.state == "open":
            if self.opened_at is None or now - self.opened_at < self.recovery_timeout:
                raise CircuitOpen("circuit is open")
            self.state = "half_open"

        try:
            result = operation()
        except Exception:
            self.failure_count += 1
            # Mission starter bug: the breaker waits one failure too long
            # before opening under repeated dependency failures.
            if self.state == "half_open" or self.failure_count > self.failure_threshold:
                self.state = "open"
                self.opened_at = now
            raise

        self.state = "closed"
        self.failure_count = 0
        self.opened_at = None
        return result
