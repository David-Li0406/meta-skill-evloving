# ADR-007: RBAC-Based Security Model

## Status

**ACCEPTED** - 2025-12-09

## Context

The OpenShift Cluster Health MCP Server requires access to cluster resources (nodes, pods, events) and external services (Prometheus, KServe) to fulfill its operational responsibilities. Security must be implemented following Kubernetes RBAC (Role-Based Access Control) principles while maintaining the principle of least privilege.

### Security Requirements

1. **Principle of Least Privilege**: Grant only necessary permissions
2. **Read-Only Access**: No write operations to cluster resources (except KServe predictions)
3. **Namespace Isolation**: Respect namespace boundaries where applicable
4. **ServiceAccount Authentication**: Use Kubernetes-native authentication
5. **OpenShift SCC Compliance**: Meet OpenShift Security Context Constraints
6. **No Hardcoded Credentials**: All credentials from Kubernetes Secrets or ServiceAccount tokens

### Current OpenShift Cluster Environment

- **OpenShift Version**: 4.18.21
- **Kubernetes Version**: v1.31.10
- **Security Features**: RBAC, SCC, Network Policies, Pod Security Standards
- **Installed Operators**: GPU, OpenShift AI, Serverless, Service Mesh, GitOps, Pipelines

### Access Requirements

| Resource | API Group | Operations | Scope | Rationale |
|----------|-----------|------------|-------|-----------|
| **Nodes** | core/v1 | get, list, watch | Cluster | Cluster health monitoring |
| **Pods** | core/v1 | get, list, watch | All namespaces | Pod health status |
| **Events** | core/v1 | get, list, watch | All namespaces | Diagnostic information |
| **Namespaces** | core/v1 | get, list | Cluster | Namespace enumeration |
| **Deployments** | apps/v1 | get, list, watch | All namespaces | Workload status |
| **StatefulSets** | apps/v1 | get, list, watch | All namespaces | Workload status |
| **InferenceServices** | serving.kserve.io/v1beta1 | get, list, watch | Specific namespace | KServe model status |
| **Prometheus** | monitoring.coreos.com/v1 | get (via HTTP) | openshift-monitoring | Metrics querying |

## Decision

We will implement a **RBAC-based security model** using Kubernetes ServiceAccounts, ClusterRoles, and RoleBindings. The MCP server will run with minimal, read-only permissions and use ServiceAccount tokens for authentication.

### Core Security Principles

1. **ServiceAccount per Deployment**: Dedicated ServiceAccount for MCP server
2. **ClusterRole for Cluster-Wide Read**: Read-only access to cluster resources
3. **RoleBinding for KServe**: Namespace-specific access to InferenceServices
4. **Non-Root User**: Run as UID 1000 (non-root)
5. **Read-Only Filesystem**: Immutable container filesystem
6. **No Privilege Escalation**: Drop all capabilities

## Implementation

### 1. ServiceAccount

```yaml
# charts/openshift-cluster-health-mcp/templates/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cluster-health-mcp
  namespace: {{ .Values.namespace }}
  labels:
    app: cluster-health-mcp
automountServiceAccountToken: true
```

### 2. ClusterRole (Read-Only Cluster Resources)

```yaml
# charts/openshift-cluster-health-mcp/templates/clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-health-mcp-reader
rules:
  # Core Kubernetes resources (read-only)
  - apiGroups: [""]
    resources:
      - nodes
      - nodes/status
      - pods
      - pods/status
      - pods/log
      - events
      - namespaces
      - services
      - configmaps
    verbs: ["get", "list", "watch"]

  # Deployments and workloads (read-only)
  - apiGroups: ["apps"]
    resources:
      - deployments
      - deployments/status
      - statefulsets
      - statefulsets/status
      - replicasets
      - replicasets/status
    verbs: ["get", "list", "watch"]

  # Metrics (for resource calculations)
  - apiGroups: ["metrics.k8s.io"]
    resources:
      - nodes
      - pods
    verbs: ["get", "list"]
```

