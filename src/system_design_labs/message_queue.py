from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Message:
    id: int
    body: str
    visible_at: float = 0.0
    acked: bool = False


@dataclass
class AtLeastOnceQueue:
    visibility_timeout: float
    _messages: list[Message] = field(default_factory=list)
    _next_id: int = 1

    def send(self, body: str) -> int:
        message_id = self._next_id
        self._next_id += 1
        self._messages.append(Message(id=message_id, body=body))
        return message_id

    def receive(self, now: float) -> Message | None:
        for message in self._messages:
            if not message.acked and message.visible_at <= now:
                message.visible_at = now + self.visibility_timeout
                return message
        return None

    def ack(self, message_id: int) -> None:
        for message in self._messages:
            if message.id == message_id:
                message.acked = True
                return
        raise ValueError(f"unknown message id: {message_id}")


@dataclass
class DeduplicatingConsumer:
    seen: set[int] = field(default_factory=set)

    def handle(self, message: Message) -> bool:
        if message.id in self.seen:
            return False
        self.seen.add(message.id)
        return True
