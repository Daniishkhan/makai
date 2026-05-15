# Makai Glossary

## Invariant

**Definition:** A condition that must remain true after every operation.

**Use it when:** You need to decide what the system must protect, such as total coin-pouch balance or one active key reservation per gate slot.

**Makai promise:** A player should be able to trust the realm's visible state after every move.

**Failure it prevents:** Silent state drift, double-claimed gates, money creation, and misleading retries.

**Related lab:** `labs/level_01` and `labs/level_02`

## Atomicity

**Definition:** A group of changes either all commit or all roll back.

**Use it when:** A shop checkout debits a pouch, credits the gatehouse, and writes ledger rows as one business action.

**Makai promise:** Cleo should never pay for a key unless the matching Gatehouse credit and ledger evidence exist.

**Failure it prevents:** A debit without a matching credit, or a confirmed shop upgrade without ledger evidence.

**Related lab:** `labs/level_01`

## Transaction

**Definition:** A database boundary that groups reads and writes under commit or rollback rules.

**Use it when:** Makai needs a protected write boundary around pouch transfers, gate holds, or shop confirmation.

**Makai promise:** A crash should not leave Ava between worlds, charged in one table and missing from another.

**Failure it prevents:** Partial writes after crashes and interleaved writes that violate local assumptions.

**Related lab:** `labs/level_01` and `labs/level_03`

## Isolation

**Definition:** The degree to which concurrent operations can observe or interfere with each other.

**Use it when:** Multiple adventurers reserve the same gate slot or withdraw from the same pouch at the same time.

**Makai promise:** Beau should not lose a claimed slot because another request slipped through the same decision window.

**Failure it prevents:** Lost updates, stale decisions, and double winners for one scarce resource.

**Related lab:** `labs/level_02`

## Idempotency

**Definition:** Repeating the same request produces one durable business effect.

**Use it when:** An adventurer retries a shop upgrade after a timeout and Makai must not charge twice.

**Makai promise:** Refreshing a stuck shop screen should replay the same outcome, not create a second purchase.

**Failure it prevents:** Duplicate payments, duplicate dispatches, and retry storms that mutate state repeatedly.

**Related lab:** `labs/level_03`

## Outbox

**Definition:** A table written in the same transaction as business state so async events can be published later.

**Use it when:** Shop confirmation must create both durable state and a dispatch event.

**Makai promise:** If Makai says a key is ready, the dispatch path should eventually learn about the committed checkout.

**Failure it prevents:** Confirmed orders with no downstream message, or messages about state that never committed.

**Related lab:** `labs/level_03`

## At-Least-Once Delivery

**Definition:** A queue guarantee where messages may be delivered more than once, but should not disappear before processing.

**Use it when:** Key-ready dispatches can be retried safely with consumer-side dedupe.

**Makai promise:** A dispatch scroll may arrive twice, but the tower should process its effect once.

**Failure it prevents:** Lost dispatches at the cost of handling duplicates.

**Related lab:** `labs/level_03`

## Backpressure

**Definition:** A way to slow or reject producers when downstream work cannot keep up.

**Use it when:** Gate-run traffic fills queues or shop workers saturate.

**Makai promise:** When the realm is overloaded, Makai should slow the edge before the core state collapses.

**Failure it prevents:** Memory blowups, latency collapse, and uncontrolled retry amplification.

**Related lab:** `labs/level_04`

## Cache Stampede

**Definition:** Many requests miss or expire the same cache key and all recompute it at once.

**Use it when:** The Makai Gate Run map becomes a hot key.

**Makai promise:** A viral gate map should not stampede the database just because one cache entry expired.

**Failure it prevents:** Database overload caused by synchronized cache misses.

**Related lab:** `labs/level_04`

## Consistent Hashing

**Definition:** A sharding strategy that remaps only part of the keyspace when nodes change.

**Use it when:** Makai adds shop shards without moving every adventurer or gate key.

**Makai promise:** Adding capacity should not reshuffle the whole realm while players are mid-quest.

**Failure it prevents:** Full-cache invalidation and broad data movement during scaling.

**Related lab:** `labs/level_04`

## Bloom Filter

**Definition:** A probabilistic set that can say “maybe present” or “definitely absent.”

**Use it when:** Makai wants a cheap precheck before expensive dedupe or abuse lookups.

**Makai promise:** Obviously absent or abusive keys should be filtered cheaply before they drain shared capacity.

**Failure it prevents:** Avoidable database reads, while accepting false positives.

**Related lab:** `labs/level_04`

## Replica Lag

**Definition:** The delay between a primary write and its visibility on a replica.

**Use it when:** A gatehouse page reads shop state from a mirror replica after the primary confirmed it.

**Makai promise:** A stale mirror should be treated as lag, not as proof that a committed upgrade vanished.

**Failure it prevents:** Treating a stale read as proof that a write failed.

**Related lab:** `labs/level_05`

## Vector Clock

**Definition:** A per-replica version map used to compare causality between updates.

**Use it when:** Two mirror realms update gate or shop metadata and Makai must detect concurrency.

**Makai promise:** Concurrent mirror updates should be recognized as conflict, not quietly flattened into old and new.

**Failure it prevents:** Accidentally overwriting a concurrent update as though it were older.

**Related lab:** `labs/level_05`

## CRDT

**Definition:** A data type designed so replicas can merge without coordination and converge.

**Use it when:** Final-tower dashboards count keys claimed or failures across mirror realms.

**Makai promise:** Operational counters should converge after partitions without pretending exclusive ownership is mergeable.

**Failure it prevents:** Divergent counters after partitions or replayed replication events.

**Related lab:** `labs/level_05`

## LSM Compaction

**Definition:** A storage maintenance process that merges sorted write segments into fewer, cleaner files.

**Use it when:** High-churn gate-run writes create many small segments that slow reads.

**Makai promise:** Heavy write pressure should not make every final-tower lookup drag through old fragments forever.

**Failure it prevents:** Read amplification and unbounded storage fragmentation.

**Related lab:** `labs/level_06`

## Raft Majority Commit

**Definition:** A consensus rule where an entry is committed after a majority of nodes accepts it.

**Use it when:** Makai needs a coordinated shop lock or rescue-control decision.

**Makai promise:** A rescue decision should not be announced as committed when only a minority of nodes accepted it.

**Failure it prevents:** Split-brain commits and writes acknowledged by too small a group.

**Related lab:** `labs/level_06`
