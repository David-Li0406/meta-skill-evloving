## Kafka Troubleshooting

### Common Issues
- Consumer lag increasing: Check consumer processing speed and add more consumers
- Producer timeouts: Check network connectivity and broker health
- Disk space issues: Adjust retention policies or add storage
- High CPU usage: Tune garbage collection or upgrade hardware
- UnderMinIsrPartitionCount metric high: Investigate network issues or broker performance

### Diagnostic Commands
```bash
# Check topic details
kafka-topics --describe --topic my-topic --bootstrap-server localhost:9092

# Check consumer group status
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group my-group

# Monitor consumer lag
kafka-run-class kafka.tools.EndToEndLatency localhost:9092 my-topic 100

# Create a topic
kafka-topics --create --topic quickstart-events --bootstrap-server localhost:9092

# Send events to the topic using console producer
kafka-console-producer --topic quickstart-events --bootstrap-server localhost:9092

# Consume events from the topic using console consumer
kafka-console-consumer --topic quickstart-events --from-beginning --bootstrap-server localhost:9092
```

### Monitoring and Observability
#### Key JMX Metrics to Monitor:
- `UnderMinIsrPartitionCount` - Counts partitions where the number of In-Sync Replicas (ISR) is below the configured `min.insync.replicas` setting
- `ConsumerLag` for fetcher operations - Track during partition reassignment
- Rate of failed authentication attempts
- Request latency
- Consumer lag
- Total number of consumer groups
- Quota-related metrics

### Enable Remote JMX Monitoring
```bash
# Enable remote JMX by setting JMX_PORT environment variable
export JMX_PORT=9999

# For production, enable security with KAFKA_JMX_OPTS
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote.authenticate=true -Dcom.sun.management.jmxremote.ssl=true"
```

### MirrorMaker Metrics
- Record-related: record-count (total records replicated), record-rate (average records per second), record-age-ms
- Replication-latency-ms: time for records to propagate from source to target
- Byte-rate and byte-count: throughput in terms of bytes replicated
- Checkpoint-latency-ms: time required to replicate consumer offsets
```
