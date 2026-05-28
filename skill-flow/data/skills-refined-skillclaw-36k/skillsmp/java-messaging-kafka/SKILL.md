---
name: java-messaging-kafka
description: Kafka producer/consumer patterns with at-least-once semantics, DLQ topics, and schema evolution. Use when building event-driven features or diagnosing lag/dup/replay issues.
license: Apache-2.0
compatibility: JDK 17+ (recommended 21+). Any framework. Kafka 2.8+ (transactions supported). Works with Gradle/Maven.
metadata:
  owner: backend-platform
  version: "1.0"
  tags: [java, kafka, messaging, reliability, dlq, schema-evolution, testing]
---

# Kafka Messaging Playbook (Java)

## Scope

### In scope

- Topic/partition/key design that preserves ordering where required.
- Producer reliability: idempotent producer, acks, retries, timeouts, batching.
- Consumer reliability: offset commit strategy, reprocessing safety, at-least-once workflows.
- DLQ design using “dead-letter topics” + error taxonomy + replay strategy.
- Schema evolution contracts (Avro/Protobuf/JSON) and compatibility strategy.
- Test harness guidance (unit + integration) and benchmarking hooks.

### Out of scope

- Kafka cluster operations (broker sizing, KRaft/ZK migration, security hardening).
- Vendor-specific features beyond standard Kafka protocol (unless explicitly requested).
- Full-blown streaming pipelines (Kafka Streams) unless asked.

## When to use

- You are adding a Kafka-based integration / event-driven feature.
- You see consumer lag, duplicates, poison messages, or broken compatibility after schema changes.
- You need a repeatable “topic contract” and “handler skeleton” with tests.

## Inputs (required context)

Ask the user (or infer from repo) for:

- Kafka client library (Apache Kafka clients vs Spring Kafka vs others).
- Delivery semantics needed per message type: best-effort vs at-least-once vs effectively-once.
- Ordering constraints: per user? per entity? global?
- Throughput/latency targets and message size distribution.
- Existing topic naming conventions, environment separation, and retention requirements.
- Current consumer commit pattern (auto-commit? manual commit?).

## Concepts (minimum shared vocabulary)

- **Partition ordering**: ordering is only guaranteed within a partition.
- **Keying strategy**: key determines partition; stable key → stable ordering for that entity.
- **Consumer group**: scaling via partitions; each partition assigned to one consumer instance in a group.
- **Delivery semantics**: at-least-once is the practical default; “exactly-once” requires transactions + read_committed + careful boundaries.

## Procedure (step-by-step)

### Step 1 — Write a Topic Contract (single source of truth)

Create `docs/messaging/kafka/<topic>.md` with:

- Topic name + purpose.
- Ownership + producers + consumers.
- Key policy (what is the key; why).
- Payload schema (link to schema file).
- Compatibility policy (BACKWARD / FORWARD / FULL).
- Retention (time/size), compaction (yes/no), max message size expectations.
- Error handling: DLQ topic name, replay guidance.

**Recommended naming**

- Domain-based: `<domain>.<event>.v1` (or `<domain>.<event>` with schema versioning in registry).
- Environment is NOT in the topic name if you have separate clusters per env; include it if you share clusters.

### Step 2 — Producer reliability baseline (safe defaults)

Goal: avoid duplicates on broker retries and avoid “silent loss”.

**Baseline config (Apache Kafka clients)**

- `enable.idempotence=true`
- `acks=all`
- `retries` set high enough (or rely on defaults where safe)
- Prefer explicit `delivery.timeout.ms` (end-to-end send timeout)
- Monitor and tune: `linger.ms`, `batch.size`, `compression.type`, `buffer.memory`

**Why**

- Idempotence prevents duplicates caused by retries at producer layer.
- `acks=all` reduces risk of losing messages during leader failover.

**If you need atomic multi-topic writes or read-process-write**

- Use **transactions**:
  - Set `transactional.id=<stable-producer-instance-id>`
  - Call `initTransactions()`, `beginTransaction()`, `send(...)`, `commitTransaction()`
  - On fatal exceptions: `abortTransaction()` and rebuild producer.

### Step 3 — Consumer commit strategy (avoid “at-most-once by accident”)

**Rule of thumb**

- For **at-least-once**: commit offsets **after** successful processing.
- Disable auto commit: `enable.auto.commit=false`

**Two common safe patterns**

1) **Process → commit**
   - Poll records
   - Process each record (idempotent processing strongly recommended)
   - Commit offsets after the batch (or per partition)
2) **Transactional consume-transform-produce (EOS-ish)**
   - Consumer `isolation.level=read_committed`
   - Producer transactions
   - Use `sendOffsetsToTransaction(...)`
   - Commit transaction to atomically publish output + offsets

### Step 4 — Define idempotency at the handler boundary

Even with idempotent producer, duplicates can still happen (rebalances, retries, timeouts).
Make the handler idempotent using one of:

- **Natural idempotency**: “set status=PAID if not already”, UPSERT, compare-and-set.
- **Dedup store**: store `(eventId, consumerGroup)` or `(topic, partition, offset)` as “processed”.
  - Use a DB unique constraint or Redis SETNX with TTL (careful with TTL vs retention).
