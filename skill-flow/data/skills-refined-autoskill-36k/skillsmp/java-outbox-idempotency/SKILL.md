---
name: java-outbox-idempotency
description: Transactional Outbox + idempotency guardrails for practical exactly-once behavior. Use when you see double-publish, inconsistent state, or need reliable integration events.
license: Apache-2.0
compatibility: JDK 17+ (recommended 21+). Any framework. Any SQL DB with transactions. Works with Gradle/Maven.
metadata:
  owner: backend-platform
  version: "1.0"
  tags: [java, outbox, idempotency, microservices, messaging, kafka, rabbitmq, reliability, cdc]
---

# Transactional Outbox + Idempotency (Practical Exactly-Once)

## Scope

### In scope

- The **Transactional Outbox** pattern: write business state + outbox event in the same DB transaction.
- Relay strategies: polling publisher vs CDC-based (e.g., Debezium).
- Idempotency keys and dedup stores for consumers and inbound requests.
- Failure handling: retries, backoff, poison events, replay.
- Test strategy to prove “no lost events + bounded duplicates”.

### Out of scope

- Full CDC infra operations (Kafka Connect ops, Debezium tuning) unless requested.
- Vendor-specific exactly-once claims; focus is practical correctness.

## When to use

- You must publish integration events after DB commit without race conditions.
- You see double publish, missing events, or “state changed but event not sent”.
- You need robust “read-process-write” reliability across services.

## Inputs (required context)

- Database type and transaction model.
- Messaging target (Kafka, RabbitMQ, HTTP webhook).
- Event volume and acceptable latency.
- Ordering requirements (per aggregate).
- Existing “event id” strategy (UUID? ULID?).
- Consumer idempotency needs and storage options (DB/Redis).

## Core idea (why this works)

You cannot atomically commit a DB transaction and an external message publish with a typical broker.
Outbox solves this by:

1) Commit DB state + outbox row in ONE transaction.
2) Publish outbox rows asynchronously with retries.
3) Consumers handle duplicates via idempotency/dedup.

This yields:

- **No lost events** (if relay is reliable)
- **At-least-once delivery** with bounded duplicates
- **Effectively-once processing** when consumers are idempotent

## Procedure (step-by-step)

### Step 1 — Define an Event Contract

Create `docs/events/<domain>/<event>.md`:

- eventType, schema, compatibility rules
- idempotency key fields
- partitioning/ordering key (aggregateId)
- producer service ownership
- consumer expectations

### Step 2 — Add an Outbox table (DB schema)

Create table `outbox_events` (example columns):

- `id` (UUID/ULID, PK)
- `aggregate_type` (string)
- `aggregate_id` (string)
- `event_type` (string)
- `payload` (json/text/bytes)
- `headers` (json) [optional]
- `created_at` (timestamp)
- `published_at` (timestamp nullable)
- `status` (NEW, PUBLISHED, FAILED) [optional]
- `attempts` (int)
- `next_attempt_at` (timestamp)

Indexes:

- `(status, next_attempt_at, created_at)`
- `(aggregate_type, aggregate_id, created_at)` if ordering needed

### Step 3 — Transaction boundary: write state + outbox in one commit

In your service layer:

1) Begin DB transaction.
2) Apply business changes.
3) Insert outbox event row.
4) Commit.

**Rule**

- No external I/O (broker publish) inside the transaction.

### Step 4 — Relay pattern (choose one)

#### Option A: Polling relay (simplest to ship)

- A background worker selects `NEW` outbox rows with `FOR UPDATE SKIP LOCKED` (DB dependent).
- Publishes events to broker.
- Marks row as `PUBLISHED` with `published_at`.
- On failure: increment attempts; compute `next_attempt_at` (exponential backoff); keep `FAILED` after max attempts.

Pros: minimal infra.
Cons: extra DB load; publish latency tied to polling interval.

#### Option B: CDC relay (Debezium Outbox pattern)

- Use CDC to stream outbox rows to Kafka.
- Debezium Outbox Event Router can transform to Kafka messages.

Pros: low app complexity; scalable.
Cons: requires CDC infra and ops.

### Step 5 — Consumer idempotency (mandatory)

Choose one:

1) **Dedup table** (strongest)
   - Table `processed_events(event_id PK, processed_at, consumer_name)`
   - Transaction: insert `event_id`; if conflict → already processed → skip
2) **Business-key idempotency**
   - Use unique constraints on business operations.
3) **Redis SETNX** (fast, but TTL pitfalls)
   - SETNX eventId with TTL > maximum replay window.

### Step 6 — Inbound idempotency keys (HTTP/RPC commands)

For “create payment” / “place order” calls:

- Require client-provided idempotency key.
- Store `(idempotency_key, request_hash, response_snapshot)` with TTL.
- If repeated with same hash: return same response.
- If same key but different hash: reject (409/422).

### Step 7 — Replay & recovery

- Provide a controlled replay tool that can:
  - replay by event type, time range, aggregate id
  - cap max replay count
  - rate limit
- Keep outbox rows for a retention window (e.g., 7–30 days) to enable replay.

## Output / Artifacts

- Outbox DB migration(s)
- Event contract docs under `docs/events/`
- Relay worker module `.../outbox/OutboxPublisher`
- Consumer idempotency guard `.../idempotency/ProcessedEventStore`
- Tests proving correctness

## Definition of Done (DoD)

- [ ] Outbox table exists with indexes and retention plan.
- [ ] Business write + outbox insert are atomic in one DB transaction.
- [ ] Relay publishes reliably with retries/backoff and marks rows published.
- [ ] Consumer is idempotent with dedup store or strong natural idempotency.
- [ ] Replay tool exists or documented procedure exists.
- [ ] Tests cover: crash before publish, crash after publish, duplicate deliveries.

## Guardrails (What NOT to do)

- Never publish to broker inside the DB transaction.
- Never assume “broker exactly-once” removes need for idempotent consumers.
- Avoid “delete outbox row immediately” unless you have another replay mechanism.
- Avoid Redis TTL dedup if your replay window can exceed TTL.

## Test plan (must-have)

1) **Atomicity test**
   - Simulate exception after state update but before outbox insert → ensure rollback.
2) **Publish retry test**
   - Force broker failure → ensure attempts increase and row remains NEW/FAILED.
3) **Duplicate delivery test**
   - Deliver same event twice → ensure consumer side effect runs once.

## References

- Transactional Outbox pattern and related idempotency patterns are documented widely in microservices literature.
- CDC-based outbox routing is supported by Debezium Outbox Event Router.
