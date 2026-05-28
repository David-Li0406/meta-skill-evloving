# Apache Kafka

**Category**: messaging
**Description**: Apache Kafka distributed streaming platform
**Homepage**: https://kafka.apache.org

## Package Detection

### NPM
*Kafka Node.js clients*

- `kafkajs`
- `node-rdkafka`
- `kafka-node`

### PYPI
*Kafka Python clients*

- `kafka-python`
- `confluent-kafka`
- `aiokafka`
- `faust`

### MAVEN
*Kafka Java clients*

- `org.apache.kafka:kafka-clients`
- `org.springframework.kafka:spring-kafka`

### GO
*Kafka Go clients*

- `github.com/segmentio/kafka-go`
- `github.com/confluentinc/confluent-kafka-go`

### RUBYGEMS
*Kafka Ruby clients*

- `ruby-kafka`
- `racecar`
- `karafka`

### Related Packages
- `@kafkajs/confluent-schema-registry`
- `avsc`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]kafkajs['"]`
- Type: esm_import

**Pattern**: `require\(['"]kafkajs['"]\)`
- Type: commonjs_require

**Pattern**: `require\(['"]node-rdkafka['"]\)`
- Type: commonjs_require

### Python

**Pattern**: `from\s+kafka`
- Type: python_import

**Pattern**: `import\s+kafka`
- Type: python_import

**Pattern**: `from\s+confluent_kafka`
- Type: python_import

**Pattern**: `from\s+aiokafka`
- Type: python_import

### Go

**Pattern**: `"github\.com/segmentio/kafka-go"`
- Type: go_import

**Pattern**: `"github\.com/confluentinc/confluent-kafka-go`
- Type: go_import

### Java

**Pattern**: `import\s+org\.apache\.kafka`
- Type: java_import

**Pattern**: `import\s+org\.springframework\.kafka`
- Type: java_import

## Environment Variables

*Kafka broker addresses*

*Kafka broker addresses (alternative)*

*Kafka broker list*

*Security protocol (PLAINTEXT, SSL, SASL_SSL)*

*SASL authentication mechanism*

*SASL username*

*SASL password*

*Consumer group ID*

*Schema Registry URL*


## Detection Notes

- Check for KAFKA_BOOTSTRAP_SERVERS environment variable
- Look for kafka:// or localhost:9092 connection strings
- Often used with Confluent Platform

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
