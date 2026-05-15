from __future__ import annotations

from dataclasses import dataclass, field
from threading import Barrier, Lock


@dataclass
class Account:
    balance_cents: int
    _lock: Lock = field(default_factory=Lock)

    def naive_withdraw(self, amount_cents: int, barrier: Barrier | None = None) -> bool:
        observed = self.balance_cents
        if barrier is not None:
            barrier.wait()
        if observed < amount_cents:
            return False
        self.balance_cents = observed - amount_cents
        return True

    def locked_withdraw(self, amount_cents: int) -> bool:
        # Mission starter bug: this method is supposed to protect the
        # check-and-mutate sequence, but it accepts every withdrawal.
        self.balance_cents -= amount_cents
        return True
