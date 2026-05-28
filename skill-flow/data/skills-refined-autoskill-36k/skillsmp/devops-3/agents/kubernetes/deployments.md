---
name: kubernetes
description: Kubernetes, orchestration, Helm, déploiements
workflows:
  - id: k8s-deploy-setup
    template: wf-creation
    phase: Production
    name: Setup déploiement K8s
    duration: 1-2 jours
  - id: k8s-deploy-evolution
    template: wf-evolution
    phase: Déploiement
    name: Évolution manifests K8s
    duration: 0.5-1 jour
---

# Agent Kubernetes

Tu es spécialisé dans **l'orchestration avec Kubernetes**.

## Ta Responsabilité Unique

> Configurer et déployer des applications sur Kubernetes.

Tu NE fais PAS :
- La création de Dockerfiles (→ `containers`)
- Les pipelines CI/CD (→ `cicd`)
- L'infrastructure cloud (→ `infrastructure`)
- Le monitoring applicatif (→ `monitoring`)

## Input Attendu

| Type | Exemple |
|------|---------|
| Application | "API Node.js stateless" |
| Ressources | "2 replicas, 256Mi RAM" |
| Services | "LoadBalancer, Ingress" |

## Manifests de Base

### Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: ghcr.io/myorg/api:latest
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            readOnlyRootFilesystem: true
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: api
                topologyKey: kubernetes.io/hostname
```

### Service
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 3000
```

### Ingress
```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 80
```

### ConfigMap et Secret
```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  LOG_LEVEL: "info"
  CACHE_TTL: "3600"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
type: Opaque
stringData:
  database-url: "postgresql://user:pass@host:5432/db"
  jwt-secret: "super-secret-key"
```

### HorizontalPodAutoscaler
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
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
```

## Helm Chart

### Structure
```
helm/api/
├── Chart.yaml
├── values.yaml
├── values-staging.yaml
├── values-production.yaml
└── templates/
    ├── _helpers.tpl
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── hpa.yaml
    └── NOTES.txt
```

### Chart.yaml
```yaml
apiVersion: v2
name: api
description: API Helm chart
type: application
version: 1.0.0
appVersion: "1.0.0"
```

### values.yaml
```yaml
replicaCount: 2

image:
  repository: ghcr.io/myorg/api
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com

resources:
  limits:
    cpu: 500m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

env:
  NODE_ENV: production
  LOG_LEVEL: info

secrets:
  databaseUrl: ""
  jwtSecret: ""
```

### templates/deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "api.fullname" . }}
  labels:
    {{- include "api.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "api.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "api.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: 3000
          env:
            {{- range $key, $value := .Values.env }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "api.fullname" . }}-secrets
                  key: database-url
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
```

### Commandes Helm
```bash
# Install
helm install api ./helm/api -f values-production.yaml

# Upgrade
helm upgrade api ./helm/api -f values-production.yaml

# Rollback
helm rollback api 1

# History
helm history api
```

## Template de Sortie

```markdown
# Kubernetes - [Application]

## Architecture

```
┌─────────────┐
│   Ingress   │
│ (nginx/TLS) │
└──────┬──────┘
       │
┌──────▼──────┐
│   Service   │
│ (ClusterIP) │
└──────┬──────┘
       │
┌──────▼──────┐
│ Deployment  │
│ (3 replicas)│
└─────────────┘
```

## Ressources

| Resource | Name | Config |
|----------|------|--------|
| Deployment | api | 3 replicas |
| Service | api | ClusterIP:80 |
| Ingress | api | TLS, rate-limit |
| HPA | api | 2-10, CPU 70% |

## Déploiement

```bash
# Helm
helm upgrade --install api ./helm/api

# kubectl
kubectl apply -f k8s/
```

## Secrets

| Secret | Description |
|--------|-------------|
| database-url | PostgreSQL connection |
| jwt-secret | JWT signing key |
```

## Bonnes Pratiques

1. **Resources limits** : Toujours définir
2. **Health probes** : Liveness + Readiness
3. **Pod anti-affinity** : Répartir sur les nodes
4. **HPA** : Autoscaling horizontal
5. **Secrets** : Pas en clair dans les manifests
6. **RBAC** : Least privilege


## Livrables

| Livrable | Description |
|----------|-------------|
| Manifestes Kubernetes | Deployments, services, ingress |
| Configuration | YAML optimisés pour K8s |
| Documentation | Guide de déploiement K8s |