- **Inbox pattern**: persist incoming events, process once.

### Step 5 — DLQ (dead-letter topic) and replay strategy

Kafka does not have a built-in DLQ primitive; model it as a topic.

**Create DLQ topic per source topic**

- `<topic>.DLQ` or `<topic>.deadletter`
Include in DLQ message:
- original topic/partition/offset
- original key
- original payload (or pointer)
- error type, error message, stack hash
- first failure time, retry count
- handler version/build SHA

**Error taxonomy**

- **Transient** (retryable): timeouts, temporary dependency failures.
- **Permanent** (non-retryable): validation, incompatible schema, business rule violations.
- **Poison**: repeated failures beyond threshold → DLQ.

**Replay**

- Provide a “replayer” tool that reads DLQ topic and re-publishes to original topic (or a replay topic),
  with guardrails:
  - Require explicit filters (time range, error types, max count).
  - Rate-limit replay.
  - Preserve original key (to preserve ordering constraints).

### Step 6 — Schema evolution policy

Pick one of:

- Protobuf (recommended for internal RPC/events when teams align)
- Avro + Schema Registry (common with Kafka ecosystems)
- JSON (only if you enforce schema with CI + compatibility checks)

**Compatibility rules (high-level)**

- Additive change (adding optional fields) is generally safe.
- Never reuse field numbers/tags (Protobuf) or rename without aliasing policy (Avro/JSON).
- For breaking changes: introduce a new topic or a new message type version.

### Step 7 — Testing harness (unit + integration)

**Unit tests**

- Validate mapping, validation, retry classification, idempotency logic (dedup).
- Mock Kafka client wrapper, not Kafka itself.

**Integration tests**

- Use Testcontainers Kafka to validate:
  - Producer config works
  - Consumer handles rebalances
  - DLQ routing for permanent errors
  - Schema compatibility gating (if you have schema registry or checks)

## Output / Artifacts

- `docs/messaging/kafka/<topic>.md` (topic contract)
- `src/main/java/.../messaging/kafka/` producer + consumer skeleton
- `src/test/java/.../messaging/kafka/` unit tests
- `src/test/java/.../messaging/kafka/` integration tests with Testcontainers
- Optional: `tools/kafka-dlq-replayer/` CLI

## Definition of Done (DoD)

- [ ] Topic contract exists and includes keying + DLQ + replay policy.
- [ ] Producer uses idempotence baseline settings (or documented exception).
- [ ] Consumer uses manual commit after processing (or documented EOS flow).
- [ ] Handler is idempotent (natural idempotency or dedup store) with tests.
- [ ] DLQ routing exists for permanent failures; transient failures have bounded retry.
- [ ] Integration test covers happy path + poison path + DLQ publish.
- [ ] Observability: lag metrics and error counters are emitted.

## Guardrails (What NOT to do)

- Never enable auto-commit for side-effecting handlers unless you accept at-most-once.
- Never commit offsets before the business action is durable.
- Never change schema in a way that breaks old consumers without a compatibility plan.
- Avoid unbounded retries (infinite loops) without DLQ/offramp.
- Avoid “random keys”; define keying strategy explicitly.

## Skeletons (minimal, framework-agnostic)

### Topic Contract Template (docs/messaging/kafka/<topic>.md)

- Name:
- Purpose:
- Owners:
- Producers:
- Consumers:
- Key policy:
- Schema:
- Compatibility:
- Retention/Compaction:
- DLQ topic:
- Retry policy:
- Replay policy:
- SLO/metrics:

### Producer (Apache Kafka clients) snippet

```java
Properties props = new Properties();
props.put("bootstrap.servers", brokers);
props.put("acks", "all");
props.put("enable.idempotence", "true");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");

try (KafkaProducer<String, byte[]> producer = new KafkaProducer<>(props)) {
  ProducerRecord<String, byte[]> record = new ProducerRecord<>(topic, key, payload);
  producer.send(record).get(); // for demo; prefer async with callback in prod
}
```

### Consumer (manual ack) sketch

```java
DeliverCallback cb = (tag, delivery) -> {
  try {
    handler.handle(delivery.getBody(), delivery.getProperties(), delivery.getEnvelope());
    channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
  } catch (TransientException e) {
    retryOrDeadLetter(delivery, e);
    channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
  } catch (PermanentException e) {
    deadLetter(delivery, e);
    channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
  }
};
channel.basicQos(prefetch);
channel.basicConsume(queue, false, cb, tag -> {});
```

### Common failure modes & fixes

- Symptom: infinite redelivery → Cause: nack requeue hot loop → Fix: TTL+DLX retries, cap attempts.
- Symptom: messages “lost” → Cause: no confirms + unroutable publish → Fix: publisher confirms + mandatory.
- Symptom: out-of-order effects → Cause: multiple consumers/prefetch > 1 → Fix: ordering policy (single consumer or sharded queues) + idempotency.
- Symptom: many unacked → Cause: consumer stalled or prefetch too high → Fix: reduce prefetch, set timeouts, monitor consumers.

## References

Prefer official RabbitMQ docs for acknowledgements, confirms, prefetch, and DLX.
