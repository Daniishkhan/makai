from __future__ import annotations

from dataclasses import dataclass, field
from threading import Event, Lock
from typing import Callable, TypeVar


T = TypeVar("T")


@dataclass
class _Flight:
    event: Event = field(default_factory=Event)
    result: object = None
    error: BaseException | None = None


class RequestCoalescer:
    def __init__(self) -> None:
        self._lock = Lock()
        self._flights: dict[str, _Flight] = {}

    def get(self, key: str, loader: Callable[[], T]) -> T:
        with self._lock:
            flight = self._flights.get(key)
            if flight is None:
                flight = _Flight()
                self._flights[key] = flight
                owner = True
            else:
                owner = False

        if owner:
            try:
                flight.result = loader()
            except BaseException as exc:
                flight.error = exc
            finally:
                with self._lock:
                    self._flights.pop(key, None)
                flight.event.set()
        else:
            flight.event.wait()

        if flight.error is not None:
            raise flight.error
        return flight.result  # type: ignore[return-value]
