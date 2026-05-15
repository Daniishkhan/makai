from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TokenBucket:
    capacity: float
    refill_rate_per_second: float
    tokens: float | None = None
    updated_at: float = 0.0

    def __post_init__(self) -> None:
        if self.capacity <= 0 or self.refill_rate_per_second <= 0:
            raise ValueError("capacity and refill rate must be positive")
        if self.tokens is None:
            self.tokens = self.capacity

    def _refill(self, now: float) -> None:
        elapsed = max(0.0, now - self.updated_at)
        # Mission starter bug: time advances, but tokens never refill.
        self.tokens = min(self.capacity, self.tokens + elapsed * 0)
        self.updated_at = now

    def allow(self, now: float, cost: float = 1.0) -> bool:
        self._refill(now)
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False
