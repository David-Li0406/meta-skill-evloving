---
id: kubernetes-deployment
name: "Kubernetes Deployment"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Kubernetes Deployment

## Overview

Kubernetes (K8s) orchestrates containerized applications across clusters of machines, providing automated deployment, scaling, and management. It handles service discovery, load balancing, storage orchestration, and self-healing capabilities.

## When to Use

- Production workloads requiring high availability
- Microservices architectures with many services
- Applications needing horizontal auto-scaling
- Multi-cloud or hybrid cloud deployments
- Teams requiring declarative infrastructure

## Key Concepts

| Concept | Description |
|---------|-------------|
| Pod | Smallest deployable unit, one or more containers |
| Deployment | Manages ReplicaSets and pod updates |
| Service | Stable network endpoint for pods |
| ConfigMap | Non-sensitive configuration data |
| Secret | Sensitive data (passwords, tokens) |
| Ingress | External HTTP/HTTPS routing |
| Namespace | Virtual cluster for resource isolation |
| PersistentVolume | Storage abstraction for data persistence |

### Architecture Overview

```
                    ┌─────────────────────────────────────┐
                    │           Ingress Controller        │
                    └─────────────────┬───────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
           ▼                          ▼                          ▼
    ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
    │  Service A  │           │  Service B  │           │  Service C  │
    └──────┬──────┘           └──────┬──────┘           └──────┬──────┘
           │                         │                          │
    ┌──────┴──────┐           ┌──────┴──────┐           ┌──────┴──────┐
    │ Deployment  │           │ Deployment  │           │ StatefulSet │
    │  (3 pods)   │           │  (2 pods)   │           │  (3 pods)   │
    └─────────────┘           └─────────────┘           └─────────────┘
```

## Implementation

### Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  labels:
    app.kubernetes.io/name: myapp
    environment: production
```

### ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: myapp
data:
  LOG_LEVEL: "info"
  DATABASE_HOST: "postgres-service"
  DATABASE_PORT: "5432"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
  APP_CONFIG: |
    {
      "feature_flags": {
        "new_dashboard": true,
        "beta_api": false
      },
      "cache_ttl": 3600
    }
```

### Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
  namespace: myapp
type: Opaque
stringData:
  DATABASE_PASSWORD: "secure-password"
  SECRET_KEY: "django-insecure-change-me"
  API_KEY: "external-api-key"
---
# For Docker registry credentials
apiVersion: v1
kind: Secret
metadata:
  name: registry-credentials
  namespace: myapp
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
```

### Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp
  labels:
    app.kubernetes.io/name: myapp
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  template:
    metadata:
      labels:
        app.kubernetes.io/name: myapp
        app.kubernetes.io/version: "1.0.0"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: myapp
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      imagePullSecrets:
        - name: registry-credentials

      initContainers:
        - name: wait-for-db
          image: busybox:1.36
          command: ['sh', '-c', 'until nc -z postgres-service 5432; do echo waiting for db; sleep 2; done']

        - name: run-migrations
          image: registry.example.com/myapp:1.0.0
          command: ['python', 'manage.py', 'migrate', '--noinput']
          envFrom:
            - configMapRef:
                name: myapp-config
            - secretRef:
                name: myapp-secrets

      containers:
        - name: myapp
          image: registry.example.com/myapp:1.0.0
          imagePullPolicy: IfNotPresent

          ports:
            - name: http
              containerPort: 8000
              protocol: TCP

          envFrom:
            - configMapRef:
                name: myapp-config
            - secretRef:
                name: myapp-secrets

          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace

          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"

          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

          startupProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30

          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: app-data
              mountPath: /app/data

      volumes:
        - name: tmp
          emptyDir: {}
        - name: app-data
          persistentVolumeClaim:
            claimName: myapp-data

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: myapp
                topologyKey: kubernetes.io/hostname

      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: myapp
```

### Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: myapp
  labels:
    app.kubernetes.io/name: myapp
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: myapp
  ports:
    - name: http
      port: 80
      targetPort: http
      protocol: TCP
---
# Headless service for StatefulSet
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
  namespace: myapp
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app.kubernetes.io/name: myapp
  ports:
    - name: http
      port: 80
      targetPort: http
```

### Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  namespace: myapp
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
    - hosts:
        - myapp.example.com
        - api.example.com
      secretName: myapp-tls
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-service
                port:
                  number: 80
    - host: api.example.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: myapp-service
                port:
                  number: 80
```

### HorizontalPodAutoscaler

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

### PersistentVolumeClaim

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-data
  namespace: myapp
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 10Gi
```

### NetworkPolicy

```yaml
# networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-network-policy
  namespace: myapp
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: myapp
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: myapp
      ports:
        - protocol: TCP
          port: 8000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: redis
      ports:
        - protocol: TCP
          port: 6379
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

## Best Practices

1. **Use namespaces** - Isolate environments and teams with namespaces
2. **Set resource requests and limits** - Enable proper scheduling and prevent noisy neighbors
3. **Implement all three probes** - liveness, readiness, and startup probes
4. **Use pod disruption budgets** - Ensure availability during maintenance
5. **Apply network policies** - Restrict pod-to-pod communication
6. **Use pod anti-affinity** - Spread pods across nodes for resilience
7. **Enable HPA** - Auto-scale based on actual load
8. **Use init containers** - Handle dependencies and migrations
9. **Apply security contexts** - Run as non-root, read-only filesystem
10. **Version your deployments** - Use labels for tracking versions

## Common Pitfalls

1. **No resource limits** - Pods can consume all node resources, causing evictions. Always set both requests and limits.

2. **Missing probes** - Without readiness probes, traffic routes to unready pods. Without liveness probes, stuck pods aren't restarted.

3. **Using latest tag** - Unpredictable deployments. Always use specific image versions.

4. **Storing secrets in ConfigMaps** - ConfigMaps are not encrypted. Use Secrets for sensitive data.

5. **No pod disruption budget** - All pods can be evicted simultaneously during maintenance.

6. **Ignoring node affinity** - Pods may all land on same node. Use anti-affinity for resilience.

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Production Best Practices](https://learnk8s.io/production-best-practices)
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)
