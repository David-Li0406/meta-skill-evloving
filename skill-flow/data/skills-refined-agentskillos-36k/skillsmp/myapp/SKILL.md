---
name: Container Orchestration
description: This skill should be used when the user asks to "deploy to Kubernetes", "configure Docker", "create Helm chart", "Kubernetes deployment", "container orchestration", "Docker Compose", "kubectl", "pod configuration", "service mesh", "Kubernetes scaling", "container networking", or needs help with containerization and orchestration.
version: 1.0.0
---

# Container Orchestration

Comprehensive guidance for Docker, Kubernetes, and container orchestration best practices.

## Docker

### Optimized Dockerfile

```dockerfile
# Multi-stage build for Node.js
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001

COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

USER nextjs
EXPOSE 3000
ENV NODE_ENV=production

CMD ["npm", "start"]
```

### Docker Best Practices

| Practice | Rationale |
|----------|-----------|
| Multi-stage builds | Smaller final images |
| .dockerignore | Exclude unnecessary files |
| Non-root user | Security |
| Specific base tags | Reproducibility |
| COPY over ADD | Explicit behavior |
| Combined RUN commands | Fewer layers |

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}  # From .env file
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: mydb
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    driver: bridge
```

## Kubernetes Fundamentals

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 20
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
---
# LoadBalancer for external access
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

### ConfigMap and Secrets

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  LOG_LEVEL: "info"
  FEATURE_FLAGS: |
    {
      "new_ui": true,
      "beta_features": false
    }
---
# Secrets should be created via kubectl or external secrets manager
# kubectl create secret generic myapp-secrets \
#   --from-literal=database-url="$(vault kv get -field=url secret/db)" \
#   --from-literal=api-key="$(vault kv get -field=key secret/api)"
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
# Values should be base64 encoded and managed externally
# Never commit actual secret values to version control
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
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
```

## Helm Charts

### Chart Structure

```
myapp/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   └── _helpers.tpl
└── charts/
```

### Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: My Application Helm Chart
version: 1.0.0
appVersion: "1.0.0"
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

### values.yaml

```yaml
replicaCount: 3

image:
  repository: myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi

# External secrets - values injected at deploy time
externalSecrets:
  enabled: true
  secretStore: vault-backend

postgresql:
  enabled: true
  auth:
    database: myapp
    existingSecret: postgresql-credentials
```

### Template Example

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 8080
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
```

### Helm Commands

```bash
# Install chart
helm install myapp ./myapp -f values-prod.yaml

# Upgrade release
helm upgrade myapp ./myapp -f values-prod.yaml

# Rollback
helm rollback myapp 1

# Uninstall
helm uninstall myapp

# Template rendering (debug)
helm template myapp ./myapp -f values-prod.yaml
```

## kubectl Commands

```bash
# Basic operations
kubectl get pods -n namespace
kubectl describe pod pod-name
kubectl logs pod-name -f
kubectl exec -it pod-name -- /bin/sh

# Deployments
kubectl rollout status deployment/myapp
kubectl rollout restart deployment/myapp
kubectl rollout undo deployment/myapp

# Scaling
kubectl scale deployment/myapp --replicas=5

# Port forwarding
kubectl port-forward svc/myapp 8080:80

# Apply manifests
kubectl apply -f manifests/ -R

# Debug
kubectl get events --sort-by='.lastTimestamp'
kubectl top pods
kubectl top nodes
```

## Resource Management

### Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-namespace
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
```

### Limit Ranges

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
spec:
  limits:
  - default:
      cpu: 500m
      memory: 256Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    type: Container
```

## Additional Resources

### Reference Files

- **`references/k8s-patterns.md`** - Kubernetes deployment patterns
- **`references/helm-best-practices.md`** - Helm chart guidelines

### Example Files

- **`examples/full-k8s-stack.yaml`** - Complete Kubernetes manifests
- **`examples/helm-chart/`** - Production-ready Helm chart
