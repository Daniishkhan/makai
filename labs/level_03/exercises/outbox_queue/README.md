# Outbox Queue

Scenario: The shop confirms a key upgrade, then crashes before the dispatch scroll leaves, or the scroll leaves before the checkout commits. The changed state is checkout plus outbox and queue rows, and the promise is that dispatches describe committed truth.

Prove it with the tests: write the outbox with business state, publish later, and make the consumer safe under duplicate delivery.

Run:

```bash
uv run python -m pytest labs/level_03/tests/test_outbox.py labs/level_03/tests/test_message_queue.py
```

Write through the committed shop checkout, outbox row, queue delivery, duplicate delivery evidence, and consumer dedupe requirement.
