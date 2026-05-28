# Stream Processing Learning Plan
## Based on "Designing Data-Intensive Applications" Chapter 11

This learning plan guides you through understanding stream processing systems, from fundamentals to advanced concepts.

---

## Learning Objectives

By the end of this learning plan, you will understand:
- The difference between batch and stream processing
- How event streams are transmitted and stored
- Different messaging systems and their trade-offs
- How to process streams in real-time
- Fault tolerance in stream processing systems
- Time handling and windowing in streams

---

## Prerequisites

Before starting, you should be familiar with:
- Basic database concepts
- Distributed systems fundamentals (from DDIA Chapters 1-9)
- Batch processing concepts (DDIA Chapter 10)

---

## Learning Path

### Phase 1: Foundations (Days 1-3)
**Goal**: Understand what stream processing is and why it's needed

#### Module 1.1: Introduction to Streams
- **Concepts**: Unbounded data, continuous processing, events
- **Key Reading**: Chapter 11 introduction (lines 0-19)
- **Questions to Answer**:
  - What is the fundamental difference between batch and stream processing?
  - Why can't batch processing always meet real-time requirements?
  - What is an "event" in stream processing?

#### Module 1.2: Transmitting Event Streams
- **Concepts**: Producers, consumers, topics, message delivery
- **Key Reading**: "Transmitting Event Streams" section (lines 20-37)
- **Questions to Answer**:
  - What are the components of a streaming system?
  - Why is polling inefficient for continuous processing?
  - How do events differ from batch records?

#### Module 1.3: Messaging Systems Overview
- **Concepts**: Message brokers, backpressure, durability, message loss
- **Key Reading**: "Messaging Systems" section (lines 39-57)
- **Questions to Answer**:
  - What happens when producers send faster than consumers can process?
  - What are the trade-offs between message durability and throughput?
  - When is message loss acceptable?

#### Checkpoint 1
- [ ] Can you explain why stream processing is needed?
- [ ] Can you describe the basic components of a streaming system?
- [ ] Do you understand the trade-offs in message delivery?

**AWS Hands-On**: See `references/aws-examples.md` Example 1 - Create a Kinesis stream and practice producing/consuming events

---

### Phase 2: Messaging Patterns (Days 4-6)
**Goal**: Understand different approaches to messaging and their trade-offs

#### Module 2.1: Direct Messaging vs Message Brokers
- **Concepts**: UDP multicast, webhooks, message queues, durability
- **Key Reading**: "Direct messaging" and "Message brokers" sections
- **Questions to Answer**:
  - What are the pros and cons of direct messaging?
  - How do message brokers improve on direct messaging?
  - How do message brokers differ from databases?

#### Module 2.2: Consumer Patterns
- **Concepts**: Load balancing, fan-out, acknowledgments, redelivery
- **Key Reading**: "Multiple consumers" and "Acknowledgments" sections
- **Questions to Answer**:
  - What is the difference between load balancing and fan-out?
  - How do acknowledgments prevent message loss?
  - Why does redelivery cause message reordering?

#### Module 2.3: Partitioned Logs
- **Concepts**: Log-based messaging, partitions, offsets, Apache Kafka
- **Key Reading**: "Partitioned Logs" section (lines 138-230)
- **Questions to Answer**:
  - How do log-based brokers differ from traditional message brokers?
  - What is a partition and why is partitioning used?
  - How do consumer offsets work?
  - What are the trade-offs of log-based vs JMS/AMQP-style brokers?

#### Checkpoint 2
- [ ] Can you compare traditional message brokers with log-based brokers?
- [ ] Can you explain when to use each messaging pattern?
- [ ] Do you understand how partitioning enables scalability?

**AWS Hands-On**: See `references/aws-examples.md` Examples 2 & 7 - Try SNS fan-out pattern and Kinesis partition keys for ordering

---

### Phase 3: Databases and Streams (Days 7-9)
**Goal**: Understand the relationship between databases and streaming systems

#### Module 3.1: Change Data Capture (CDC)
- **Concepts**: Database logs, replication, derived data
- **Key Reading**: "Change Data Capture" section
- **Questions to Answer**:
  - What is change data capture?
  - How can database changes be turned into streams?
  - What are the use cases for CDC?