### 3. ClusterRoleBinding

```yaml
# charts/openshift-cluster-health-mcp/templates/clusterrolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-health-mcp-reader
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-health-mcp-reader
subjects:
  - kind: ServiceAccount
    name: cluster-health-mcp
    namespace: {{ .Values.namespace }}
```

### 4. Role (KServe InferenceServices - Namespace-Scoped)

```yaml
# charts/openshift-cluster-health-mcp/templates/role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: cluster-health-mcp-kserve
  namespace: {{ .Values.kserve.namespace }}
rules:
  # KServe InferenceServices (read-only)
  - apiGroups: ["serving.kserve.io"]
    resources:
      - inferenceservices
      - inferenceservices/status
    verbs: ["get", "list", "watch"]

  # ServingRuntimes (for model serving metadata)
  - apiGroups: ["serving.kserve.io"]
    resources:
      - servingruntimes
    verbs: ["get", "list"]
```

### 5. RoleBinding (KServe Access)

```yaml
# charts/openshift-cluster-health-mcp/templates/rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cluster-health-mcp-kserve
  namespace: {{ .Values.kserve.namespace }}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: cluster-health-mcp-kserve
subjects:
  - kind: ServiceAccount
    name: cluster-health-mcp
    namespace: {{ .Values.namespace }}
```

### 6. Prometheus Access (via Service)

For Prometheus metrics, we need access to the `prometheus-k8s` service in `openshift-monitoring`:

```yaml
# charts/openshift-cluster-health-mcp/templates/prometheus-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: cluster-health-mcp-prometheus
  namespace: openshift-monitoring
rules:
  # Access to Prometheus service endpoints
  - apiGroups: [""]
    resources:
      - services/prometheus-k8s
    resourceNames:
      - prometheus-k8s
    verbs: ["get"]

  # Query Prometheus API via service proxy
  - apiGroups: [""]
    resources:
      - services
    resourceNames:
      - prometheus-k8s
    verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cluster-health-mcp-prometheus
  namespace: openshift-monitoring
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: cluster-health-mcp-prometheus
subjects:
  - kind: ServiceAccount
    name: cluster-health-mcp
    namespace: {{ .Values.namespace }}
```

### 7. Security Context (Pod-Level)

```yaml
# charts/openshift-cluster-health-mcp/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-health-mcp
spec:
  template:
    spec:
      serviceAccountName: cluster-health-mcp
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: mcp-server
        image: quay.io/openshift-aiops/cluster-health-mcp:0.1.0
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
              - ALL

        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /cache

      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
```

### 8. Network Policy

Restrict ingress to only OpenShift Lightspeed and egress to required services:

```yaml
# charts/openshift-cluster-health-mcp/templates/networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cluster-health-mcp
  namespace: {{ .Values.namespace }}
spec:
  podSelector:
    matchLabels:
      app: cluster-health-mcp

  policyTypes:
  - Ingress
  - Egress

  # Allow ingress only from OpenShift Lightspeed
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: openshift-lightspeed
    ports:
    - protocol: TCP
      port: 8080

  # Allow egress to required services
  egress:
  # Kubernetes API server
  - to:
    - namespaceSelector:
        matchLabels:
          name: default
    ports:
    - protocol: TCP
      port: 443

  # Prometheus
  - to:
    - namespaceSelector:
        matchLabels:
          name: openshift-monitoring
    ports:
    - protocol: TCP
      port: 9091

  # Coordination Engine (if enabled)
  - to:
    - namespaceSelector:
        matchLabels:
          name: {{ .Values.coordinationEngine.namespace }}
    ports:
    - protocol: TCP
      port: 8080

  # KServe models (if enabled)
  - to:
    - namespaceSelector:
        matchLabels:
          name: {{ .Values.kserve.namespace }}
    ports:
    - protocol: TCP
      port: 8080

  # DNS resolution
  - to:
    - namespaceSelector:
        matchLabels:
          name: openshift-dns
    ports:
    - protocol: UDP
      port: 53
```

