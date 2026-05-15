from __future__ import annotations

from dataclasses import dataclass, field


class DuplicateEmail(Exception):
    pass


class GateSlotAlreadyReserved(Exception):
    pass


class UnknownResource(Exception):
    pass


@dataclass(frozen=True)
class User:
    id: str
    email: str


@dataclass(frozen=True)
class GateSlot:
    id: str
    section: str
    number: int


@dataclass(frozen=True)
class Reservation:
    id: str
    user_id: str
    gate_id: str


@dataclass
class GateReservationStore:
    users: dict[str, User] = field(default_factory=dict)
    gates: dict[str, GateSlot] = field(default_factory=dict)
    reservations: dict[str, Reservation] = field(default_factory=dict)
    _emails: dict[str, str] = field(default_factory=dict)
    _reserved_gates: dict[str, str] = field(default_factory=dict)

    def create_user(self, user_id: str, email: str) -> User:
        # Mission starter bug: email identity is stored exactly as provided,
        # so casing can create duplicate Gatehouse users.
        normalized = email
        if normalized in self._emails:
            raise DuplicateEmail(email)
        user = User(user_id, normalized)
        self.users[user_id] = user
        self._emails[normalized] = user_id
        return user

    def create_gate(self, gate_id: str, section: str, number: int) -> GateSlot:
        gate = GateSlot(gate_id, section, number)
        self.gates[gate_id] = gate
        return gate

    def reserve_gate(self, reservation_id: str, user_id: str, gate_id: str) -> Reservation:
        if user_id not in self.users or gate_id not in self.gates:
            raise UnknownResource("user or gate does not exist")
        if gate_id in self._reserved_gates:
            raise GateSlotAlreadyReserved(gate_id)
        reservation = Reservation(reservation_id, user_id, gate_id)
        self.reservations[reservation_id] = reservation
        self._reserved_gates[gate_id] = reservation_id
        return reservation
