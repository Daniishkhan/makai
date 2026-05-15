from system_design_labs.message_queue import AtLeastOnceQueue, DeduplicatingConsumer


def test_unacked_message_is_redelivered_after_visibility_timeout():
    queue = AtLeastOnceQueue(visibility_timeout=5)
    queue.send("send-email")

    first = queue.receive(now=0)
    assert first is not None
    assert queue.receive(now=1) is None

    second = queue.receive(now=6)
    assert second is not None
    assert second.id == first.id


def test_ack_prevents_redelivery():
    queue = AtLeastOnceQueue(visibility_timeout=5)
    message_id = queue.send("send-email")
    message = queue.receive(now=0)
    assert message is not None
    queue.ack(message_id)

    assert queue.receive(now=6) is None


def test_consumer_deduplicates_redelivered_message():
    queue = AtLeastOnceQueue(visibility_timeout=5)
    consumer = DeduplicatingConsumer()
    queue.send("send-email")

    assert consumer.handle(queue.receive(now=0))
    assert not consumer.handle(queue.receive(now=6))
