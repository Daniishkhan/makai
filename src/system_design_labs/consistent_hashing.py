from __future__ import annotations

from bisect import bisect_right, insort
from dataclasses import dataclass, field
import hashlib


def stable_hash(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")


@dataclass
class ConsistentHashRing:
    replicas: int = 100
    _ring: list[tuple[int, str]] = field(default_factory=list)

    def __init__(self, nodes: list[str] | None = None, replicas: int = 100) -> None:
        self.replicas = replicas
        self._ring = []
        for node in nodes or []:
            self.add_node(node)

    def add_node(self, node: str) -> None:
        for replica in range(self.replicas):
            insort(self._ring, (stable_hash(f"{node}:{replica}"), node))

    def remove_node(self, node: str) -> None:
        self._ring = [(point, owner) for point, owner in self._ring if owner != node]

    def get_node(self, key: str) -> str:
        if not self._ring:
            raise ValueError("ring has no nodes")
        points = [point for point, _ in self._ring]
        index = bisect_right(points, stable_hash(key)) % len(self._ring)
        return self._ring[index][1]


def movement_ratio(keys: list[str], before: ConsistentHashRing, after: ConsistentHashRing) -> float:
    moved = sum(1 for key in keys if before.get_node(key) != after.get_node(key))
    return moved / len(keys)
