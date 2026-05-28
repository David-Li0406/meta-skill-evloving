# Apache Kafka

**Category**: apache
**Description**: Distributed event streaming platform
**Homepage**: https://kafka.apache.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Kafka JavaScript clients*

- `kafkajs` - Modern Kafka client for Node.js
- `kafka-node` - Legacy Kafka client
- `node-rdkafka` - Node.js bindings for librdkafka
- `@confluentinc/kafka-javascript` - Confluent's Kafka client

#### PYPI
*Kafka Python clients*

- `kafka-python` - Pure Python Kafka client
- `confluent-kafka` - Confluent's Python client
- `aiokafka` - Async Kafka client
- `faust` - Stream processing library
- `pykafka` - Samsa's Kafka client

#### GO
*Kafka Go clients*

- `github.com/segmentio/kafka-go` - Segment's Kafka client
- `github.com/confluentinc/confluent-kafka-go` - Confluent Go client
- `github.com/IBM/sarama` - IBM's Kafka client (formerly Shopify)
- `github.com/twmb/franz-go` - High-performance client

#### MAVEN
*Kafka Java clients*

- `org.apache.kafka:kafka-clients` - Official Java client
- `org.apache.kafka:kafka-streams` - Kafka Streams
- `org.apache.kafka:kafka_2.13` - Kafka broker
- `io.confluent:kafka-avro-serializer` - Avro serialization
- `io.confluent:kafka-schema-registry-client` - Schema Registry client
- `org.springframework.kafka:spring-kafka` - Spring Kafka

#### RUBYGEMS
*Kafka Ruby clients*

- `ruby-kafka` - Pure Ruby Kafka client
- `karafka` - Framework for Kafka applications
- `rdkafka` - Ruby bindings for librdkafka

#### NUGET
*Kafka .NET clients*

- `Confluent.Kafka` - Confluent's .NET client
- `KafkaNet` - Legacy .NET client

#### CARGO
*Kafka Rust clients*

- `rdkafka` - Rust bindings for librdkafka
- `kafka` - Pure Rust Kafka client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Kafka usage*

