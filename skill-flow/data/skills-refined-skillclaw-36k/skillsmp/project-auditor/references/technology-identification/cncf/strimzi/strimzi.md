# Strimzi

**Category**: cncf
**Description**: Apache Kafka on Kubernetes
**Homepage**: https://strimzi.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### MAVEN
*Strimzi Java packages*

- `io.strimzi:strimzi-kafka-oauth` - OAuth support
- `io.strimzi:strimzi-api` - Strimzi API

#### GO
*Strimzi Go packages*

- `github.com/strimzi/strimzi-kafka-operator` - Kafka operator

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Strimzi usage*

- `kafka.yaml` - Kafka cluster definition
- `kafka-topic.yaml` - KafkaTopic
- `kafka-user.yaml` - KafkaUser
- `strimzi.yaml` - Strimzi deployment

### Code Patterns

**Pattern**: `strimzi\.io/|strimzi-`
- Strimzi annotations and naming
- Example: `strimzi.io/cluster: my-cluster`

**Pattern**: `kind:\s*(Kafka|KafkaTopic|KafkaUser|KafkaConnect|KafkaMirrorMaker|KafkaBridge|KafkaRebalance)`
- Strimzi CRD kinds
- Example: `kind: Kafka`

**Pattern**: `apiVersion:\s*kafka\.strimzi\.io/v[0-9]+`
- Strimzi API version
- Example: `apiVersion: kafka.strimzi.io/v1beta2`

**Pattern**: `kafka:|zookeeper:|entityOperator:|cruiseControl:`
- Kafka cluster spec sections
- Example: `kafka:\n  replicas: 3`

**Pattern**: `strimzi-cluster-operator|strimzi-kafka|strimzi-zookeeper`
- Strimzi component names
- Example: `strimzi-cluster-operator`

**Pattern**: `listeners:|authentication:|authorization:|config:`
- Kafka configuration sections
- Example: `listeners:\n  - name: plain`

**Pattern**: `tls:|plain:|scram-sha-512:|oauth:`
- Kafka authentication types
- Example: `authentication:\n  type: scram-sha-512`

**Pattern**: `topicName:|partitions:|replicas:|config:`
- KafkaTopic spec
- Example: `topicName: my-topic`

---

## Environment Variables

- `STRIMZI_NAMESPACE` - Strimzi namespace
- `STRIMZI_KAFKA_IMAGES` - Kafka images
- `STRIMZI_ZOOKEEPER_IMAGES` - ZooKeeper images

## Detection Notes

- Runs Apache Kafka on Kubernetes
- Manages Kafka, ZooKeeper, Connect
- KafkaUser for ACLs
- KafkaTopic for topic management
- Cruise Control for rebalancing

---

## Secrets Detection

### Credentials

#### Kafka User Credentials
**Pattern**: `authentication:\s*\n\s*type:\s*['"]?scram-sha-512['"]?`
**Severity**: high
**Description**: Kafka SCRAM authentication configured
**Multiline**: true

#### Kafka TLS Certificate
**Pattern**: `tls:\s*\n\s*trustedCertificates:`
**Severity**: high
**Description**: Kafka TLS certificate configuration
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Kafka Replicas Extraction

**Pattern**: `kafka:\s*\n\s*replicas:\s*([0-9]+)`
- Kafka broker replicas
- Extracts: `kafka_replicas`
- Example: `kafka:\n  replicas: 3`
**Multiline**: true

### Topic Partitions Extraction

**Pattern**: `partitions:\s*([0-9]+)`
- Topic partition count
- Extracts: `partitions`
- Example: `partitions: 12`

### Cluster Name Extraction

**Pattern**: `strimzi\.io/cluster:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Strimzi cluster name
- Extracts: `cluster_name`
- Example: `strimzi.io/cluster: my-cluster`
