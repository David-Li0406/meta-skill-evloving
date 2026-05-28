# OpenShift Cluster Health MCP Server

Model Context Protocol (MCP) server for OpenShift cluster health monitoring and AI Ops integration. Provides real-time cluster health data, incident management, and ML-powered anomaly detection through a standardized MCP interface.

![CI Status](https://github.com/openshift-aiops/openshift-cluster-health-mcp/workflows/CI/badge.svg)
[![Go Report Card](https://goreportcard.com/badge/github.com/openshift-aiops/openshift-cluster-health-mcp)](https://goreportcard.com/report/github.com/openshift-aiops/openshift-cluster-health-mcp)
![Branch Protection](https://img.shields.io/badge/branch-protected-green)

## Features

- **MCP Tools**: 7 tools for cluster operations and AI-powered analysis
  - `get-cluster-health` - Real-time cluster health snapshot
  - `list-pods` - Pod listing with advanced filtering
  - `list-incidents` - Active incident tracking via Coordination Engine
  - `trigger-remediation` - Automated remediation actions
  - `analyze-anomalies` - ML-powered anomaly detection via KServe
  - `get-model-status` - KServe model health monitoring
  - `predict-resource-usage` - Time-specific resource usage forecasting via ML models

- **MCP Resources**: 3 resources for passive data access
  - `cluster://health` - Real-time cluster health (10s cache)
  - `cluster://nodes` - Node information and capacity (30s cache)
  - `cluster://incidents` - Active incidents from Coordination Engine (5s cache)

- **Integrations**:
  - ✅ Kubernetes API (required)
  - ✅ Coordination Engine (optional - incident management)
  - ✅ KServe (optional - ML model serving)
  - ✅ Prometheus (optional - enhanced metrics)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  OpenShift Lightspeed / AI Assistant                    │
│  (MCP Client)                                           │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/SSE (MCP Protocol)
┌─────────────────▼───────────────────────────────────────┐
│  OpenShift Cluster Health MCP Server                    │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ MCP Tools   │  │ MCP Resources│  │ Cache (30s TTL)│ │
│  │ (7 total)   │  │ (3 total)    │  │                │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
└──────┬──────────────┬──────────────┬──────────────┬─────┘
       │              │              │              │
┌──────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐ ┌────▼────────┐
│ Kubernetes  │ │Coordination│ │   KServe    │ │ Prometheus  │
│ API         │ │ Engine     │ │  (ML Models)│ │   (Metrics) │
└─────────────┘ └──────────┘ └─────────────┘ └─────────────┘
```

## Version Compatibility

| OpenShift Version | Kubernetes Version | Container Image | Status |
|-------------------|-------------------|-----------------|--------|
| **4.18** | 1.31 | `quay.io/takinosh/openshift-cluster-health-mcp:4.18-latest` | ✅ Supported |
| **4.19** | 1.31 | `quay.io/takinosh/openshift-cluster-health-mcp:4.19-latest` | ✅ Supported |
| **4.20** | 1.33 | `quay.io/takinosh/openshift-cluster-health-mcp:4.20-latest` | ✅ Supported |

**📚 [Complete Installation Guide](./docs/INSTALLATION.md)** - Detailed instructions for installing the MCP server for each OpenShift version.

## Quick Start

### Prerequisites

- OpenShift 4.18+ (see version compatibility table above)
- Go 1.24+ (for local development)
- Helm 3.0+
- kubectl/oc CLI

### Local Development

```bash
# Clone repository
git clone https://github.com/openshift-aiops/openshift-cluster-health-mcp.git
cd openshift-cluster-health-mcp

# Install dependencies
go mod download

# Run tests
make test

# Build binary
make build

# Run locally (HTTP transport - default)
MCP_TRANSPORT=http ./bin/mcp-server

# Test with curl
curl http://localhost:8080/health
```

### Deploy to OpenShift

**Option 1: Use Pre-built Container Images (Recommended)**

```bash
# Determine your OpenShift version
oc version

# Install with Helm using the matching image tag
# The default service name is "mcp-server" on port 8080
helm install mcp-server ./charts/openshift-cluster-health-mcp \
  --namespace self-healing-platform \
  --create-namespace \
  --set image.repository=quay.io/takinosh/openshift-cluster-health-mcp \
  --set image.tag=4.20-latest  # Use 4.18-latest, 4.19-latest, or 4.20-latest

# Verify deployment
oc get pods -n self-healing-platform
oc logs -l app=mcp-server -n self-healing-platform

# Service endpoint: mcp-server.self-healing-platform.svc:8080
```

**Option 2: Build from Source**

```bash
# Build container image
make docker-build
oc new-build --name mcp-server --binary --strategy docker -n self-healing-platform
oc start-build mcp-server --from-dir=. --follow -n self-healing-platform

# Deploy with Helm
helm install mcp-server ./charts/openshift-cluster-health-mcp \
  --namespace self-healing-platform
```

**📖 For detailed installation instructions, version-specific configurations, and troubleshooting, see the [Installation Guide](./docs/INSTALLATION.md).**

**Option 3: Manual Deployment via GitHub Actions**

For pre-release validation or testing against real OpenShift clusters, use the manual deployment workflow:
- Navigate to [Actions → OpenShift Deploy](https://github.com/tosin2013/openshift-cluster-health-mcp/actions/workflows/openshift-deploy.yml)
- Provide your OpenShift server URL and authentication token
- Optionally deploy to your cluster after testing
- See [Manual OpenShift Deployment Guide](./docs/OPENSHIFT_MANUAL_DEPLOYMENT.md) for detailed instructions

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MCP_TRANSPORT` | Transport mode (http or stdio) | `http` | Yes |
| `MCP_HTTP_PORT` | HTTP server port | `8080` | If HTTP |
| `LOG_LEVEL` | Logging level (debug, info, warn, error) | `info` | No |
| `LOG_FORMAT` | Log format (json or text) | `json` | No |
| `ENABLE_COORDINATION_ENGINE` | Enable Coordination Engine integration | `false` | No |
| `COORDINATION_ENGINE_URL` | Coordination Engine endpoint | - | If CE enabled |
| `ENABLE_KSERVE` | Enable KServe integration | `false` | No |
| `KSERVE_NAMESPACE` | Namespace for KServe models | `self-healing-platform` | If KServe enabled |
| `KSERVE_PREDICTOR_PORT` | KServe predictor port (8080 for RawDeployment, 80 for Serverless) | `8080` | No |
| `ENABLE_PROMETHEUS` | Enable Prometheus integration | `false` | No |
| `PROMETHEUS_URL` | Prometheus endpoint | - | If Prom enabled |

### Helm Values

See `charts/openshift-cluster-health-mcp/values.yaml` for full configuration options.

**Key configurations**:

```yaml
# Enable all integrations (dev example)
integrations:
  coordinationEngine:
    enabled: true
    url: http://coordination-engine:8080

  kserve:
    enabled: true
    namespace: self-healing-platform

  prometheus:
    enabled: true
    url: https://prometheus-k8s.openshift-monitoring.svc:9091

# Security context (OpenShift compatible)
podSecurityContext:
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault
```

## Usage

### HTTP Endpoints

```bash
# Health check
curl http://localhost:8080/health

# List available tools
curl http://localhost:8080/mcp/tools

# List available resources
curl http://localhost:8080/mcp/resources

# Get cluster health resource
curl http://localhost:8080/mcp/resources/cluster/health

# Execute tool
curl -X POST http://localhost:8080/mcp/tools/get-cluster-health \
  -H 'Content-Type: application/json' \
  -d '{}'
```

### MCP Client Integration

```typescript
// Example: Connect to MCP server
// Service URL: mcp-server.self-healing-platform.svc:8080
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const transport = new SSEClientTransport(
  new URL("http://mcp-server.self-healing-platform.svc:8080/mcp/sse")
);

const client = new Client({
  name: "openshift-lightspeed",
  version: "1.0.0"
}, {
  capabilities: {}
});

await client.connect(transport);

// List tools
const tools = await client.listTools();
console.log("Available tools:", tools);

// Execute tool
const result = await client.callTool({
  name: "get-cluster-health",
  arguments: {}
});
console.log("Cluster health:", result);
```

### Analyze Anomalies Tool

The `analyze-anomalies` tool performs ML-powered anomaly detection on Prometheus metrics. It supports filtering by namespace, deployment, pod, or label selector for targeted analysis.

**Input Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `metric` | string | Yes | The metric name to analyze (e.g., `cpu_usage`, `memory_usage`, `pod_restarts`). |
| `namespace` | string | No | Kubernetes namespace to scope the analysis. |
| `deployment` | string | No | Specific deployment name to filter anomalies for. Mutually exclusive with `pod`. |
| `pod` | string | No | Specific pod name to filter anomalies for (e.g., `etcd-0`, `prometheus-k8s-0`). Mutually exclusive with `deployment`. |
| `label_selector` | string | No | Kubernetes label selector to filter pods (e.g., `app=flask`). Cannot combine with `deployment` or `pod`. |
| `time_range` | string | No | Time range for analysis: `1h`, `6h`, `24h`, `7d` (default: `1h`). |
| `threshold` | number | No | Anomaly score threshold 0.0-1.0 (default: `0.7`). |
| `model_name` | string | No | KServe model name (default: `predictive-analytics`). |

**Example Usage**:

```bash
# Analyze CPU anomalies in a specific deployment
curl -X POST http://localhost:8080/mcp/tools/analyze-anomalies/call \
  -H 'Content-Type: application/json' \
  -H 'X-MCP-Session-ID: <session-id>' \
  -d '{
    "metric": "cpu_usage",
    "deployment": "sample-flask-app",
    "namespace": "self-healing-platform",
    "time_range": "24h"
  }'

# Analyze memory anomalies in etcd pods
curl -X POST http://localhost:8080/mcp/tools/analyze-anomalies/call \
  -H 'Content-Type: application/json' \
  -H 'X-MCP-Session-ID: <session-id>' \
  -d '{
    "metric": "memory_usage",
    "pod": "etcd-0",
    "namespace": "openshift-etcd"
  }'

# Analyze anomalies using label selector
curl -X POST http://localhost:8080/mcp/tools/analyze-anomalies/call \
  -H 'Content-Type: application/json' \
  -H 'X-MCP-Session-ID: <session-id>' \
  -d '{
    "metric": "cpu_usage",
    "label_selector": "app=monitoring",
    "time_range": "6h"
  }'
```

**Example Response**:

```json
{
  "status": "success",
  "metric": "cpu_usage",
  "time_range": "24h",
  "namespace": "self-healing-platform",
  "deployment": "sample-flask-app",
  "filter_target": "deployment 'sample-flask-app' in namespace 'self-healing-platform'",
  "model_used": "predictive-analytics",
  "anomalies": [
    {
      "timestamp": "2026-01-13T14:30:00Z",
      "metric_name": "cpu_usage",
      "value": 95.5,
      "anomaly_score": 0.89,
      "confidence": 0.92,
      "severity": "high",
      "explanation": "Metric 'cpu_usage' shows high anomaly (score: 0.89, confidence: 0.92)."
    }
  ],
  "anomaly_count": 1,
  "max_score": 0.89,
  "average_score": 0.89,
  "message": "Detected 1 anomalies in cpu_usage for deployment 'sample-flask-app' in namespace 'self-healing-platform' over the last 24h (max score: 0.89)",
  "recommendation": "WARNING: Monitor closely. 1 anomalies detected in cpu_usage."
}
```

### Predict Resource Usage Tool

The `predict-resource-usage` tool enables time-specific resource usage forecasting using ML models. It supports predictions for pods, deployments, namespaces, or cluster-wide infrastructure.

**Input Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `target_time` | string | No | Target time in HH:MM format (24-hour). Defaults to current time + 1 hour. |
| `target_date` | string | No | Target date in YYYY-MM-DD format. Defaults to today. |
| `namespace` | string | No | Kubernetes namespace to scope the prediction. Supports wildcards (e.g., `openshift-*`). |
| `deployment` | string | No | Specific deployment name for prediction. |
| `pod` | string | No | Specific pod name for prediction. |
| `metric` | string | No | Metric type: `cpu_usage`, `memory_usage`, or `both` (default). |
| `scope` | string | No | Prediction scope: `pod`, `deployment`, `namespace` (default), or `cluster`. |

**Example Usage**:

```bash
# Predict CPU usage at 3 PM today for a namespace
curl -X POST http://localhost:8080/mcp/tools/predict-resource-usage/call \
  -H 'Content-Type: application/json' \
  -H 'X-MCP-Session-ID: <session-id>' \
  -d '{
    "target_time": "15:00",
    "namespace": "self-healing-platform",
    "metric": "cpu_usage",
    "scope": "namespace"
  }'

# Predict memory usage for tomorrow morning
curl -X POST http://localhost:8080/mcp/tools/predict-resource-usage/call \
  -H 'Content-Type: application/json' \
  -H 'X-MCP-Session-ID: <session-id>' \
  -d '{
    "target_time": "09:00",
    "target_date": "2026-01-14",
    "namespace": "openshift-monitoring",
    "metric": "memory_usage"
  }'

# Cluster-wide prediction
curl -X POST http://localhost:8080/mcp/tools/predict-resource-usage/call \
  -H 'Content-Type: application/json' \
  -H 'X-MCP-Session-ID: <session-id>' \
  -d '{
    "target_time": "00:00",
    "scope": "cluster",
    "metric": "both"
  }'
```

**Example Response**:

```json
{
  "status": "success",
  "scope": "namespace",
  "target": "self-healing-platform",
  "current_metrics": {
    "cpu_percent": 68.2,
    "memory_percent": 74.5,
    "timestamp": "2026-01-13T14:30:00Z"
  },
  "predicted_metrics": {
    "cpu_percent": 74.5,
    "memory_percent": 81.2,
    "target_time": "2026-01-13T15:00:00Z",
    "confidence": 0.92
  },
  "trend": "upward",
  "recommendation": "Memory approaching 85% threshold. Consider monitoring or scaling.",
  "model_used": "predictive-analytics",
  "model_version": "v1"
}
```

## Development

### Project Structure

```
openshift-cluster-health-mcp/
├── cmd/
│   └── mcp-server/          # Main entry point
├── internal/
│   ├── server/              # HTTP server and MCP protocol handling
│   ├── tools/               # MCP tool implementations
│   └── resources/           # MCP resource implementations
├── pkg/
│   ├── clients/             # External API clients (K8s, CE, KServe)
│   └── cache/               # Caching layer
├── charts/
│   └── openshift-cluster-health-mcp/  # Helm chart
├── .github/
│   └── workflows/           # GitHub Actions CI/CD
├── docs/
│   └── adrs/                # Architecture Decision Records
└── test/                    # Test files
```

### Running Tests

```bash
# Unit tests
make test

# Unit tests with coverage
make test-coverage

# Lint code
make lint

# Security scan
make security-scan
```

### Build Options

```bash
# Local development build
make build

# Production build (optimized)
make build-prod

# Docker build
make docker-build

# Multi-arch build
make docker-buildx
```

## Production Deployment

### Security Considerations

- **RBAC**: ServiceAccount with minimal ClusterRole permissions (read-only)
- **Security Context**: Runs as nonroot user with read-only filesystem
- **Network Policies**: Optional network isolation
- **Image**: Based on Red Hat UBI 9 Micro (minimal attack surface)

### High Availability

```yaml
# Helm values for HA deployment
replicaCount: 2

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: mcp-server
        topologyKey: kubernetes.io/hostname
```

### Monitoring

The server exposes Prometheus metrics at `/metrics`:

- `mcp_tools_total` - Total tool executions
- `mcp_tools_errors_total` - Tool execution errors
- `mcp_resources_requests_total` - Resource access requests
- `mcp_cache_hits_total` - Cache hits
- `mcp_cache_misses_total` - Cache misses

## Troubleshooting

### Common Issues

**Pods not starting (SCC violations)**:
```bash
# Check security context constraints
oc get pods -n self-healing-platform -o yaml | grep -A 10 securityContext

# Ensure podSecurityContext.runAsUser is not set (let OpenShift assign)
```

**Integration failures**:
```bash
# Check logs
oc logs -l app=mcp-server -n self-healing-platform

# Verify service connectivity
oc exec -n self-healing-platform <pod-name> -- curl -I http://coordination-engine:8080/health
```

**Cache issues**:
```bash
# Check cache statistics in logs
oc logs <pod-name> | grep -i cache
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](.github/CONTRIBUTING.md) for detailed information on:

- Development setup and prerequisites
- Branch strategy and protection rules
- Pull request process and requirements
- Code review requirements
- Testing guidelines
- Commit message format

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch from `main` (`git checkout -b feature/amazing-feature`)
3. Make your changes following our [code style guidelines](.github/CONTRIBUTING.md#code-style-guidelines)
4. Run tests and linters locally (`make test && make lint`)
5. Commit your changes using [Conventional Commits](.github/CONTRIBUTING.md#commit-message-format)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request using our [PR template](.github/PULL_REQUEST_TEMPLATE.md)

**Branch Protection**: All main and release branches are protected. See [Branch Protection Rules](docs/BRANCH_PROTECTION.md) for details.

## License

Apache License 2.0

## Support

- Issues: [GitHub Issues](https://github.com/openshift-aiops/openshift-cluster-health-mcp/issues)
- Discussions: [GitHub Discussions](https://github.com/openshift-aiops/openshift-cluster-health-mcp/discussions)
- Documentation: [docs/](./docs/)

## Acknowledgments

- Built on the [Model Context Protocol](https://modelcontextprotocol.io/)
- Integrates with [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift)
- Powered by [KServe](https://kserve.github.io/website/) for ML inference
