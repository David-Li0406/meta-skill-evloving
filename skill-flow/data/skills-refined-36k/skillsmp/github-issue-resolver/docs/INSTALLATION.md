# Installation Guide

This guide explains how to install the OpenShift Cluster Health MCP Server for different OpenShift versions.

## Version Compatibility

The MCP server is released with version-specific container images to ensure compatibility with your OpenShift cluster:

| OpenShift Version | Kubernetes Version | Container Image Tag | Branch |
|-------------------|-------------------|---------------------|--------|
| **OpenShift 4.18** | Kubernetes 1.31 | `4.18-latest` | `release-4.18` |
| **OpenShift 4.19** | Kubernetes 1.31 | `4.19-latest` | `release-4.19` |
| **OpenShift 4.20** | Kubernetes 1.33 | `4.20-latest` | `release-4.20` |

**Important**: Always use the container image that matches your OpenShift cluster version to avoid API compatibility issues.

## Installation Methods

### Method 1: Helm Chart (Recommended)

#### 1. Determine Your OpenShift Version

```bash
oc version
# Example output:
# Client Version: 4.20.0
# Kubernetes Version: v1.33.7
# Server Version: 4.20.0
```

#### 2. Add Version-Specific Values

Create a `values-<version>.yaml` file:

**For OpenShift 4.18:**
```yaml
# values-4.18.yaml
image:
  repository: quay.io/takinosh/openshift-cluster-health-mcp
  tag: "4.18-latest"
  pullPolicy: Always

replicaCount: 1

env:
  MCP_TRANSPORT: "http"
  MCP_HTTP_PORT: "8080"
  CACHE_TTL: "30s"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

**For OpenShift 4.19:**
```yaml
# values-4.19.yaml
image:
  repository: quay.io/takinosh/openshift-cluster-health-mcp
  tag: "4.19-latest"
  pullPolicy: Always

replicaCount: 1

env:
  MCP_TRANSPORT: "http"
  MCP_HTTP_PORT: "8080"
  CACHE_TTL: "30s"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

**For OpenShift 4.20:**
```yaml
# values-4.20.yaml
image:
  repository: quay.io/takinosh/openshift-cluster-health-mcp
  tag: "4.20-latest"
  pullPolicy: Always

replicaCount: 1

env:
  MCP_TRANSPORT: "http"
  MCP_HTTP_PORT: "8080"
  CACHE_TTL: "30s"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

#### 3. Install with Helm

```bash
# Create namespace
oc new-project self-healing-platform

# Install the chart (replace 4.20 with your version)
# Default service name: mcp-server on port 8080
helm install mcp-server \
  ./charts/openshift-cluster-health-mcp \
  --namespace self-healing-platform \
  --values values-4.20.yaml

# Verify installation
oc get pods -n self-healing-platform
oc logs -l app=mcp-server -n self-healing-platform

# Service endpoint: mcp-server.self-healing-platform.svc:8080
```

#### 4. Test the Deployment

```bash
# Port-forward to access the server
oc port-forward -n self-healing-platform svc/mcp-server 8080:8080

# In another terminal, test the endpoints
curl http://localhost:8080/health
curl http://localhost:8080/mcp/info
curl http://localhost:8080/mcp/tools
```

### Method 2: Container Deployment (Standalone)

For testing or non-Helm deployments:

#### OpenShift 4.20 Example

```bash
# Create deployment
oc new-project self-healing-platform

cat <<EOF | oc apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
  namespace: self-healing-platform
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      serviceAccountName: mcp-server
      containers:
      - name: mcp-server
        image: quay.io/takinosh/openshift-cluster-health-mcp:4.20-latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
          protocol: TCP
        env:
        - name: MCP_TRANSPORT
          value: "http"
        - name: MCP_HTTP_PORT
          value: "8080"
        - name: CACHE_TTL
          value: "30s"
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 128Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-server
  namespace: self-healing-platform
spec:
  selector:
    app: mcp-server
  ports:
  - port: 8080
    targetPort: 8080
    protocol: TCP
EOF

# Service endpoint: mcp-server.self-healing-platform.svc:8080
```

### Method 3: Local Development

For development with version-specific dependencies:

```bash
# Clone the repository
git clone https://github.com/tosin2013/openshift-cluster-health-mcp.git
cd openshift-cluster-health-mcp

# Check out the branch matching your OpenShift version
git checkout release-4.20  # Or release-4.18, release-4.19

