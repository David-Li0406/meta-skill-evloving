---
name: api-queue-bullmq
description: Generate BullMQ job queues and workers with tenant isolation, retry logic with exponential backoff, and dead letter queue. Use when creating background jobs or async workflows.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# BullMQ Job Queues

## Purpose

Generate BullMQ job queues with tenant isolation, automatic retry logic with exponential backoff, dead letter queue configuration, and comprehensive error handling.

## When to Use

- Creating background job processors (emails, reports, batch operations)
- Implementing async workflows with retries
- Building tenant-isolated job queues
- Creating scheduled/recurring jobs
- Processing AI requests with priority queues

## What It Generates

### Directory Structure

```
apps/api/src/modules/{feature}/queues/
├── {queue}-queue.service.ts
├── {queue}-queue.spec.ts
├── {queue}-worker.service.ts
└── index.ts
```

## Patterns Enforced

### Tenant Isolation

- Job queues are tenant-prefixed: `tenant:{tenantId}:{queueName}`
- Job data includes `tenantId` for processing context
- Workers validate tenant access before processing

### Retry Configuration

- Default: 3 attempts with exponential backoff (2s base)
- Customizable per job type
- Dead letter queue for permanently failed jobs

### Priority Support

- Jobs support priority levels (1-10, lower = higher priority)
- Separate queues for high/normal/low priority
- AI requests use high-priority queue

## Usage Example

```bash
/skill queue-bullmq --name=Email --jobs='welcome,password-reset,report' --withScheduler=true
```

## Related Files

- [Event RabbitMQ](../event-rabbitmq/SKILL.md) - Event-driven job scheduling
- [Cache Redis](../cache-redis/SKILL.md) - Caching job results
- [Tracing OTEL](../tracing-otel/SKILL.md) - OpenTelemetry job tracing
