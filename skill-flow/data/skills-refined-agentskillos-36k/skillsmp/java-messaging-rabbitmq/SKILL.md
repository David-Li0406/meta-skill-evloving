---
name: java-messaging-rabbitmq
description: RabbitMQ queue patterns with acknowledgements, retries, dead-lettering, and ordering constraints. Use when building job queues, async workers, or diagnosing requeue/poison issues.
license: Apache-2.0
compatibility: JDK 17+ (recommended 21+). Any framework. RabbitMQ 3.x. Works with Gradle/Maven. Applies to AMQP 0-9-1 clients.
metadata:
  owner: backend-platform
  version: "1.0"
  tags: [java, rabbitmq, amqp, queue, retry, dlx, ordering, reliability, testing]
---

# RabbitMQ Messaging Playbook (Java)

## Scope

### In scope

- Exchange/queue/binding contract templates.
- Worker reliability: ack/nack/reject, prefetch, consumer concurrency.
- Retry strategies: immediate retry, delayed retry via TTL + DLX, poison message handling.
- Dead-letter exchanges and error taxonomy.
- Publisher reliability: publisher confirms, mandatory flag patterns.
- Ordering constraints and design options.
- Test harness guidance for unit and integration.

### Out of scope

- Cluster ops (mirroring, quorum sizing, disk alarms), TLS setup, and user/permission mgmt.

## When to use

- Implementing async job processing or event fanout using RabbitMQ.
- Seeing “message stuck/unacked”, infinite redelivery loops, or out-of-order side effects.
- You need standardized “queue contract + worker guidelines”.

## Inputs (required context)

- Pattern type: work queue, pub/sub, routing, RPC.
- Ordering requirement: strict FIFO? per key? no ordering needed?
- Retry policy: max attempts, delay schedule, poison handling.
- Delivery guarantees needed: at-least-once is typical; exactly-once requires idempotency.
- Expected payload size and throughput.
- Existing naming conventions and environment separation.

## Concepts (minimum shared vocabulary)

- **Exchange** routes messages to queues (direct/topic/fanout/headers).
- **Queue** stores messages; consumers pull.
- **Ack** acknowledges processing success; without ack, message can be re-delivered.
- **Prefetch** limits unacked deliveries per consumer (QoS).
- **DLX** (Dead Letter Exchange) receives rejected/expired messages.
- **Publisher confirms** acknowledge broker persistence/acceptance of published messages.

## Procedure (step-by-step)

### Step 1 — Write a Queue Contract

Create `docs/messaging/rabbitmq/<name>.md` with:

- Exchange name/type, queue name, routing keys.
- Producer(s) and consumer(s).
- Message schema and headers (correlation-id, idempotency-key).
- Delivery mode (persistent vs transient).
- Retry policy (attempts + delays).
- DLX/DLQ wiring and poison handling.
- Ordering constraints and consumer concurrency policy.

**Recommended naming**

- Exchanges: `<domain>.<purpose>.x`
- Queues: `<domain>.<purpose>.q`
- DLQ: `<domain>.<purpose>.dlq`
- Retry queues: `<domain>.<purpose>.retry.<delay>`

### Step 2 — Publisher reliability baseline

Goal: avoid “published but never routed” and detect broker-side failures.

**Baseline**

- Enable **publisher confirms**.
- Consider `mandatory` publishing if routing correctness matters.
- Mark messages as persistent if they must survive broker restart (delivery mode 2).

### Step 3 — Consumer reliability baseline (ack + prefetch)

**Ack strategy**

- Ack only after side effects are durable (DB commit done).
- On failure:
  - If transient and attempts remain: route to retry (delayed) or requeue with backoff policy.
  - If permanent or attempts exhausted: dead-letter to DLQ.

**Prefetch**

- Set prefetch (QoS) to avoid large “in-flight” unacked messages that amplify failures.
- Typical starting point: prefetch=10..100 depending on job time.

### Step 4 — Retry strategy options (pick one)

#### Option A: Immediate retry (simple, risky)

- `basic.nack(requeue=true)` triggers immediate redelivery.
- Risk: hot loop, thundering herd, dependency meltdown.
- Only acceptable for tiny transient blips with circuit breakers elsewhere.

#### Option B: Delayed retry via TTL + DLX (recommended)

- Main queue dead-letters to a delay queue with TTL.
- Delay queue dead-letters back to main exchange after TTL.
- Implement multiple delay tiers: 10s, 1m, 5m, 30m.
- Encode attempt count in headers.

#### Option C: Dedicated retry exchange with routing keys

- Use topic exchange with `retry.<delay>` keys mapping to corresponding TTL queues.

### Step 5 — Poison message handling

- Define max attempts (e.g., 5).
- If exhausted: publish to DLQ with error metadata:
  - exception class, message, stack hash
  - attempt count
  - original routing key
  - first failure time
- Provide a replay tool with filtering and rate-limits.

### Step 6 — Ordering constraints (choose intentionally)

RabbitMQ provides FIFO per queue, but concurrency breaks perceived ordering.

Options:

1) **Strict ordering**: single consumer, prefetch=1.
2) **Per-key ordering**:
   - Use consistent routing key → map to dedicated queues (sharded queues).
   - Or encode key→queue mapping at publisher.
3) **No ordering**: scale consumers; ensure idempotency and commutativity.

## Output / Artifacts

- `docs/messaging/rabbitmq/<name>.md` (queue/exchange contract)
- `src/main/java/.../messaging/rabbitmq/` publisher + worker skeleton
- `src/test/java/.../messaging/rabbitmq/` unit tests and integration tests
- Optional: `tools/rabbitmq-dlq-replayer/` CLI

## Definition of Done (DoD)

- [ ] Contract exists: exchange/queue/bindings + retry + DLQ + ordering policy.
- [ ] Publisher confirms enabled (or documented exception).
- [ ] Consumer acks after durable success; failures route to retry/DLQ deterministically.
- [ ] Prefetch configured; consumer concurrency justified.
- [ ] Poison messages end up in DLQ with metadata; replay plan exists.
- [ ] Tests cover happy path + transient retry + permanent DLQ.

## Guardrails (What NOT to do)

- Never `requeue=true` in a tight loop without backoff and max attempts.
- Never ack before the side effect is committed.
- Avoid massive prefetch with slow jobs (memory spikes + long redelivery storms).
- Avoid assuming “exactly-once” without explicit idempotency keys.

## Skeletons

### Queue Contract Template (docs/messaging/rabbitmq/<name>.md)

- Exchange:
- Type:
- Queue:
- Routing keys:
- Producers:
- Consumers:
- Payload schema:
- Headers: correlation-id, idempotency-key, attempt
- Durability: persistent?
- Prefetch:
- Retry schedule:
- DLQ:
- Ordering policy:
- Observability:

### Publisher (Java client) sketch

```java
// Pseudocode: configure channel confirm mode and publish persistent messages
channel.confirmSelect();
AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
  .contentType("application/json")
  .deliveryMode(2) // persistent
  .correlationId(correlationId)
  .headers(headers)
  .build();

channel.basicPublish(exchange, routingKey, true, props, body);
channel.waitForConfirmsOrDie(5_000);
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
