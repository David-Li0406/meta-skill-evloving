# Stream Processing Key Concepts Reference

Quick reference guide for stream processing concepts from DDIA Chapter 11.

---

## Core Concepts

### Stream vs Batch
- **Batch Processing**: Operates on bounded (finite) datasets, processes all data before producing output
- **Stream Processing**: Operates on unbounded (infinite) datasets, processes data continuously as it arrives
- **Key Difference**: Stream processing doesn't wait for all data - it processes incrementally

### Event
- Small, self-contained, immutable object representing something that happened
- Contains timestamp and details of occurrence
- Examples: user action, sensor reading, log entry
- Encoded as text, JSON, or binary format

### Producer / Consumer
- **Producer**: Generates events and sends them to stream (also: publisher, sender)
- **Consumer**: Receives and processes events from stream (also: subscriber, recipient)
- Multiple consumers can read the same events independently

### Topic / Stream
- Logical grouping of related events
- Similar to how filename groups records in batch processing
- Multiple producers can write to same topic
- Multiple consumers can read from same topic

---

## Messaging Patterns

### Load Balancing
- Each message delivered to ONE consumer in a group
- Enables parallel processing by distributing work
- Used when messages are expensive to process
- JMS: shared subscription, AMQP: multiple clients on one queue

### Fan-out
- Each message delivered to ALL consumers
- Allows independent consumers to process same data stream
- Streaming equivalent of multiple batch jobs reading same file
- JMS: topic subscriptions, AMQP: exchange bindings

### Backpressure (Flow Control)
- Mechanism to prevent fast producers from overwhelming slow consumers
- Producer blocks when consumer can't keep up
- Alternative approaches: drop messages or buffer in queue
- Unix pipes and TCP use backpressure with small buffers

---

## Messaging Systems

### Direct Messaging
**Examples**: UDP multicast, ZeroMQ, webhooks

**Pros**:
- Low latency
- No intermediary to manage
- Simple architecture

**Cons**:
- Limited fault tolerance
- Messages lost if consumer offline
- Producer must handle retries
- Application aware of message loss possibility

### Message Brokers (Traditional)
**Examples**: RabbitMQ, ActiveMQ, AMQP, JMS

**Characteristics**:
- Centralized server for message routing
- Messages typically kept in memory
- Deleted after delivery and acknowledgment
- Supports load balancing and fan-out
- Asynchronous delivery
- Unbounded queueing possible

**Pros**:
- Handles client disconnections
- Durability options available
- Decouples producers from consumers

**Cons**:
- Not suitable for long-term storage
- Performance degrades with large queues
- Limited replay capabilities

### Log-based Message Brokers
**Examples**: Apache Kafka, Amazon Kinesis, DistributedLog

**Characteristics**:
- Append-only log on disk
- Messages persist (not deleted on consumption)
- Partitioned for scalability
- Sequential offset-based consumption

**Pros**:
- Durable storage
- Can replay messages
- High throughput (millions msg/sec)
- Fan-out trivially supported
- Messages stored for days/weeks
- Consistent throughput regardless of history

**Cons**:
- Coarser-grained load balancing (partition-level, not message-level)
- Head-of-line blocking within partition
- Max consumers = number of partitions

---

## Partitioned Logs Deep Dive

### Partition
- Independent log that can be read/written separately
- Messages within partition are totally ordered
- No ordering guarantee across partitions
- Enables horizontal scaling

### Offset
- Monotonically increasing sequence number within partition
- Uniquely identifies message position in partition
- Consumer tracks current offset
- Similar to log sequence number in database replication

### Consumer Offset Management
- Broker only tracks consumer's current offset (not per-message acks)
- All messages with offset < current are processed
- All messages with offset > current are unprocessed
- Reduced bookkeeping overhead vs traditional brokers
- Periodic offset commits (not per-message)

### Partitioning Strategy
- Events requiring consistent ordering go to same partition
- Partition chosen by partitioning key (e.g., user ID)
- Ensures events for same entity are ordered
- Load distributed across partitions for different keys

---

## Database Integration

### Change Data Capture (CDC)
- Captures database changes as stream of events
- Observes database log (write-ahead log or replication log)
- All writes become events in stream
- Enables derived data systems (search indexes, caches, analytics)
- Tools: Debezium, Maxwell, Databus

**Benefits**:
- Keep multiple systems in sync
- No dual writes problem
- Reliable and ordered changes
- Can rebuild derived data by replaying

### Event Sourcing
- Store all changes as sequence of immutable events
- Current state is result of applying all events
- Events are facts that happened (not mutable state)
- Different from CDC: events are the primary source of truth

**Benefits**:
- Complete audit log
- Can reconstruct state at any point in time
- Easier debugging (event replay)
- Enables new views on historical data

**Challenges**:
- Schema evolution of events
- Event versioning
- Reconstructing state can be expensive

### Log Compaction
- Keep only most recent event for each key
- Discards older versions
- Maintains complete current state while reducing storage
- Kafka feature for maintaining materialized views

---

## Stream Processing Operations

### Stateless Processing
- Each event processed independently
- No need to remember previous events
- Examples: filtering, parsing, transformation
- Easy to parallelize and scale

### Stateful Processing
- Maintains state across multiple events
- Examples: aggregations, joins, pattern detection
- Requires state management and fault tolerance
- More complex to implement correctly

### Windows
- Group events by time periods
- Types:
  - **Tumbling**: Fixed-length, non-overlapping intervals
  - **Hopping**: Fixed-length, overlapping intervals
  - **Sliding**: Window per event, looks back fixed duration
  - **Session**: Variable length based on activity gaps

