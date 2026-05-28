---
name: observability
title: Observability Stack
description: ASU's observability stack for monitoring, logging, and tracing
subtypes:
  - datadog
  - logging-lake
  - cloudwatch
  - opentelemetry
  - splunk
---

# Observability Stack

ASU's observability stack for monitoring, logging, and tracing.
Primary tools: Datadog (APM/RUM), Cribl/Logging Lake (logs),
CloudWatch (AWS metrics), OpenTelemetry (K8s).

**WARNING: Splunk is DEPRECATED - use Logging Lake instead**

## Datadog

### TypeScript/Node.js APM

**Package**: dd-trace
**Example**: ASU/lms-canvas-enrollment-system

```typescript
import tracer from 'dd-trace';
tracer.init({ service: 'my-service' });
```

### TypeScript/React RUM

**Package**: @datadog/browser-rum
**Example**: ASU/cremo-cmidp-course-requisite-api (frontend)

```typescript
import { datadogRum } from '@datadog/browser-rum';
datadogRum.init({
  applicationId: 'xxx',
  clientToken: 'xxx',
  site: 'datadoghq.com',
  service: 'my-app',
  env: process.env.NODE_ENV
});
```

### Python APM

**Package**: ddtrace
**Example**: ASU/iden-universal-service-provisioner

```python
from ddtrace import tracer
@tracer.wrap(service='my-service')
def my_function():
    pass
```

### Java APM

**Agent**: dd-java-agent.jar
**Example**: ASU/edna

```bash
java -javaagent:/path/to/dd-java-agent.jar \
     -Ddd.service=my-service \
     -Ddd.env=prod \
     -jar app.jar
```

### Jenkins Deployment Events

**Function**: datadogDeployment()
**Repo**: ASU/devops-jenkins-pipeline-library

```groovy
datadogDeployment(
  serviceName: 'my-service',
  env: 'prod'
)
```

## Logging Lake

**This is the RECOMMENDED destination for all logs.**

### Architecture

```
Cribl Stream (EKS) → S3 → OpenSearch
OSIS (OpenSearch Ingestion Service) pipelines
```

### Key Repositories

| Repo | Purpose |
|------|---------|
| ASU/eli5-observability-pipeline-platform | Platform |
| ASU/eli5-kafkabahn | Kafka Bridge |
| ASU/eli5-osis-pipelines | OSIS pipelines |

**Team Prefix**: eli5

### Terraform Modules

| Module | Description |
|--------|-------------|
| cloudwatch-logs-to-log-lake | CloudWatch to S3 data lake |
| cloudflare-zone-logpush-logging-lake | Cloudflare to data lake |

### Migration from Splunk

1. Update log shippers to point to Cribl
2. Use OSIS pipelines for OpenSearch ingestion
3. Decommission Splunk forwarders

## CloudWatch

### Alarm Patterns
- Lambda errors
- API Gateway 5xx
- ECS task failures

### Routing Options

| Destination | Module | Status |
|-------------|--------|--------|
| Datadog | cloudwatch-logs-to-datadog | Active |
| Logging Lake | cloudwatch-logs-to-log-lake | Active |
| Splunk | cloudwatch-to-splunk | **DEPRECATED** |

### Terraform Modules

```
Source: jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform
```

- cloudwatch-logs-to-datadog
- cloudwatch-logs-to-log-lake
- datadog-lambda-forwarder
- datadog-logs-firehose-forwarder

## OpenTelemetry

### Architecture

```
K8s OTEL Collector → OSIS → OpenSearch
```

### Use Cases
- Kubernetes workloads on EKS
- Vendor-neutral instrumentation
- Custom metrics and traces

### Integration Points
- OSIS pipelines (ASU/eli5-osis-pipelines)
- OpenSearch dashboards

**Note**: For APM, Datadog is preferred for most use cases.
Use OTEL when vendor neutrality is required.

## Splunk

**WARNING: SPLUNK IS DEPRECATED**

Splunk is being phased out at ASU.
All new implementations MUST use Logging Lake instead.

### Migration Path

```
FROM: Splunk Universal Forwarder / HEC
TO:   Cribl Stream → S3 → OpenSearch
```

### Steps to Migrate

1. Identify current Splunk sources
2. Configure Cribl Stream inputs
3. Update Terraform to use cloudwatch-logs-to-log-lake
4. Migrate dashboards to OpenSearch
5. Decommission Splunk forwarders

### Contact

**Team**: eli5 (Enterprise Logging Infrastructure)
**Repo**: ASU/eli5-observability-pipeline-platform

## Terraform Modules Summary

| Module | Description |
|--------|-------------|
| cloudwatch-logs-to-datadog | CloudWatch to Datadog |
| cloudwatch-logs-to-log-lake | CloudWatch to S3 data lake |
| datadog-lambda-forwarder | Datadog Lambda forwarder |
| datadog-logs-firehose-forwarder | Datadog Kinesis Firehose |

## Related Commands

```bash
discover.sh pattern --name observability --type datadog
discover.sh pattern --name observability --type logging-lake
discover.sh pattern --name observability --type cloudwatch
discover.sh pattern --name observability --type opentelemetry
discover.sh pattern --name observability --type splunk
```
