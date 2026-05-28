---
name: api-event-rabbitmq
description: Generate RabbitMQ event publishers and subscribers with tenant routing, durable queues, and automatic reconnection. Use when implementing event-driven architecture or cross-service communication.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# RabbitMQ Event Bus

## Purpose

Generate RabbitMQ event bus services for publishing and subscribing to domain events with tenant routing, durable queues, and automatic reconnection.

## When to Use

- Implementing event-driven architecture
- Cross-service communication
- Async event processing
- Domain event sourcing
- Microservices integration

## What It Generates

### Directory Structure

```
apps/api/src/modules/{feature}/events/
├── publishers/
│   ├── {event}.publisher.ts
│   └── index.ts
├── subscribers/
│   ├── {event}.subscriber.ts
│   └── index.ts
└── index.ts
```

## Patterns Enforced

### Tenant Routing

Events use tenant-specific routing keys:

- Format: `{tenantId}.{event.pattern}`
- Enables tenant-scoped event handling
- Supports wildcard subscriptions

### Durable Queues

Queues survive broker restarts:

- `queueOptions: { durable: true }`
- Messages persisted
- No data loss on restart

### Persistent Messages

Messages survive broker restart:

- `messageOptions: { persistent: true }`
- Critical for domain events
- At-least-once delivery

### Acknowledgments

Manual ack for reliability:

- Handlers ack on success
- Handlers nack on failure
- Dead letter for failed events

## Usage Example

```bash
/skill event-rabbitmq --name=User --events='created,updated,deleted'
```

## Related Files

- [Feature CQRS](../../core/feature-cqrs/SKILL.md) - Events in CQRS handlers
- [BullMQ Queues](../queue-bullmq/SKILL.md) - Queue jobs from events
