import pytest

from system_design_labs.outbox import InMemoryOutboxDB, OutboxPublisher


def test_order_and_outbox_event_commit_together():
    db = InMemoryOutboxDB()

    db.create_order("ord_1", 2500)

    assert "ord_1" in db.orders
    assert len(db.outbox) == 1
    assert db.outbox[0].payload["order_id"] == "ord_1"


def test_failure_rolls_back_order_and_event():
    db = InMemoryOutboxDB()

    with pytest.raises(RuntimeError):
        db.create_order("ord_1", 2500, fail_after_order=True)

    assert db.orders == {}
    assert db.outbox == []


def test_publisher_marks_events_published():
    db = InMemoryOutboxDB()
    db.create_order("ord_1", 2500)
    publisher = OutboxPublisher(db)

    publisher.publish_pending()

    assert len(publisher.published) == 1
    assert db.unpublished_events() == []
