from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VersionedValue:
    value: str
    timestamp: int
    node_id: str


@dataclass
class LWWRegister:
    node_id: str
    current: VersionedValue | None = None

    def write(self, value: str, timestamp: int) -> VersionedValue:
        self.current = VersionedValue(value=value, timestamp=timestamp, node_id=self.node_id)
        return self.current

    def merge(self, other: "LWWRegister") -> None:
        if other.current is None:
            return
        if self.current is None:
            self.current = other.current
            return
        # Mission starter bug: equal timestamps use local list order instead
        # of the deterministic node-id tie breaker.
        self.current = max(
            [self.current, other.current],
            key=lambda item: item.timestamp,
        )