#### Module 3.2: Event Sourcing
- **Concepts**: Immutable events, event logs, state reconstruction
- **Key Reading**: "Event Sourcing" section
- **Questions to Answer**:
  - How does event sourcing differ from traditional databases?
  - What are the benefits of storing events instead of current state?
  - What are the challenges with event sourcing?

#### Module 3.3: State, Streams, and Immutability
- **Concepts**: Mutable state vs immutable events, log compaction
- **Key Reading**: "State, Streams, and Immutability" section
- **Questions to Answer**:
  - How do you maintain state from event streams?
  - What is log compaction and when is it useful?
  - How do databases and streams relate to each other?

#### Checkpoint 3
- [ ] Can you explain how databases can be derived from event streams?
- [ ] Can you describe the benefits of event sourcing?
- [ ] Do you understand the relationship between state and streams?

**AWS Hands-On**: See `references/aws-examples.md` Examples 3 & 5 - Try DynamoDB Streams (CDC) and implement event sourcing pattern with Kinesis

---

### Phase 4: Stream Processing (Days 10-14)
**Goal**: Learn how to process and transform streams in real-time

#### Module 4.1: Uses of Stream Processing
- **Concepts**: Complex event processing, stream analytics, search indexes
- **Key Reading**: "Uses of Stream Processing" section
- **Questions to Answer**:
  - What are common use cases for stream processing?
  - How is stream processing different from batch processing?
  - What types of operations can be performed on streams?

#### Module 4.2: Reasoning About Time
- **Concepts**: Event time vs processing time, windows, straggler events
- **Key Reading**: "Reasoning About Time" section
- **Questions to Answer**:
  - What is the difference between event time and processing time?
  - What are windows and why are they needed?
  - How do you handle late-arriving events?

#### Module 4.3: Stream Joins
- **Concepts**: Stream-stream joins, stream-table joins, time windows
- **Key Reading**: "Stream Joins" section
- **Questions to Answer**:
  - How do you join multiple streams?
  - What are the challenges of joining streams?
  - How do stream joins differ from database joins?

#### Module 4.4: Fault Tolerance
- **Concepts**: Exactly-once semantics, idempotence, checkpointing
- **Key Reading**: "Fault Tolerance" section
- **Questions to Answer**:
  - What are the challenges of fault tolerance in stream processing?
  - How do stream processors achieve exactly-once semantics?
  - What is the role of checkpointing?

#### Checkpoint 4
- [ ] Can you describe different stream processing operations?
- [ ] Can you explain time handling in stream processing?
- [ ] Do you understand how to make stream processing fault-tolerant?

**AWS Hands-On**: See `references/aws-examples.md` Examples 4 & 6 - Build a Lambda stream processor and experiment with time windowing in Kinesis Data Analytics

---

## Final Assessment

### Comprehension Check
Answer these questions to verify your understanding:

1. **Architecture**: Design a stream processing system for a real-time analytics use case
2. **Trade-offs**: Compare batch processing vs stream processing for a given scenario
3. **Fault Tolerance**: Explain how to handle failures in a stream processing pipeline
4. **Time**: Design a windowing strategy for counting events in real-time
5. **Integration**: Describe how to keep a search index in sync with a database using streams

### Practical Projects (Optional)
1. Set up a local Kafka cluster and implement producer/consumer
2. Build a simple stream processor that aggregates events
3. Implement a CDC pipeline from a database to Kafka
4. Create a real-time dashboard using stream processing

---

## Resources

### Technologies to Explore
- **Apache Kafka** - Industry-standard log-based message broker
- **Apache Flink** - Stream processing framework
- **Apache Spark Streaming** - Micro-batch stream processing
- **AWS Kinesis** - Managed streaming service
- **Google Cloud Dataflow** - Managed stream/batch processing

### Further Reading
- Kafka: The Definitive Guide
- Streaming Systems by Tyler Akidau et al.
- Apache Flink documentation
- Martin Kleppmann's blog posts on stream processing

---

## Study Tips

1. **Read actively**: Take notes and draw diagrams as you read
2. **Ask questions**: Note anything you don't understand immediately
3. **Make connections**: Relate stream processing concepts to batch processing
4. **Practice**: Try to implement concepts with actual streaming systems
5. **Review regularly**: Revisit earlier modules to reinforce learning

---

## Next Steps

After completing this learning plan:
1. Explore Chapter 12 on "The Future of Data Systems"
2. Practice with real streaming platforms (Kafka, Flink, etc.)
3. Build a complete streaming application
4. Read advanced papers on stream processing