- `server.properties` - Kafka broker configuration
- `producer.properties` - Producer configuration
- `consumer.properties` - Consumer configuration
- `connect-distributed.properties` - Kafka Connect config
- `kafka.yml` - Kafka YAML configuration
- `docker-compose.yml` - Often contains Kafka services

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]kafkajs['"]`
- KafkaJS import
- Example: `import { Kafka } from 'kafkajs';`

**Pattern**: `require\(['"]kafka-node['"]\)`
- kafka-node require
- Example: `const kafka = require('kafka-node');`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+kafka\s+import`
- kafka-python import
- Example: `from kafka import KafkaProducer, KafkaConsumer`

**Pattern**: `^from\s+confluent_kafka\s+import`
- confluent-kafka import
- Example: `from confluent_kafka import Producer, Consumer`

**Pattern**: `^import\s+aiokafka`
- aiokafka import
- Example: `import aiokafka`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/segmentio/kafka-go"`
- kafka-go import
- Example: `import kafka "github.com/segmentio/kafka-go"`

**Pattern**: `"github\.com/IBM/sarama"|"github\.com/Shopify/sarama"`
- Sarama import
- Example: `import "github.com/IBM/sarama"`

#### Java
Extensions: `.java`

**Pattern**: `import\s+org\.apache\.kafka\.`
- Kafka Java client import
- Example: `import org.apache.kafka.clients.producer.KafkaProducer;`

**Pattern**: `import\s+org\.springframework\.kafka\.`
- Spring Kafka import
- Example: `import org.springframework.kafka.core.KafkaTemplate;`

### Code Patterns

**Pattern**: `bootstrap\.servers|KAFKA_BOOTSTRAP_SERVERS`
- Kafka bootstrap servers configuration
- Example: `bootstrap.servers=localhost:9092`

**Pattern**: `KafkaProducer|KafkaConsumer|KafkaStreams`
- Kafka client class usage
- Example: `new KafkaProducer<>(props)`

**Pattern**: `kafka://|PLAINTEXT://|SSL://|SASL_`
- Kafka protocol URLs
- Example: `PLAINTEXT://localhost:9092`

**Pattern**: `:9092|:9093|:9094`
- Kafka default ports
- Example: `localhost:9092`

**Pattern**: `\.confluent\.cloud|pkc-[a-z0-9]+\.`
- Confluent Cloud URLs
- Example: `pkc-abc123.us-east-1.aws.confluent.cloud:9092`

---

## Environment Variables

- `KAFKA_BOOTSTRAP_SERVERS` - Kafka broker addresses
- `KAFKA_BROKERS` - Alternative broker variable
- `KAFKA_USERNAME` - SASL username
- `KAFKA_PASSWORD` - SASL password
- `KAFKA_API_KEY` - Confluent Cloud API key
- `KAFKA_API_SECRET` - Confluent Cloud API secret
- `KAFKA_SASL_MECHANISM` - SASL mechanism
- `KAFKA_SECURITY_PROTOCOL` - Security protocol
- `KAFKA_SSL_CA` - SSL CA certificate
- `SCHEMA_REGISTRY_URL` - Schema Registry URL
- `SCHEMA_REGISTRY_API_KEY` - Schema Registry API key
- `SCHEMA_REGISTRY_API_SECRET` - Schema Registry API secret

## Detection Notes

- Default port 9092 for PLAINTEXT, 9093 for SSL
- Confluent Cloud uses different authentication
- Schema Registry often paired with Kafka
- Kafka Connect for integrations
- ZooKeeper dependency in older versions (deprecated)

---

## Secrets Detection

### Credentials

#### Kafka SASL Password
**Pattern**: `(?:kafka|KAFKA).*(?:password|PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Kafka SASL password
**Example**: `KAFKA_PASSWORD=secretpass`

#### Confluent Cloud API Key
**Pattern**: `(?:kafka|KAFKA|confluent|CONFLUENT).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([A-Z0-9]{16})['"]?`
**Severity**: critical
**Description**: Confluent Cloud API key
**Example**: `KAFKA_API_KEY=ABCDEFGH12345678`

#### Confluent Cloud API Secret
**Pattern**: `(?:kafka|KAFKA|confluent|CONFLUENT).*(?:api[_-]?secret|API[_-]?SECRET)\s*[=:]\s*['"]?([A-Za-z0-9+/=]{64})['"]?`
**Severity**: critical
**Description**: Confluent Cloud API secret
**Example**: `KAFKA_API_SECRET=abc123def456...`

#### Schema Registry Credentials
**Pattern**: `(?:schema[_-]?registry|SCHEMA[_-]?REGISTRY).*(?:api[_-]?secret|password|PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Schema Registry API credentials

### Validation

#### API Documentation
- **Apache Kafka**: https://kafka.apache.org/documentation/
- **Confluent Cloud**: https://docs.confluent.io/cloud/current/

---

## TIER 3: Configuration Extraction

### Bootstrap Servers Extraction

**Pattern**: `bootstrap\.servers\s*[=:]\s*['"]?([^\s'"]+)['"]?`
- Kafka bootstrap servers
- Extracts: `bootstrap_servers`
- Example: `bootstrap.servers=localhost:9092,localhost:9093`

### Topic Extraction

**Pattern**: `(?:topic|KAFKA_TOPIC)\s*[=:]\s*['"]?([a-zA-Z0-9._-]+)['"]?`
- Kafka topic name
- Extracts: `topic_name`
- Example: `topic=my-events`

### Consumer Group Extraction

**Pattern**: `(?:group\.id|group[_-]?id|KAFKA_GROUP_ID)\s*[=:]\s*['"]?([a-zA-Z0-9._-]+)['"]?`
- Consumer group ID
- Extracts: `group_id`
- Example: `group.id=my-consumer-group`