## OpenShift Security Context Constraints (SCC)

OpenShift requires pods to comply with Security Context Constraints. The `restricted-v2` SCC is sufficient for our use case:

```yaml
# No custom SCC needed - use default restricted-v2
# The ServiceAccount will automatically use restricted-v2 SCC

# Verify SCC assignment:
# oc get pod <pod-name> -o jsonpath='{.metadata.annotations.openshift\.io/scc}'
# Expected: restricted-v2
```

**restricted-v2 SCC provides**:
- ✅ Non-root user enforcement
- ✅ No privilege escalation
- ✅ Read-only root filesystem
- ✅ Dropped capabilities

## Authentication and Authorization Flow

### 1. In-Cluster Authentication (Production)

```go
// pkg/clients/kubernetes.go
func NewK8sClient() (*K8sClient, error) {
    // Load ServiceAccount token from:
    // /var/run/secrets/kubernetes.io/serviceaccount/token
    config, err := rest.InClusterConfig()
    if err != nil {
        return nil, err
    }

    // Token automatically included in all API requests
    clientset, err := kubernetes.NewForConfig(config)
    return &K8sClient{clientset: clientset}, nil
}
```

**Token Location**: `/var/run/secrets/kubernetes.io/serviceaccount/token`
**CA Certificate**: `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`
**Namespace**: `/var/run/secrets/kubernetes.io/serviceaccount/namespace`

### 2. Local Development Authentication

```go
// Local development uses KUBECONFIG
func NewK8sClient() (*K8sClient, error) {
    // Try in-cluster first
    config, err := rest.InClusterConfig()
    if err != nil {
        // Fallback to local kubeconfig
        kubeconfig := os.Getenv("KUBECONFIG")
        if kubeconfig == "" {
            kubeconfig = filepath.Join(os.Getenv("HOME"), ".kube", "config")
        }
        config, err = clientcmd.BuildConfigFromFlags("", kubeconfig)
        if err != nil {
            return nil, err
        }
    }

    clientset, err := kubernetes.NewForConfig(config)
    return &K8sClient{clientset: clientset}, nil
}
```

### 3. Prometheus Authentication

```go
// pkg/clients/prometheus.go
func NewPromClient(config PromConfig) *PromClient {
    // Read ServiceAccount token
    tokenBytes, err := os.ReadFile("/var/run/secrets/kubernetes.io/serviceaccount/token")
    if err != nil {
        log.Warn("Failed to read ServiceAccount token", "error", err)
        return &PromClient{enabled: false}
    }

    return &PromClient{
        baseURL: config.URL,
        token:   string(tokenBytes),
        httpClient: &http.Client{
            Timeout: 5 * time.Second,
            Transport: &http.Transport{
                TLSClientConfig: &tls.Config{
                    // Trust OpenShift CA
                    RootCAs: loadOpenShiftCA(),
                },
            },
        },
    }
}

func (c *PromClient) Query(ctx context.Context, query string) (*QueryResult, error) {
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", c.token))

    resp, err := c.httpClient.Do(req)
    // ... handle response
}
```

## Secret Management

### Secrets for External Integrations

```yaml
# charts/openshift-cluster-health-mcp/templates/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: cluster-health-mcp-secrets
  namespace: {{ .Values.namespace }}
type: Opaque
stringData:
  # Optional: External API keys (if needed)
  coordination-engine-api-key: {{ .Values.coordinationEngine.apiKey | default "" }}
```

**Mounting Secrets**:
```yaml
env:
- name: COORDINATION_ENGINE_API_KEY
  valueFrom:
    secretKeyRef:
      name: cluster-health-mcp-secrets
      key: coordination-engine-api-key
      optional: true
```

