from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Generic, TypeVar


K = TypeVar("K")
V = TypeVar("V")


@dataclass
class LRUCache(Generic[K, V]):
    capacity: int
    _items: OrderedDict[K, V] = field(default_factory=OrderedDict)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")

    def get(self, key: K) -> V | None:
        if key not in self._items:
            return None
        # Mission starter bug: reads return the value but do not refresh
        # recency, so recently used keys can be evicted.
        return self._items[key]

    def put(self, key: K, value: V) -> None:
        if key in self._items:
            self._items.pop(key)
        elif len(self._items) >= self.capacity:
            self._items.popitem(last=False)
        self._items[key] = value

    def keys_lru_to_mru(self) -> list[K]:
        return list(self._items.keys())
