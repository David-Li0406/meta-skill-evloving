# Kubernetes Security Patterns

**Category**: devops/iac-policies/kubernetes
**Description**: Kubernetes manifest security and organizational policy patterns
**CWE**: CWE-250, CWE-732

---

## Container Security Patterns

### Container Running as Root
**Pattern**: `(?i)runAsUser:\s*0\b`
**Type**: regex
**Severity**: high
**Languages**: [yaml, kubernetes]
- Containers should not run as root user
- Remediation: Set `runAsUser` to a non-root UID (e.g., 1000)
- CWE-250: Execution with Unnecessary Privileges

### Privileged Container
**Pattern**: `(?i)privileged:\s*true`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, kubernetes]
- Containers should not run in privileged mode
- Remediation: Set `privileged: false` and use specific capabilities

### Allow Privilege Escalation
**Pattern**: `(?i)allowPrivilegeEscalation:\s*true`
**Type**: regex
**Severity**: high
**Languages**: [yaml, kubernetes]
- Containers should not allow privilege escalation
- Remediation: Set `allowPrivilegeEscalation: false`

### Host Network Namespace
**Pattern**: `(?i)hostNetwork:\s*true`
**Type**: regex
**Severity**: high
**Languages**: [yaml, kubernetes]
- Pods should not use the host network namespace
- Remediation: Set `hostNetwork: false` and use NetworkPolicies

### Host PID Namespace
**Pattern**: `(?i)hostPID:\s*true`
**Type**: regex
**Severity**: high
**Languages**: [yaml, kubernetes]
- Pods should not use the host PID namespace
- Remediation: Set `hostPID: false`

### Host IPC Namespace
**Pattern**: `(?i)hostIPC:\s*true`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Pods should not use the host IPC namespace
- Remediation: Set `hostIPC: false`

### All Capabilities Added
**Pattern**: `(?i)capabilities:[\s\S]*?add:\s*\[\s*["']?ALL["']?\s*\]`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, kubernetes]
- Containers should not have all Linux capabilities
- Remediation: Add only specific required capabilities

### SYS_ADMIN Capability
**Pattern**: `(?i)capabilities:[\s\S]*?add:[\s\S]*?["']?SYS_ADMIN["']?`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, kubernetes]
- SYS_ADMIN capability is dangerous and rarely needed
- Remediation: Remove SYS_ADMIN and use more specific capabilities

### Writable Root Filesystem
**Pattern**: `(?i)readOnlyRootFilesystem:\s*false`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Container root filesystem should be read-only
- Remediation: Set `readOnlyRootFilesystem: true`

---

## Resource Management Patterns

### Missing Resource Limits
**Pattern**: `(?i)containers:[\s\S]*?name:\s*[^\n]+(?:(?!resources:).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Containers should have resource limits defined
- Remediation: Add `resources.limits` for CPU and memory

### Missing Memory Limit
**Pattern**: `(?i)resources:[\s\S]*?limits:(?:(?!memory:).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Containers should have memory limits to prevent OOM
- Remediation: Add `limits.memory` (e.g., "512Mi")

### Missing CPU Limit
**Pattern**: `(?i)resources:[\s\S]*?limits:(?:(?!cpu:).)*$`
**Type**: regex
**Severity**: low
**Languages**: [yaml, kubernetes]
- Containers should have CPU limits for fair scheduling
- Remediation: Add `limits.cpu` (e.g., "500m")

---

## Network Security Patterns

### Service Exposed via NodePort
**Pattern**: `(?i)type:\s*NodePort`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- NodePort exposes service on all cluster nodes
- Remediation: Use LoadBalancer or ClusterIP with Ingress

### Missing NetworkPolicy
**Pattern**: `kind:\s*Deployment`
**Type**: structural
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Namespaces should have NetworkPolicies for traffic control
- Remediation: Create NetworkPolicy to restrict pod communication

---

## RBAC Patterns

### ClusterRoleBinding to cluster-admin
**Pattern**: `(?i)roleRef:[\s\S]*?name:\s*["']?cluster-admin["']?`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, kubernetes]
- Binding to cluster-admin grants full cluster access
- Remediation: Create custom ClusterRole with minimal permissions
- CWE-732: Incorrect Permission Assignment

### Wildcard Verb in Role
**Pattern**: `(?i)verbs:\s*\[\s*["']?\*["']?\s*\]`
**Type**: regex
**Severity**: high
**Languages**: [yaml, kubernetes]
- Roles should not grant wildcard verb permissions
- Remediation: Specify explicit verbs

### Wildcard Resource in Role
**Pattern**: `(?i)resources:\s*\[\s*["']?\*["']?\s*\]`
**Type**: regex
**Severity**: high
**Languages**: [yaml, kubernetes]
- Roles should not grant access to all resources
- Remediation: Specify explicit resource types

### Secrets Access in Role
**Pattern**: `(?i)resources:[\s\S]*?["']?secrets["']?[\s\S]*?verbs:\s*\[[\s\S]*?(?:get|list|\*)[\s\S]*?\]`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Access to secrets should be carefully controlled
- Remediation: Ensure secrets access is necessary and audited

---

## Pod Security Patterns

### Missing SecurityContext
**Pattern**: `(?i)spec:[\s\S]*?containers:(?:(?!securityContext:).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Pods should have securityContext defined
- Remediation: Add securityContext with runAsNonRoot, capabilities

### Missing RunAsNonRoot
**Pattern**: `(?i)securityContext:(?:(?!runAsNonRoot).)*$`
**Type**: regex
**Severity**: high
**Languages**: [yaml, kubernetes]
- Pods should enforce non-root execution
- Remediation: Add `runAsNonRoot: true`

### Default Service Account
**Pattern**: `(?i)serviceAccountName:\s*["']?default["']?`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Pods should not use the default service account
- Remediation: Create and use dedicated service account

### Automount Service Account Token
**Pattern**: `(?i)automountServiceAccountToken:\s*true`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Service account tokens should not be auto-mounted unless needed
- Remediation: Set `automountServiceAccountToken: false`

---

## Image Security Patterns

### Image with Latest Tag
**Pattern**: `(?i)image:\s*[^\s:]+:latest`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Images should not use the :latest tag
- Remediation: Use specific version tags (e.g., nginx:1.25.0)

### Image without Tag
**Pattern**: `(?i)image:\s*[^\s:]+\s*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, kubernetes]
- Images should have explicit tags
- Remediation: Specify version tag

### Image Pull Policy Always
**Pattern**: `(?i)imagePullPolicy:\s*Always`
**Type**: regex
**Severity**: low
**Languages**: [yaml, kubernetes]
- Always pulling images may slow deployments
- Remediation: Consider IfNotPresent for production

---

## References

- [CWE-250: Execution with Unnecessary Privileges](https://cwe.mitre.org/data/definitions/250.html)
- [CWE-732: Incorrect Permission Assignment](https://cwe.mitre.org/data/definitions/732.html)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NSA/CISA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
