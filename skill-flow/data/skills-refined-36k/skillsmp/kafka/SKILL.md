---
name: kafka
description: Comprehensive Apache Kafka skill for building event-driven architectures from hello world to professionstal production systems. Provides guidance on Kafka setup, topic management, producer/consumer implementation, stream processing, security, monitoring, and best practices for scalable event streaming platforms.
---

# Apache Kafka Skill

This skill provides comprehensive guidance for building event-driven architectures using Apache Kafka from hello world examples to professional production systems. Based on official Kafka 4.1.1 documentation. Focuses on Python implementations using the kafka-python library.

## When to Use This Skill

Use this skill when working with:
- Kafka cluster setup and configuration
- Topic creation and management
- Producer and consumer implementation in Python
- Kafka Streams and stream processing
- Event-driven architecture design
- Kafka security and monitoring
- Production Kafka deployments
- Troubleshooting Kafka issues
- Using Share Consumer API for flexible message sharing

## Prerequisites

- Basic understanding of distributed systems
- Familiarity with messaging concepts
- Understanding of event-driven architecture patterns
- Python programming knowledge

## Core Concepts

Kafka is an event streaming platform that combines three key capabilities:
1. To **publish** (write) and **subscribe to** (read) streams of events
2. To **store** streams of events durably and reliably for as long as needed
3. To **process** streams of events as they occur or retrospectively

Kafka's core functionality revolves around a distributed commit log architecture where producers publish records to topics, brokers persist these records across multiple partitions for scalability and fault tolerance, and consumers subscribe to topics to process records either individually or as part of consumer groups for load balancing. The platform includes five primary client APIs:

- Producer API for publishing records
- Consumer API for subscribing to topics and processing records with consumer groups
- Share Consumer API (Preview) for flexible message sharing across multiple consumers without strict partition assignment
- Streams API for building real-time stream processing applications
- Connect API for integrating Kafka with external data systems
- Admin API for cluster management operations

Kafka supports exactly-once semantics for mission-critical applications requiring strong processing guarantees.

## Getting Started

### Installation
To install the kafka-python library:
```bash
pip install kafka-python
```

For complete installation and setup instructions, see [references/installation-setup.md](references/installation-setup.md).

### Installing Apache Kafka Server
We provide automated scripts to install the Apache Kafka server on your system:

**Prerequisites:** Either Java 17+ or Docker must be installed on your system. The installation scripts will automatically detect what's available and choose the appropriate installation method:
- If Java 17+ is available, it will perform a native installation
- If Docker is available but Java is not, it will run Kafka in a Docker container
- If neither is available, it will show an error with installation instructions

**IMPORTANT: You MUST ask user to run these scripts with administrator privileges (Windows) or as root (Linux/macOS)**

**For Windows:**
```powershell
# Install to default location (C:\Program Files\kafka)
powershell -ExecutionPolicy Bypass -File scripts\install-kafka.ps1

# Install to custom location
powershell -ExecutionPolicy Bypass -File scripts\install-kafka.ps1 -InstallPath "D:\MyKafka"
```

**For Linux/macOS:**
```bash
# Install to default location (/opt/kafka)
sudo bash scripts/install-kafka.sh

# Install to custom location
sudo bash scripts/install-kafka.sh --path "/custom/path/kafka"
```

After installation, use the generated `start-kafka.sh` or `start-kafka.bat` script to start the Kafka server, and `test-kafka.sh` or `test-kafka.bat` to verify the installation.

### Basic Producer Example
```python
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Create producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Send a message
future = producer.send('my-topic', key=b'1', value=b'hello world')

# Wait for delivery
try:
    record_metadata = future.get(timeout=10)
    print(f'Message delivered to {record_metadata.topic} [{record_metadata.partition}] at offset {record_metadata.offset}')
except KafkaError as e:
    print(f'Message delivery failed: {e}')

producer.close()
```

For more detailed producer examples, see [references/producer-examples.md](references/producer-examples.md).

### Basic Consumer Example
```python
from kafka import KafkaConsumer

# Create consumer
consumer = KafkaConsumer(
    'my-topic',
    group_id='my-consumer-group',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest'
)

# Consume messages
for message in consumer:
    print(f'Topic: {message.topic}, Partition: {message.partition}, Value: {message.value.decode("utf-8")}')
```

For more detailed consumer examples, see [references/consumer-examples.md](references/consumer-examples.md).

## Topic Management

### Basic Topic Operations
```python
from kafka import KafkaAdminClient
from kafka.admin import NewTopic

# Create admin client
admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])

# Create topic
new_topic = NewTopic(
    name="my-topic",
    num_partitions=3,
    replication_factor=1,
    topic_configs={
        'cleanup.policy': 'compact',
        'retention.ms': '86400000'  # 1 day
    }
)

admin_client.create_topics([new_topic])
```

For comprehensive topic management examples, see [references/admin-examples.md](references/admin-examples.md).

## Stream Processing

For stream processing with Python and Kafka, see [references/stream-processing.md](references/stream-processing.md).

## Kafka Connect

For working with Kafka Connect from Python, see [references/connect-examples.md](references/connect-examples.md).

## Security Configuration

### SSL Encryption
```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    security_protocol='SSL',
    ssl_cafile='/path/to/ca-cert',
    ssl_certfile='/path/to/client-cert.pem',
    ssl_keyfile='/path/to/client-key.pem',
    ssl_password='key-password'  # if key file is encrypted
)
```

For complete security configuration examples, see [references/producer-examples.md](references/producer-examples.md) and [references/consumer-examples.md](references/consumer-examples.md).

## Common Patterns

For common Kafka patterns and production best practices, see [references/common-patterns.md](references/common-patterns.md).

## Troubleshooting

For troubleshooting tips and diagnostic commands, see [references/troubleshooting.md](references/troubleshooting.md).
