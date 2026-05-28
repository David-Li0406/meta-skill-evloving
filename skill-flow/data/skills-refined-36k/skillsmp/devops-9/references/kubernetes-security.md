# Kubernetes Security Patterns

## Pod Security

### Security Context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault

  containers:
    - name: app
      image: myapp:1.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
      volumeMounts:
        - name: tmp
          mountPath: /tmp

  volumes:
    - name: tmp
      emptyDir: {}
```

### Pod Security Standards

```yaml
# Enforce restricted policy on namespace
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## RBAC

### Principle of Least Privilege

```yaml
# Role with minimal permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-reader
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get"]
    resourceNames: ["app-config"]  # Specific resources only

---
# Bind to service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-reader-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: app-sa
    namespace: production
roleRef:
  kind: Role
  name: app-reader
  apiGroup: rbac.authorization.k8s.io
```

### Avoid ClusterRoleBindings

```yaml
# ❌ Too broad - cluster-wide access
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: app-admin
subjects:
  - kind: ServiceAccount
    name: app-sa
    namespace: default
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io

# ✅ Namespace-scoped
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-admin
  namespace: production
# ...
```

## Network Policies

### Default Deny

```yaml
# Deny all ingress by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress

---
# Deny all egress by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
```

### Allow Specific Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow from frontend pods
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - port: 8080
          protocol: TCP
  egress:
    # Allow to database
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
          protocol: TCP
    # Allow DNS
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - port: 53
          protocol: UDP
```

## Secrets Management

### External Secrets

```yaml
# Using External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: app-secrets
  data:
    - secretKey: database-password
      remoteRef:
        key: production/database
        property: password
```

### Sealed Secrets

```yaml
# Encrypt secrets for Git storage
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  encryptedData:
    database-password: AgBy3i4OJSWK+PiTySYZZA9rO...
```

### Mount Secrets Securely

```yaml
containers:
  - name: app
    env:
      # ❌ Avoid environment variables for secrets
      - name: DB_PASSWORD
        valueFrom:
          secretKeyRef:
            name: db-secret
            key: password

    # ✅ Prefer volume mounts
    volumeMounts:
      - name: secrets
        mountPath: /etc/secrets
        readOnly: true

volumes:
  - name: secrets
    secret:
      secretName: db-secret
      defaultMode: 0400
```

## Resource Limits

```yaml
containers:
  - name: app
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "256Mi"
        cpu: "500m"

---
# Enforce with LimitRange
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:
        memory: "256Mi"
        cpu: "200m"
      defaultRequest:
        memory: "128Mi"
        cpu: "100m"
      max:
        memory: "1Gi"
        cpu: "1000m"
```

## Service Account Security

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
automountServiceAccountToken: false  # Disable unless needed

---
# If token needed, mount explicitly
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: app-sa
  automountServiceAccountToken: true  # Explicit when needed
```

## Image Security

### Image Pull Policy

```yaml
containers:
  - name: app
    image: myregistry.io/app:v1.2.3
    imagePullPolicy: Always  # Or use digest

  # ✅ Use image digest
  - name: app
    image: myregistry.io/app@sha256:abc123...
```

### Admission Controller

```yaml
# OPA Gatekeeper constraint
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRepos
metadata:
  name: allowed-repos
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    repos:
      - "gcr.io/my-project/"
      - "docker.io/myorg/"
```

## Audit Logging

```yaml
# audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  # Log all requests to secrets
  - level: Metadata
    resources:
      - group: ""
        resources: ["secrets"]

  # Log pod exec
  - level: RequestResponse
    resources:
      - group: ""
        resources: ["pods/exec", "pods/attach"]

  # Log auth failures
  - level: Metadata
    omitStages:
      - RequestReceived
    users: ["system:anonymous"]
```

## Security Checklist

| Area | Check |
|------|-------|
| Pod Security | runAsNonRoot, readOnlyRootFilesystem, drop ALL capabilities |
| RBAC | No cluster-admin bindings, namespace-scoped roles |
| Network | Default deny policies, explicit allow rules |
| Secrets | External secrets manager, no secrets in Git |
| Images | Signed images, vulnerability scanning, private registry |
| Resources | Limits defined, LimitRange in place |
| Service Accounts | automountServiceAccountToken: false by default |
| Namespaces | Pod Security Standards enforced |

## Scanning Commands

```bash
# Scan cluster with kubesec
kubesec scan deployment.yaml

# Scan with kube-bench (CIS benchmark)
kubectl apply -f kube-bench-job.yaml
kubectl logs job/kube-bench

# Check RBAC
kubectl auth can-i --list --as=system:serviceaccount:default:app-sa

# Find privileged pods
kubectl get pods -A -o json | jq '.items[] | select(.spec.securityContext.privileged==true) | .metadata.name'
```
