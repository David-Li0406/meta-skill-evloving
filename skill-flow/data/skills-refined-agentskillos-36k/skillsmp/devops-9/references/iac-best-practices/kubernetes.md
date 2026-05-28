# Kubernetes Best Practices Patterns

**Category**: devops/iac-best-practices/kubernetes
**Description**: Kubernetes manifest organizational and operational best practices
**CWE**: CWE-1188

---

## Label Patterns

### Missing Standard Labels
**Pattern**: `metadata:\s*\n\s+name:[^\n]+\n(?:(?!labels:).)*spec:`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Resources should have standard labels for organization
- Required labels: app, version, component
- Remediation: Add `labels: { app.kubernetes.io/name: myapp, app.kubernetes.io/version: "1.0" }`

### Missing App Label
**Pattern**: `labels:\s*\n(?:(?!app\.kubernetes\.io/name|app:).)*\n\s+[a-z]`
**Type**: regex
**Severity**: low
**Languages**: [yaml, kubernetes]
- All resources should have an app/name label for identification
- Remediation: Add `app.kubernetes.io/name: <app-name>` label

---

## Resource Management

### Missing Resource Requests
**Pattern**: `containers:\s*\n\s*-\s*name:[^\n]+\n(?:(?!resources:).)*image:`
**Type**: regex
**Severity**: high
**Languages**: [yaml, kubernetes]
- Containers should define resource requests for scheduling
- Remediation: Add `resources: { requests: { cpu: "100m", memory: "128Mi" } }`

### Missing Resource Limits
**Pattern**: `resources:\s*\n(?:(?!limits:).)*requests:`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Containers should define resource limits to prevent resource exhaustion
- Remediation: Add `limits: { cpu: "500m", memory: "512Mi" }`

---

## Health Checks

### Missing Liveness Probe
**Pattern**: `containers:\s*\n\s*-\s*name:[^\n]+\n(?:(?!livenessProbe:).)*ports:`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Containers should have liveness probes for restart on failure
- Remediation: Add `livenessProbe: { httpGet: { path: /health, port: 8080 } }`

### Missing Readiness Probe
**Pattern**: `containers:\s*\n\s*-\s*name:[^\n]+\n(?:(?!readinessProbe:).)*ports:`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Containers should have readiness probes for traffic management
- Remediation: Add `readinessProbe: { httpGet: { path: /ready, port: 8080 } }`

---

## Replica Management

### Single Replica Deployment
**Pattern**: `replicas:\s*1\s*\n`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Production deployments should have multiple replicas for HA
- Remediation: Set `replicas: 2` or higher for production

### Missing PodDisruptionBudget
**Pattern**: `kind:\s*Deployment`
**Type**: structural
**Severity**: low
**Languages**: [yaml, kubernetes]
- Critical deployments should have PodDisruptionBudget
- Remediation: Create PDB with `minAvailable` or `maxUnavailable`

---

## Namespace Best Practices

### Using Default Namespace
**Pattern**: `namespace:\s*["']?default["']?\s*\n`
**Type**: regex
**Severity**: low
**Languages**: [yaml, kubernetes]
- Avoid using the default namespace in production
- Remediation: Create and use application-specific namespaces

### Missing Namespace
**Pattern**: `metadata:\s*\n\s+name:[^\n]+\n(?:(?!namespace:).)*spec:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, kubernetes]
- Resources should explicitly specify namespace
- Remediation: Add `namespace: <namespace>` to metadata

---

## Image Best Practices

### Missing Image Pull Policy
**Pattern**: `image:\s*[^\n]+\n(?:(?!imagePullPolicy:).)*ports:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, kubernetes]
- Containers should specify imagePullPolicy explicitly
- Remediation: Add `imagePullPolicy: IfNotPresent` or `Always`

---

## References

- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [CWE-1188: Insecure Default Initialization of Resource](https://cwe.mitre.org/data/definitions/1188.html)