## Audit Logging

Enable Kubernetes audit logging for MCP server actions:

```yaml
# OpenShift audit policy (cluster-level configuration)
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  # Log all requests from cluster-health-mcp ServiceAccount
  - level: RequestResponse
    users:
      - "system:serviceaccount:self-healing-platform:cluster-health-mcp"
    omitStages:
      - RequestReceived
```

## RBAC Validation

### Testing RBAC Permissions

```bash
# Test if ServiceAccount can list nodes
oc auth can-i list nodes \
  --as=system:serviceaccount:self-healing-platform:cluster-health-mcp

# Test if ServiceAccount can delete pods (should be no)
oc auth can-i delete pods \
  --as=system:serviceaccount:self-healing-platform:cluster-health-mcp

# Test KServe access
oc auth can-i get inferenceservices \
  --as=system:serviceaccount:self-healing-platform:cluster-health-mcp \
  -n self-healing-platform
```

### Automated RBAC Tests

```go
// test/integration/rbac_test.go
func TestRBACPermissions(t *testing.T) {
    client := setupK8sClient()

    // Test allowed operations
    t.Run("ListNodes", func(t *testing.T) {
        _, err := client.CoreV1().Nodes().List(context.Background(), metav1.ListOptions{})
        assert.NoError(t, err, "Should be able to list nodes")
    })

    // Test forbidden operations
    t.Run("DeletePod", func(t *testing.T) {
        err := client.CoreV1().Pods("default").Delete(context.Background(), "test-pod", metav1.DeleteOptions{})
        assert.Error(t, err, "Should NOT be able to delete pods")
        assert.Contains(t, err.Error(), "forbidden")
    })
}
```

## Security Scanning

### Container Image Scanning

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build container image
        run: docker build -t cluster-health-mcp:test .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: cluster-health-mcp:test
          severity: CRITICAL,HIGH
          exit-code: 1

      - name: Run Snyk security scan
        uses: snyk/actions/docker@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          image: cluster-health-mcp:test
          args: --severity-threshold=high
```

### Code Security Scanning

```bash
# Run gosec for Go code security analysis
make security-scan

# Makefile target
security-scan:
	gosec -exclude=G104 ./...
	trivy fs --severity HIGH,CRITICAL .
```

## Success Criteria

### Phase 1 Success (Week 2)
- ✅ ServiceAccount created with minimal permissions
- ✅ ClusterRole and Role defined
- ✅ RBAC tests passing
- ✅ Security context configured (non-root, read-only FS)

### Phase 2 Success (Week 3)
- ✅ Pod starts with restricted-v2 SCC
- ✅ Network policy restricts traffic correctly
- ✅ RBAC validation tests passing
- ✅ No security scan vulnerabilities (CRITICAL/HIGH)

### Phase 3 Success (Week 4)
- ✅ Production deployment with security hardening
- ✅ Audit logging configured
- ✅ Security documentation complete
- ✅ Penetration testing passed

## Related ADRs

- [ADR-003: Standalone MCP Server Architecture](003-standalone-mcp-server-architecture.md)
- [ADR-006: Integration Architecture](006-integration-architecture.md)
- [ADR-008: Distroless Container Images](008-distroless-container-images.md)

## References

- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [OpenShift Security Context Constraints](https://docs.openshift.com/container-platform/4.18/authentication/managing-security-context-constraints.html)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [OpenShift Cluster Health MCP PRD](../../PRD.md)

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Over-privileged access** | Low | High | Regular RBAC audits, automated testing |
| **Token exposure** | Low | High | No token logging, secure volume mounts |
| **Privilege escalation** | Very Low | High | Drop all capabilities, read-only FS |
| **Network exposure** | Low | Medium | NetworkPolicy, TLS for external traffic |

## Approval

- **Architect**: Approved
- **Security Team**: Approved
- **Platform Team**: Approved
- **Date**: 2025-12-09
