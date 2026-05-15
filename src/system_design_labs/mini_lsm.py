from __future__ import annotations

from dataclasses import dataclass, field


TOMBSTONE = object()


@dataclass
class MiniLSM:
    flush_threshold: int
    memtable: dict[str, object] = field(default_factory=dict)
    sstables: list[dict[str, object]] = field(default_factory=list)

    def put(self, key: str, value: str) -> None:
        self.memtable[key] = value
        if len(self.memtable) >= self.flush_threshold:
            self.flush()

    def delete(self, key: str) -> None:
        self.memtable[key] = TOMBSTONE
        if len(self.memtable) >= self.flush_threshold:
            self.flush()

    def get(self, key: str) -> str | None:
        if key in self.memtable:
            value = self.memtable[key]
            return None if value is TOMBSTONE else value  # type: ignore[return-value]
        for table in self.sstables:
            if key in table:
                value = table[key]
                return None if value is TOMBSTONE else value  # type: ignore[return-value]
        return None

    def flush(self) -> None:
        if self.memtable:
            self.sstables.insert(0, dict(self.memtable))
            self.memtable.clear()

    def compact(self) -> None:
        merged: dict[str, object] = {}
        for table in self.sstables:
            for key, value in table.items():
                merged.setdefault(key, value)
        self.sstables = [{key: value for key, value in merged.items() if value is not TOMBSTONE}]