### Aggregations
- Compute summaries over event streams
- Examples: counts, sums, averages, max/min
- Often windowed (e.g., events per minute)
- Requires maintaining state

---

## Time in Stream Processing

### Event Time
- When event actually occurred (according to device/source)
- Timestamp embedded in event
- Preferred for correctness
- May arrive out of order

### Processing Time
- When event is processed by stream processor
- Wall-clock time on processing machine
- Simpler to implement
- Can be misleading if delays occur

### Watermarks
- Estimate of "how far" event time has progressed
- Used to trigger window completion
- Declares "no more events with timestamp < X expected"
- Allows system to produce output for completed windows

### Straggler Events
- Events that arrive after window should have closed
- Late arrivals due to network delays, clock skew, etc.
- Options:
  - Drop late events
  - Keep windows open longer
  - Update previously emitted results
  - Track separately as late events

---

## Stream Joins

### Stream-Stream Join
- Join two event streams
- Need to maintain state for both streams
- Time window required (can't wait indefinitely)
- Example: match ad impression with later click

### Stream-Table Join (Enrichment)
- Join stream with database table
- Query database for each event or cache locally
- Example: add user profile info to clickstream

### Table-Table Join
- Both inputs are changelog streams
- Maintains materialized view of join result
- Example: user profiles joined with settings

---

## Fault Tolerance

### Processing Guarantees

**At-most-once**:
- Message processed zero or one time
- May lose messages on failure
- Simplest to implement, no overhead

**At-least-once**:
- Message processed one or more times
- May duplicate processing on failure
- Requires idempotent operations or deduplication

**Exactly-once**:
- Message processed exactly one time (appears to)
- Most complex to achieve
- Requires coordinated checkpointing and rollback

### Idempotence
- Operation can be applied multiple times with same result
- Makes at-least-once processing safe
- Natural for some operations (set value)
- Requires design for others (increment counter)

### Checkpointing
- Periodically save processor state
- Includes consumer offsets and internal state
- On failure, restore from checkpoint and replay
- Trade-off: checkpoint frequency vs recovery time

### Microbatching
- Process stream in small batches
- Each batch is atomic unit
- Easier to achieve exactly-once semantics
- Higher latency than pure streaming
- Used by Spark Streaming

---

## Technologies

### Apache Kafka
- Log-based message broker
- Distributed, partitioned, replicated
- High throughput (millions messages/sec)
- Configurable retention (days/weeks)
- Strong ordering within partition
- Consumer groups for load balancing

### Apache Flink
- True stream processing (not microbatch)
- Low latency
- Exactly-once guarantees
- Event time processing with watermarks
- Stateful processing support
- Powerful windowing

### Apache Spark Streaming
- Microbatch stream processing
- Built on Spark batch engine
- Higher latency than pure streaming
- Leverages Spark ecosystem
- Good for mixed batch/stream workloads

### AWS Kinesis
- Managed streaming service
- Similar to Kafka
- Integrated with AWS services
- Shards instead of partitions
- Automatic scaling options

---

## When to Use Stream Processing

### Good Use Cases
- Real-time analytics and dashboards
- Fraud detection
- Real-time recommendations
- Monitoring and alerting
- Real-time search index updates
- IoT sensor data processing
- Log aggregation and analysis
- Complex event processing (pattern matching)

### Consider Batch Instead When
- Historical analysis of complete dataset
- Reports that don't need real-time updates
- Complex analytics requiring multiple passes
- Data arrives in large batches anyway
- Eventual consistency is acceptable
- Debugging/development complexity matters more than latency

---

## Trade-offs Summary

| Aspect | Batch | Stream |
|--------|-------|--------|
| Data Type | Bounded | Unbounded |
| Latency | High (minutes to hours) | Low (seconds or less) |
| Throughput | Very high | High |
| Complexity | Lower | Higher |
| Fault Tolerance | Simpler (retry tasks) | More complex (state management) |
| Cost | Lower (run periodically) | Higher (continuous) |
| Use Case | Historical analysis | Real-time processing |

---

## Common Patterns

### Lambda Architecture
- Parallel batch and stream layers
- Batch: accurate, complete view (slow)
- Stream: fast, approximate view
- Merge results in serving layer
- Criticized for maintaining two systems

### Kappa Architecture
- Stream processing only
- Reprocessing by replaying stream
- Simpler: one processing framework
- Requires good stream replay capabilities

### Materialized Views
- Maintain query results incrementally
- Update as new events arrive
- Stream processing as continuous view maintenance
- Cache that never goes stale

---

## Best Practices

1. **Design for Idempotence**: Make operations safe to retry
2. **Choose Partitioning Key Carefully**: Ensures ordering where needed
3. **Monitor Consumer Lag**: Track how far consumers are behind
4. **Use Event Time**: More correct than processing time
5. **Handle Late Events**: Have strategy for stragglers
6. **Test Failure Scenarios**: Verify fault tolerance actually works
7. **Version Events**: Plan for schema evolution
8. **Keep State Small**: Easier to checkpoint and recover
9. **Separate Hot and Cold Paths**: Different latency requirements
10. **Document Semantics**: Clear about exactly-once vs at-least-once

---

## Further Learning

- Read Chapter 11 in detail for examples and deeper explanations
- Experiment with Kafka or similar platform
- Build a simple stream processor
- Study academic papers on stream processing (Dataflow model, etc.)
- Explore production streaming platforms (Kafka, Flink, Kinesis)
