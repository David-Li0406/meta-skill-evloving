# KEDA

**Category**: cncf
**Description**: Kubernetes Event-driven Autoscaling
**Homepage**: https://keda.sh

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*KEDA Go packages*

- `github.com/kedacore/keda/v2` - KEDA v2 core
- `github.com/kedacore/keda/v2/apis` - API types
- `github.com/kedacore/keda/v2/pkg` - Shared packages

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate KEDA usage*

- `scaledobject.yaml` - ScaledObject resource
- `scaledjob.yaml` - ScaledJob resource
- `triggerauthentication.yaml` - TriggerAuthentication
- `keda.yaml` - KEDA installation manifest

### Code Patterns

**Pattern**: `keda\.sh/|keda\.k8s\.io/`
- KEDA API groups
- Example: `apiVersion: keda.sh/v1alpha1`

**Pattern**: `kind:\s*(ScaledObject|ScaledJob|TriggerAuthentication|ClusterTriggerAuthentication)`
- KEDA CRD kinds
- Example: `kind: ScaledObject`

**Pattern**: `scaleTargetRef:|triggers:|pollingInterval:|cooldownPeriod:`
- ScaledObject spec fields
- Example: `scaleTargetRef:\n  name: my-deployment`

**Pattern**: `type:\s*(prometheus|kafka|rabbitmq|aws-sqs-queue|azure-queue|redis|mysql|postgresql|cron)`
- KEDA trigger types
- Example: `type: prometheus`

**Pattern**: `minReplicaCount:|maxReplicaCount:|idleReplicaCount:`
- KEDA scaling parameters
- Example: `minReplicaCount: 0`

**Pattern**: `metadata:\s*\n\s*(serverAddress|queueName|topicName|consumerGroup):`
- Trigger metadata fields
- Example: `serverAddress: http://prometheus:9090`

**Pattern**: `authenticationRef:|secretTargetRef:|podIdentity:`
- KEDA authentication configuration
- Example: `authenticationRef:\n  name: keda-trigger-auth`

**Pattern**: `keda-operator|keda-metrics-apiserver`
- KEDA component names
- Example: `keda-operator-metrics-apiserver`

**Pattern**: `external\.metrics\.k8s\.io|custom\.metrics\.k8s\.io`
- KEDA metrics APIs
- Example: `external.metrics.k8s.io/v1beta1`

---

## Environment Variables

- `KEDA_HTTP_DEFAULT_TIMEOUT` - HTTP default timeout
- `KEDA_SCALER_GLOBAL_HTTP_TIMEOUT` - Global scaler HTTP timeout
- `KEDA_LOG_LEVEL` - Log level
- `WATCH_NAMESPACE` - Namespace to watch

## Detection Notes

- ScaledObject for Deployments/StatefulSets
- ScaledJob for batch job scaling
- Scale to zero capability
- 60+ built-in scalers (Kafka, RabbitMQ, AWS, Azure, etc.)
- Integrates with Kubernetes HPA

---

## Secrets Detection

### Credentials

#### Trigger Authentication Secret
**Pattern**: `secretTargetRef:\s*\n\s*-\s*parameter:\s*['"]?([^\s'"]+)['"]?\s*\n\s*name:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: KEDA trigger authentication secret reference
**Multiline**: true

#### Connection String
**Pattern**: `connectionString(?:FromEnv)?:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Connection string for scalers (e.g., Azure, Redis)

---

## TIER 3: Configuration Extraction

### Min Replicas

**Pattern**: `minReplicaCount:\s*([0-9]+)`
- Minimum replica count
- Extracts: `min_replicas`
- Example: `minReplicaCount: 0`

### Max Replicas

**Pattern**: `maxReplicaCount:\s*([0-9]+)`
- Maximum replica count
- Extracts: `max_replicas`
- Example: `maxReplicaCount: 100`

### Polling Interval

**Pattern**: `pollingInterval:\s*([0-9]+)`
- Metric polling interval in seconds
- Extracts: `polling_interval`
- Example: `pollingInterval: 30`

### Cooldown Period

**Pattern**: `cooldownPeriod:\s*([0-9]+)`
- Scale down cooldown in seconds
- Extracts: `cooldown_period`
- Example: `cooldownPeriod: 300`

### Trigger Type

**Pattern**: `type:\s*['"]?([a-z0-9-]+)['"]?`
- Scaler trigger type
- Extracts: `trigger_type`
- Example: `type: kafka`
