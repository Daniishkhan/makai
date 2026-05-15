from system_design_labs.bounded_queue import BoundedQueue


def test_reject_new_policy_applies_backpressure():
    queue: BoundedQueue[str] = BoundedQueue(capacity=2, overflow_policy="reject_new")

    assert queue.enqueue("a")
    assert queue.enqueue("b")
    assert not queue.enqueue("c")
    assert queue.snapshot() == ["a", "b"]


def test_drop_oldest_policy_preserves_newest_work():
    queue: BoundedQueue[str] = BoundedQueue(capacity=2, overflow_policy="drop_oldest")

    queue.enqueue("a")
    queue.enqueue("b")
    queue.enqueue("c")

    assert queue.snapshot() == ["b", "c"]
