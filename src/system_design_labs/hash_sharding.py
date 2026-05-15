from __future__ import annotations

import hashlib
from dataclasses import dataclass


def stable_hash(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")


@dataclass(frozen=True)
class ModuloSharder:
    shards: tuple[str, ...]

    def shard_for(self, key: str) -> str:
        if not self.shards:
            raise ValueError("at least one shard is required")
        return self.shards[stable_hash(key) % len(self.shards)]


def movement_ratio(keys: list[str], before: ModuloSharder, after: ModuloSharder) -> float:
    moved = sum(1 for key in keys if before.shard_for(key) != after.shard_for(key))
    return moved / len(keys)
