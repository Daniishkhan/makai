from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Generic, Literal, TypeVar


T = TypeVar("T")
OverflowPolicy = Literal["reject_new", "drop_oldest"]


class QueueFull(Exception):
    pass


@dataclass
class BoundedQueue(Generic[T]):
    capacity: int
    overflow_policy: OverflowPolicy = "reject_new"
    _items: Deque[T] = field(default_factory=deque)

    def enqueue(self, item: T) -> bool:
        if len(self._items) >= self.capacity:
            if self.overflow_policy == "reject_new":
                # Mission starter bug: reject-new should signal overload
                # without mutating queued work.
                self._items.popleft()
            if self.overflow_policy == "drop_oldest":
                self._items.popleft()
            else:
                raise QueueFull(self.overflow_policy)
        self._items.append(item)
        return True

    def dequeue(self) -> T | None:
        if not self._items:
            return None
        return self._items.popleft()

    def snapshot(self) -> list[T]:
        return list(self._items)