# Install dependencies
go mod download

# Build
make build

# Run locally with your cluster's kubeconfig
export KUBECONFIG=~/.kube/config
MCP_TRANSPORT=http ./bin/mcp-server

# In another terminal, test
curl http://localhost:8080/health
```

## RBAC Requirements

The MCP server requires the following permissions (automatically created by Helm):

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: mcp-server-reader
rules:
- apiGroups: [""]
  resources: ["nodes", "pods", "namespaces"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["serving.kserve.io"]
  resources: ["inferenceservices"]
  verbs: ["get", "list"]
```

## Optional Integrations

### Enable Coordination Engine (Incident Management)

Add to your `values.yaml`:

```yaml
env:
  ENABLE_COORDINATION_ENGINE: "true"
  COORDINATION_ENGINE_URL: "http://coordination-engine:8080"
```

### Enable KServe (ML Anomaly Detection)

Add to your `values.yaml`:

```yaml
env:
  ENABLE_KSERVE: "true"
  KSERVE_NAMESPACE: "self-healing-platform"
  KSERVE_PREDICTOR_PORT: "8080"  # 8080 for RawDeployment mode, 80 for Serverless mode
```

### Enable Prometheus (Enhanced Metrics)

Add to your `values.yaml`:

```yaml
env:
  ENABLE_PROMETHEUS: "true"
  PROMETHEUS_URL: "https://prometheus-k8s.openshift-monitoring.svc:9091"
```

## Upgrading Between OpenShift Versions

When upgrading your OpenShift cluster, update the MCP server container image:

```bash
# Upgrade from 4.19 to 4.20
helm upgrade mcp-server \
  ./charts/openshift-cluster-health-mcp \
  --namespace self-healing-platform \
  --reuse-values \
  --set image.tag=4.20-latest

# Verify the new version
oc get pods -n self-healing-platform
oc describe pod -l app=mcp-server -n self-healing-platform | grep Image:
```

## Verification

After installation, verify the server is working:

```bash
# Check pod status
oc get pods -n self-healing-platform

# Check logs
oc logs -l app=mcp-server -n self-healing-platform

# Port-forward and test endpoints
oc port-forward -n self-healing-platform svc/mcp-server 8080:8080

# Test health endpoint
curl http://localhost:8080/health
# Expected: {"status":"ok"}

# Test MCP info
curl http://localhost:8080/mcp/info
# Expected: Server info with version and capabilities

# Test MCP tools
curl http://localhost:8080/mcp/tools
# Expected: List of 6 available tools

# Test cluster health tool
curl -X POST http://localhost:8080/mcp/tools/get-cluster-health \
  -H 'Content-Type: application/json' \
  -d '{}'
# Expected: Cluster health data with nodes, pods, etc.
```

## Troubleshooting

### Pod CrashLoopBackOff

```bash
# Check logs
oc logs -l app=mcp-server -n self-healing-platform --previous

# Common issues:
# 1. Wrong image tag for your OpenShift version
# 2. Missing RBAC permissions
# 3. Invalid kubeconfig (in-cluster auth should work automatically)
```

### API Compatibility Errors

```bash
# Symptoms: Errors like "unknown field" or "unsupported API version"
# Solution: Ensure image tag matches your OpenShift version

# Check your cluster version
oc version

# Update Helm values with correct image tag
helm upgrade mcp-server \
  ./charts/openshift-cluster-health-mcp \
  --namespace self-healing-platform \
  --set image.tag=4.20-latest  # Match your version
```

### Connection Refused / Timeout

```bash
# Check service and endpoints
oc get svc,endpoints -n self-healing-platform

# Check pod networking
oc get pods -n self-healing-platform -o wide

# Check security policies
oc get networkpolicies -n self-healing-platform
```

## Next Steps

After successful installation:

1. **Integrate with OpenShift Lightspeed**: Configure Lightspeed to connect to the MCP server endpoint
2. **Enable Optional Integrations**: Set up Coordination Engine and/or KServe if needed
3. **Configure Monitoring**: Set up metrics and alerting for the MCP server
4. **Review Documentation**: Check `/docs` for advanced configuration options

## Support

- **Issues**: https://github.com/tosin2013/openshift-cluster-health-mcp/issues
- **Documentation**: https://github.com/tosin2013/openshift-cluster-health-mcp/tree/main/docs
- **Container Images**: https://quay.io/repository/takinosh/openshift-cluster-health-mcp
