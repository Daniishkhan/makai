import pytest

from system_design_labs.api_resource_modeling import (
    DuplicateEmail,
    GateReservationStore,
    GateSlotAlreadyReserved,
)


def test_reservation_links_user_and_gate():
    store = GateReservationStore()
    store.create_user("usr_1", "ALICE@example.com")
    store.create_gate("gate_A1", "A", 1)

    reservation = store.reserve_gate("res_1", "usr_1", "gate_A1")

    assert reservation.user_id == "usr_1"
    assert reservation.gate_id == "gate_A1"


def test_unique_email_constraint_is_enforced():
    store = GateReservationStore()
    store.create_user("usr_1", "alice@example.com")

    with pytest.raises(DuplicateEmail):
        store.create_user("usr_2", "ALICE@example.com")


def test_gate_cannot_be_reserved_twice():
    store = GateReservationStore()
    store.create_user("usr_1", "alice@example.com")
    store.create_user("usr_2", "bob@example.com")
    store.create_gate("gate_A1", "A", 1)
    store.reserve_gate("res_1", "usr_1", "gate_A1")

    with pytest.raises(GateSlotAlreadyReserved):
        store.reserve_gate("res_2", "usr_2", "gate_A1")
