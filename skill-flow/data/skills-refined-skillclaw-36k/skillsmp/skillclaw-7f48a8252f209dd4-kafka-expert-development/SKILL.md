---
name: kafka-expert-development
description: Use this skill when you need expert guidance on Apache Kafka, including best practices for event streaming and distributed messaging.
---

# Skill body

## Core Concepts

- Topics, partitions, and offsets
- Producers and consumers
- Consumer groups
- Kafka Streams
- Kafka Connect
- Exactly-once semantics

## Architecture Overview

### Core Components

- **Topics**: Categories/feeds for organizing messages
- **Partitions**: Ordered, immutable sequences within topics enabling parallelism
- **Producers**: Clients that publish messages to topics
- **Consumers**: Clients that read messages from topics
- **Consumer Groups**: Coordinate consumption across multiple consumers
- **Brokers**: Kafka servers that store data and serve clients

## Producer

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',  # Wait for all replicas
    retries=3
)

# Send message
future = producer.send('user-events', {
    'user_id': '123',
    'event': 'login',
    'timestamp': '2024-01-01T00:00:00Z'
})

# Wait for acknowledgment
record_metadata = future.get(timeout=10)
print(f"Topic: {record_metadata.topic}, Partition: {record_metadata.partition}")

producer.flush()
producer.close()
```

## Consumer

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    group_id='my-group',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(f"Received: {message.value}")

    # Process message
    process_event(message.value)

    # Manual commit
    consumer.commit()
```

## Kafka Streams

```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-app");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

StreamsBuilder builder = new StreamsBuilder();

KStream<String, String> source = builder.stream("input-topic");

// Transform and filter
KStream<String, String> transformed = source
    .filter((key, value) -> value.length() > 10)
    .mapValues(value -> value.toUpperCase());

transformed.to("output-topic");

KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();
```

## Best Practices

### Topic Design

- Use partition keys to place related events in the same partition.
- Choose keys carefully to avoid uneven distribution causing hot partitions.
- Start with the number of consumers you expect to run concurrently.

### Producer Best Practices

- **Reliability Settings**:
    ```
    acks=all               # Wait for all replicas to acknowledge
    retries=MAX_INT        # Retry on transient failures
    enable.idempotence=true # Prevent duplicate messages on retry
    ```

### Performance Tuning

- `batch.size`: Accumulate messages before sending to improve throughput.
- Monitor consumer lag and implement idempotent producers.

## Anti-Patterns

❌ Single partition topics  
❌ No error handling in consumers  
❌ Leaving todos or placeholders in the implementation