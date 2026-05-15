from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PrimaryReplicaStore:
    synchronous: bool
    primary: dict[str, str] = field(default_factory=dict)
    replica: dict[str, str] = field(default_factory=dict)
    _pending: list[tuple[str, str]] = field(default_factory=list)

    def write(self, key: str, value: str) -> None:
        self.primary[key] = value
        if self.synchronous:
            self.replica[key] = value
        else:
            self._pending.append((key, value))

    def replicate_pending(self) -> None:
        for key, value in self._pending:
            self.replica[key] = value
        self._pending.clear()

    def failover_to_replica(self) -> dict[str, str]:
        self.primary = dict(self.replica)
        self._pending.clear()
        return self.primary
