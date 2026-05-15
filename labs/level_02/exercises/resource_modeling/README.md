# Resource Modeling

Scenario: The Gatehouse API blurs adventurers, gate runs, passage slots, and key reservations, so a key claim can appear to mutate the wrong owner. The changed state needs a clear resource boundary, and the promise is that every transition has one authoritative home.

Read the passing test as proof: it models the resources so the API names the owner of each state change, then leaves you to explain which uniqueness rule still needs database enforcement.

Run:

```bash
uv run python -m pytest labs/level_02/tests/test_api_resource_modeling.py
```

Write through the resource boundary, the unique-gate-slot invariant, the evidence from the tests, and why API shape alone is not enough without constraints.
