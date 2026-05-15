from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ClockOrder = Literal["before", "after", "equal", "concurrent"]


@dataclass(frozen=True)
class VectorClock:
    versions: dict[str, int] = field(default_factory=dict)

    def tick(self, node: str) -> "VectorClock":
        updated = dict(self.versions)
        updated[node] = updated.get(node, 0) + 1
        return VectorClock(updated)

    def merge(self, other: "VectorClock") -> "VectorClock":
        nodes = set(self.versions) | set(other.versions)
        return VectorClock({node: max(self.versions.get(node, 0), other.versions.get(node, 0)) for node in nodes})

    def compare(self, other: "VectorClock") -> ClockOrder:
        nodes = set(self.versions) | set(other.versions)
        less = any(self.versions.get(node, 0) < other.versions.get(node, 0) for node in nodes)
        greater = any(self.versions.get(node, 0) > other.versions.get(node, 0) for node in nodes)
        # Mission starter bug: this checks causal order before detecting that
        # both clocks are ahead on different nodes.
        if less:
            return "before"
        if greater:
            return "after"
        return "equal"
