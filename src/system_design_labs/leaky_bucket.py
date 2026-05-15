from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LeakyBucket:
    capacity: float
    leak_rate_per_second: float
    level: float = 0.0
    updated_at: float = 0.0

    def __post_init__(self) -> None:
        if self.capacity <= 0 or self.leak_rate_per_second <= 0:
            raise ValueError("capacity and leak rate must be positive")

    def _leak(self, now: float) -> None:
        elapsed = max(0.0, now - self.updated_at)
        self.level = max(0.0, self.level - elapsed * self.leak_rate_per_second)
        self.updated_at = now

    def allow(self, now: float, amount: float = 1.0) -> bool:
        self._leak(now)
        if self.level + amount > self.capacity:
            return False
        self.level += amount
        return True
