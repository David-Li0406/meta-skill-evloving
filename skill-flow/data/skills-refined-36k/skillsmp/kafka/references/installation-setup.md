## Kafka Installation and Setup

### Installing kafka-python
To install the kafka-python library:
```bash
pip install kafka-python
```

Or with uv:
```bash
uv add kafka-python
```

### Local Setup

#### Using Downloaded Files
To set up Kafka locally, download the latest version and start the environment:

```bash
# Download and extract Kafka (example with version 4.1.1)
tar -xzf kafka_2.13-4.1.1.tgz
cd kafka_2.13-4.1.1

# Generate a Cluster UUID
export KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# Format Log Directories
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties

# Start the Kafka Server
bin/kafka-server-start.sh config/server.properties
```

#### Using Docker
JVM-based Docker image:
```bash
docker pull apache/kafka:4.1.1
docker run -p 9092:9092 apache/kafka:4.1.1
```

GraalVM-based native Docker image (experimental):
```bash
docker pull apache/kafka-native:4.1.1
docker run -p 9092:9092 apache/kafka-native:4.1.1
```

### Creating a Topic
```bash
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```
