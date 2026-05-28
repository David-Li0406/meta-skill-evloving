---
name: kafka-event-streaming
description: Use this skill when you need to implement best practices and guidelines for Apache Kafka event streaming and distributed messaging systems.
---

# Kafka Event Streaming

This skill provides expert guidance on Apache Kafka, event streaming, and building event-driven architectures, including best practices for producers, consumers, and Kafka Streams.

## Core Concepts

- **Topics**: Categories for organizing messages.
- **Partitions**: Ordered sequences within topics enabling parallelism.
- **Producers**: Clients that publish messages to topics.
- **Consumers**: Clients that read messages from topics.
- **Consumer Groups**: Coordinate consumption across multiple consumers.
- **Brokers**: Kafka servers that store data and serve clients.
- **Offsets**: Unique sequential IDs for messages within partitions.

## Producer Best Practices

### Reliability Settings

```properties
acks=all               # Wait for all replicas to acknowledge
retries=MAX_INT        # Retry on transient failures
enable.idempotence=true # Prevent duplicate messages on retry
```

### Performance Tuning

- `batch.size`: Accumulate messages before sending.
- `linger.ms`: Wait time for batching.
- `buffer.memory`: Total memory for buffering unsent messages.
- `compression.type`: Use formats like gzip or snappy for bandwidth savings.

### Error Handling

- Implement retry logic with exponential backoff.
- Log and alert on send failures.
- Consider dead letter topics for messages that fail repeatedly.

## Consumer Best Practices

### Offset Management

- Track processed messages via offsets.
- Commit offsets after successful processing.
- Use `enable.auto.commit=false` for exactly-once semantics.

### Consumer Groups

- Share partitions among consumers in a group.
- Use `group.instance.id` for static membership to reduce rebalances.

### Processing Patterns

- Process messages in order within a partition.
- Implement idempotent processing for at-least-once delivery.

## Kafka Streams

### State Management

- Implement log compaction to maintain the latest version of each key.
- Monitor state store size and access patterns.

### Windowing Operations

- Handle out-of-order events and skewed timestamps.
- Configure grace periods for late-arriving data.

## Topic Design

### Partitioning Strategy

- Use partition keys to ensure related events are in the same partition.
- Choose keys carefully to avoid hot partitions.

### Topic Configuration

- Set `retention.ms` for message retention duration.
- Configure `cleanup.policy` for message deletion or compaction.

## Security

### Authentication

- Use SASL/SSL for client authentication and encryption in transit.

### Authorization

- Use Kafka ACLs for fine-grained access control.

## Monitoring and Observability

### Key Metrics

- Monitor producer and consumer metrics such as send rates and lag.
- Alert on increasing consumer lag trends.

## Testing

### Unit Testing

- Mock Kafka clients for isolated testing.
- Verify serialization/deserialization logic.

### Integration Testing

- Use embedded Kafka or Testcontainers for full producer-consumer flows.

## Common Patterns

### Event Sourcing

- Store all state changes as immutable events.
- Rebuild state by replaying events.

### CQRS (Command Query Responsibility Segregation)

- Separate write and read models using Kafka as the event store.

### Saga Pattern

- Coordinate distributed transactions across services using events.

### Change Data Capture (CDC)

- Capture database changes as Kafka events for real-time data synchronization.

## Resources

- [Apache Kafka](https://kafka.apache.org/)
- [Confluent Platform](https://www.confluent.io/)