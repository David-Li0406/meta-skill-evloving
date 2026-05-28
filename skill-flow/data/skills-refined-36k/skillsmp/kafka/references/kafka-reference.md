# Apache Kafka Reference Materials

## Common Configuration Properties

### Producer Configuration Properties
- `bootstrap.servers`: Comma-separated list of host and port pairs for establishing the initial connection to the Kafka cluster
- `key.serializer`: Serializer class for keys
- `value.serializer`: Serializer class for values
- `acks`: Number of acknowledgments the producer requires
- `retries`: Number of retries before attempting to send a message
- `batch.size`: Number of bytes to accumulate before sending
- `linger.ms`: Amount of time to wait before sending
- `buffer.memory`: Total bytes of memory the producer can use

### Consumer Configuration Properties
- `bootstrap.servers`: Comma-separated list of host and port pairs for establishing the initial connection to the Kafka cluster
- `group.id`: Unique identifier for the consumer group
- `key.deserializer`: Deserializer class for keys
- `value.deserializer`: Deserializer class for values
- `auto.offset.reset`: Action to take when there is no initial offset
- `enable.auto.commit`: Whether to auto-commit consumed offsets
- `max.poll.records`: Max number of records returned in a single poll

### Kafka Streams Configuration Properties
- `application.id`: Unique identifier for the application
- `bootstrap.servers`: Comma-separated list of host and port pairs for establishing the initial connection to the Kafka cluster
- `default.key.serde`: Default serializer/deserializer for keys
- `default.value.serde`: Default serializer/deserializer for values
- `cache.max.bytes.buffering`: Maximum number of bytes to be used for record caches across all threads
- `commit.interval.ms`: Frequency with which to save the position of the processor

## Kafka Commands Cheat Sheet

### Topic Management
```bash
# Create a topic
kafka-topics --create --topic my-topic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092

# List all topics
kafka-topics --list --bootstrap-server localhost:9092

# Describe a topic
kafka-topics --describe --topic my-topic --bootstrap-server localhost:9092

# Delete a topic
kafka-topics --delete --topic my-topic --bootstrap-server localhost:9092
```

### Producing and Consuming
```bash
# Produce messages to a topic
echo "Hello Kafka" | kafka-console-producer --broker-list localhost:9092 --topic my-topic

# Consume messages from a topic
kafka-console-consumer --bootstrap-server localhost:9092 --topic my-topic --from-beginning
```

### Consumer Groups
```bash
# List consumer groups
kafka-consumer-groups --bootstrap-server localhost:9092 --list

# Describe consumer group
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group my-group

# Reset consumer group offsets
kafka-consumer-groups --bootstrap-server localhost:9092 --group my-group --reset-offsets --to-earliest --topic my-topic --execute
```

## Best Practices for Different Scenarios

### High-Throughput Scenarios
- Increase the number of partitions to allow for greater parallelism
- Tune `batch.size` and `linger.ms` on the producer side
- Increase `fetch.min.bytes` and `fetch.max.wait.ms` on the consumer side
- Use compression (snappy, lz4, or zstd) to reduce network traffic

### Low-Latency Scenarios
- Reduce `linger.ms` to 0 or very low values
- Reduce `fetch.max.wait.ms` to get messages as soon as they're available
- Use smaller batch sizes for producers
- Consider using Kafka Streams for real-time processing

### Durability-Critical Scenarios
- Set `acks=all` for producers to ensure all replicas have received the message
- Use a replication factor of at least 3
- Set `min.insync.replicas` to at least 2
- Use idempotent producers to prevent duplicate messages
- Consider using transactions for exactly-once semantics

### Security Configuration
- Enable SSL encryption for data in transit
- Use SASL for authentication (SCRAM, Kerberos, or OAUTHBEARER)
- Enable ACLs for authorization
- Use SSL for inter-broker communication
- Secure ZooKeeper if using older Kafka versions

## Common Anti-Patterns to Avoid

1. **Single Partition Topics**: While simple, this prevents parallelism and limits throughput
2. **Too Many Partitions**: Each partition adds overhead; balance with expected throughput
3. **Auto Topic Creation**: Can lead to inconsistent configurations; create topics explicitly
4. **No Consumer Group Management**: Leads to rebalancing issues and message processing delays
5. **Not Handling Rebalancing**: Consumers should implement rebalance listeners
6. **Ignoring Offsets**: Proper offset management is crucial for message processing guarantees
7. **No Monitoring**: Essential for understanding cluster health and performance
