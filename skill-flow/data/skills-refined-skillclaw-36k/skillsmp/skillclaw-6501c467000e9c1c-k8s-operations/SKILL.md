---
name: k8s-operations
description: Use this skill when managing Kubernetes operations, deployment patterns, and cloud-native best practices, particularly when working with containers, K8s manifests, or cloud infrastructure.
---

# Kubernetes Operations Skill

## Core Resources

### Workload Resources

```yaml
# Deployment - Stateless applications
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:v1
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 3
```

```yaml
# StatefulSet - Stateful applications
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: "db"
  replicas: 3
  selector:
    matchLabels:
      app: db
  template:
    spec:
      containers:
      - name: db
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### Service Types

| Type        | Use Case               | Access                  |
|-------------|------------------------|-------------------------|
| ClusterIP   | Internal services      | Within cluster only     |
| NodePort    | Development/testing     | Node IP + port         |
| LoadBalancer| Production external    | Cloud LB IP            |
| ExternalName| External DNS alias     | DNS CNAME              |

### Ingress Pattern
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app
            port:
              number: 80
```

## Deployment Strategies

### Rolling Update (Default)
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
```