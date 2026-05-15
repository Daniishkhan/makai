from __future__ import annotations

from dataclasses import dataclass, field


class InvalidOrder(Exception):
    pass


@dataclass
class OutboxEvent:
    id: int
    topic: str
    payload: dict[str, object]
    published: bool = False


@dataclass
class InMemoryOutboxDB:
    orders: dict[str, dict[str, object]] = field(default_factory=dict)
    outbox: list[OutboxEvent] = field(default_factory=list)
    _next_event_id: int = 1

    def create_order(self, order_id: str, amount_cents: int, *, fail_after_order: bool = False) -> None:
        if amount_cents <= 0:
            raise InvalidOrder("amount must be positive")

        # Mission starter bug: order state is written before the outbox event
        # is staged, so a crash can leave committed business state alone.
        self.orders[order_id] = {"id": order_id, "amount_cents": amount_cents}
        staged_orders = dict(self.orders)
        staged_outbox = list(self.outbox)

        if fail_after_order:
            raise RuntimeError("simulated crash before outbox event")

        staged_outbox.append(
            OutboxEvent(
                id=self._next_event_id,
                topic="order.created",
                payload={"order_id": order_id, "amount_cents": amount_cents},
            )
        )
        self._next_event_id += 1
        self.orders = staged_orders
        self.outbox = staged_outbox

    def unpublished_events(self) -> list[OutboxEvent]:
        return [event for event in self.outbox if not event.published]

    def mark_published(self, event_id: int) -> None:
        for event in self.outbox:
            if event.id == event_id:
                event.published = True
                return
        raise ValueError(f"unknown event id: {event_id}")


@dataclass
class OutboxPublisher:
    db: InMemoryOutboxDB
    published: list[OutboxEvent] = field(default_factory=list)

    def publish_pending(self) -> None:
        for event in self.db.unpublished_events():
            self.published.append(event)
            self.db.mark_published(event.id)
