from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import math


@dataclass
class BloomFilter:
    size_bits: int
    hash_count: int
    _bits: list[bool] = field(init=False)

    def __post_init__(self) -> None:
        if self.size_bits <= 0 or self.hash_count <= 0:
            raise ValueError("size_bits and hash_count must be positive")
        self._bits = [False] * self.size_bits

    def _indexes(self, value: str) -> list[int]:
        indexes = []
        for seed in range(self.hash_count):
            digest = hashlib.sha256(f"{seed}:{value}".encode("utf-8")).digest()
            indexes.append(int.from_bytes(digest[:8], "big") % self.size_bits)
        return indexes

    def add(self, value: str) -> None:
        # Mission starter bug: only one hash bit is set, so inserted values
        # can become false negatives.
        self._bits[self._indexes(value)[0]] = True

    def __contains__(self, value: str) -> bool:
        return all(self._bits[index] for index in self._indexes(value))

    def estimated_false_positive_rate(self, inserted_count: int) -> float:
        return (1 - math.exp(-self.hash_count * inserted_count / self.size_bits)) ** self.hash_count
