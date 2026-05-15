from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Callable, TypeVar


T = TypeVar("T")


@dataclass
class CacheEntry:
    value: object
    expires_at: float


class CacheAside:
    def __init__(self, ttl_seconds: float) -> None:
        self.ttl_seconds = ttl_seconds
        self._entries: dict[str, CacheEntry] = {}
        self._locks: dict[str, Lock] = {}
        self._global_lock = Lock()

    def _lock_for(self, key: str) -> Lock:
        with self._global_lock:
            return self._locks.setdefault(key, Lock())

    def get(self, key: str, now: float, loader: Callable[[], T]) -> T:
        entry = self._entries.get(key)
        if entry is not None and entry.expires_at > now:
            return entry.value  # type: ignore[return-value]

        with self._lock_for(key):
            entry = self._entries.get(key)
            if entry is not None and entry.expires_at > now:
                return entry.value  # type: ignore[return-value]
            value = loader()
            self._entries[key] = CacheEntry(value=value, expires_at=now + self.ttl_seconds)
            return value
