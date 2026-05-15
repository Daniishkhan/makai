from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Callable, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int
    base_delay: float
    factor: float = 2.0
    max_delay: float = 60.0
    jitter: str = "none"

    def delay_for(self, retry_index: int, rng: random.Random | None = None) -> float:
        delay = min(self.max_delay, self.base_delay * (self.factor ** retry_index))
        if self.jitter == "none":
            return delay
        if self.jitter == "full":
            return (rng or random).uniform(0, delay)
        raise ValueError(f"unknown jitter mode: {self.jitter}")


def retry(
    operation: Callable[[], T],
    policy: RetryPolicy,
    *,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
    sleeper: Callable[[float], None] | None = None,
    rng: random.Random | None = None,
) -> T:
    if policy.max_attempts <= 0:
        raise ValueError("max_attempts must be positive")

    attempt = 0
    while True:
        try:
            return operation()
        except retry_on:
            attempt += 1
            if attempt >= policy.max_attempts:
                raise
            if sleeper is not None:
                sleeper(policy.delay_for(attempt - 1, rng))
