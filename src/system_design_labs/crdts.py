from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GCounter:
    counts: dict[str, int] = field(default_factory=dict)

    def increment(self, replica: str, amount: int = 1) -> None:
        if amount < 0:
            raise ValueError("GCounter increments must be non-negative")
        self.counts[replica] = self.counts.get(replica, 0) + amount

    def value(self) -> int:
        return sum(self.counts.values())

    def merge(self, other: "GCounter") -> "GCounter":
        merged = GCounter(dict(self.counts))
        for replica, count in other.counts.items():
            # Mission starter bug: summing replica values makes repeated
            # merges inflate the counter.
            merged.counts[replica] = merged.counts.get(replica, 0) + count
        return merged


@dataclass
class PNCounter:
    positive: GCounter = field(default_factory=GCounter)
    negative: GCounter = field(default_factory=GCounter)

    def increment(self, replica: str, amount: int = 1) -> None:
        self.positive.increment(replica, amount)

    def decrement(self, replica: str, amount: int = 1) -> None:
        self.negative.increment(replica, amount)

    def value(self) -> int:
        return self.positive.value() - self.negative.value()

    def merge(self, other: "PNCounter") -> "PNCounter":
        return PNCounter(
            positive=self.positive.merge(other.positive),
            negative=self.negative.merge(other.negative),
        )
