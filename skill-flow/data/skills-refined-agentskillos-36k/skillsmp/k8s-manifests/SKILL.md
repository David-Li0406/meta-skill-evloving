---
name: k8s-manifests
description: Generate Kubernetes manifest templates for deployments, services, configmaps, secrets, ingress, and other resources. Use when creating new k8s resources, scaffolding applications, or needing YAML templates. Triggers on requests to create, generate, or scaffold kubernetes resources.
---

# Kubernetes Manifest Templates

## Quick Generation

```bash
# Generate deployment YAML
kubectl create deployment myapp --image=nginx --dry-run=client -o yaml > deployment.yaml

# Generate service YAML
kubectl create service clusterip myapp --tcp=80:80 --dry-run=client -o yaml > service.yaml

# Generate configmap from file
kubectl create configmap myconfig --from-file=config.yaml --dry-run=client -o yaml > configmap.yaml

# Generate secret
kubectl create secret generic mysecret --from-literal=password=secret --dry-run=client -o yaml > secret.yaml
```

## Deployment

### Standard Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
spec:
  replicas: ${REPLICAS:-3}
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}:${TAG}
          ports:
            - containerPort: ${PORT:-8080}
          env:
            - name: ENV
              value: "${ENVIRONMENT}"
          envFrom:
            - configMapRef:
                name: ${APP_NAME}-config
            - secretRef:
                name: ${APP_NAME}-secrets
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: ${PORT:-8080}
            initialDelaySeconds: 15
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: ${PORT:-8080}
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /healthz
              port: ${PORT:-8080}
            failureThreshold: 30
            periodSeconds: 10
      imagePullSecrets:
        - name: regcred
```

### Deployment with Init Container

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      initContainers:
        - name: init-db
          image: busybox:1.36
          command: ['sh', '-c', 'until nc -z ${DB_HOST} 5432; do echo waiting for db; sleep 2; done']
        - name: migrations
          image: ${IMAGE}:${TAG}
          command: ['./migrate', 'up']
          envFrom:
            - secretRef:
                name: ${APP_NAME}-db
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}:${TAG}
          ports:
            - containerPort: 8080
```

## Services

### ClusterIP (internal)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  type: ClusterIP
  selector:
    app: ${APP_NAME}
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
```

### NodePort (external via node)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
spec:
  type: NodePort
  selector:
    app: ${APP_NAME}
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080  # 30000-32767
```

### LoadBalancer (cloud provider)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  annotations:
    # AWS
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"
    # GCP
    cloud.google.com/load-balancer-type: "Internal"
spec:
  type: LoadBalancer
  selector:
    app: ${APP_NAME}
  ports:
    - port: 443
      targetPort: 8443
```

### Headless Service (StatefulSet)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}-headless
spec:
  clusterIP: None
  selector:
    app: ${APP_NAME}
  ports:
    - port: 5432
      targetPort: 5432
```

## Ingress

### NGINX Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - ${DOMAIN}
      secretName: ${APP_NAME}-tls
  rules:
    - host: ${DOMAIN}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ${APP_NAME}
                port:
                  number: 80
```

### Multiple Paths

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: api-v1
                port:
                  number: 80
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: api-v2
                port:
                  number: 80
```

## ConfigMap & Secret

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-config
data:
  # Simple key-value
  LOG_LEVEL: "info"
  API_URL: "https://api.example.com"
  
  # Multi-line file
  config.yaml: |
    server:
      port: 8080
      host: 0.0.0.0
    database:
      pool_size: 10
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secrets
type: Opaque
stringData:  # Plain text (base64 encoded on apply)
  DATABASE_URL: "postgresql://user:pass@host:5432/db"
  API_KEY: "secret-api-key"
---
# Or with base64 encoded data
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secrets
type: Opaque
data:  # Already base64 encoded
  password: cGFzc3dvcmQxMjM=  # echo -n "password123" | base64
```

### Docker Registry Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
```

```bash
# Create via kubectl
kubectl create secret docker-registry regcred \
  --docker-server=ghcr.io \
  --docker-username=$USER \
  --docker-password=$TOKEN
```

## StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ${APP_NAME}
spec:
  serviceName: ${APP_NAME}-headless
  replicas: 3
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: standard
        resources:
          requests:
            storage: 10Gi
```

## CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ${JOB_NAME}
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      backoffLimit: 3
      activeDeadlineSeconds: 3600
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: ${JOB_NAME}
              image: ${IMAGE}
              command: ["/bin/sh", "-c"]
              args:
                - |
                  echo "Running backup..."
                  /scripts/backup.sh
              envFrom:
                - secretRef:
                    name: ${JOB_NAME}-secrets
```

## HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ${APP_NAME}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ${APP_NAME}
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

## PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ${APP_NAME}-data
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard  # Or gp2, premium-rwo, etc.
  resources:
    requests:
      storage: 10Gi
```

## NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ${APP_NAME}-policy
spec:
  podSelector:
    matchLabels:
      app: ${APP_NAME}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - port: 8080
          protocol: TCP
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - port: 5432
    - to:  # Allow DNS
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - port: 53
          protocol: UDP
```

## ServiceAccount with RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ${APP_NAME}
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ${APP_NAME}-role
rules:
  - apiGroups: [""]
    resources: ["pods", "configmaps"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${APP_NAME}-binding
subjects:
  - kind: ServiceAccount
    name: ${APP_NAME}
roleRef:
  kind: Role
  name: ${APP_NAME}-role
  apiGroup: rbac.authorization.k8s.io
```

## PodDisruptionBudget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ${APP_NAME}
spec:
  selector:
    matchLabels:
      app: ${APP_NAME}
  minAvailable: 2  # Or use maxUnavailable: 1
```

## Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ${NAMESPACE}-quota
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "50"
    persistentvolumeclaims: "10"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: ${NAMESPACE}-limits
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
      max:
        cpu: "2"
        memory: "4Gi"
```

## Complete Application Stack

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    name: ${NAMESPACE}
---
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-config
  namespace: ${NAMESPACE}
data:
  LOG_LEVEL: "info"
---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
type: Opaque
stringData:
  DATABASE_URL: "postgresql://..."
---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}:${TAG}
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: ${APP_NAME}-config
            - secretRef:
                name: ${APP_NAME}-secrets
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  selector:
    app: ${APP_NAME}
  ports:
    - port: 80
      targetPort: 8080
---
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ${APP_NAME}
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```
