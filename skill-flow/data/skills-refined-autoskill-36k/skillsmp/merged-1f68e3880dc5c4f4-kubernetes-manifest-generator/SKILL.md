---
name: kubernetes-manifest-generator
description: Use this skill to generate production-ready Kubernetes manifests for deploying applications, including Deployments, Services, Ingress, HPA, ConfigMaps, Secrets, and StatefulSets.
---

# Kubernetes Manifest Generator

Generate complete Kubernetes manifests by analyzing your application and applying production best practices. This skill supports various Kubernetes resources and configurations.

## What This Skill Does

- Auto-generates K8s manifests from project analysis
- Creates Deployments, Services, ConfigMaps, Secrets, Ingress, and HPA
- Implements health checks (liveness/readiness probes)
- Sets resource limits and requests
- Follows security best practices and 12-factor app principles

## Instructions

### Phase 1: Application Analysis

Analyze the application to determine requirements:

```bash
# Detect application type
Use Glob/Grep to find:
- Dockerfile → Container config
- .env → Environment variables
- Port bindings
- Volume requirements
```

### Phase 2: Generate Core Manifests

**Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <app_name>
  labels:
    app: <app_name>
spec:
  replicas: <replica_count>
  selector:
    matchLabels:
      app: <app_name>
  template:
    metadata:
      labels:
        app: <app_name>
    spec:
      containers:
      - name: <app_name>
        image: <image_name>:<tag>
        ports:
        - containerPort: <container_port>
        resources:
          requests:
            memory: "<memory_request>"
            cpu: "<cpu_request>"
          limits:
            memory: "<memory_limit>"
            cpu: "<cpu_limit>"
        livenessProbe:
          httpGet:
            path: <liveness_path>
            port: <container_port>
          initialDelaySeconds: <initial_delay>
          periodSeconds: <period>
        readinessProbe:
          httpGet:
            path: <readiness_path>
            port: <container_port>
          initialDelaySeconds: <initial_delay>
          periodSeconds: <period>
        envFrom:
        - configMapRef:
            name: <app_name>-config
        - secretRef:
            name: <app_name>-secrets
```

**Service**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <app_name>
spec:
  selector:
    app: <app_name>
  ports:
  - protocol: TCP
    port: <service_port>
    targetPort: <container_port>
  type: ClusterIP
```

**ConfigMap**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: <app_name>-config
data:
  NODE_ENV: production
  LOG_LEVEL: info
  API_URL: <api_url>
```

**HPA (Horizontal Pod Autoscaler)**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: <app_name>-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: <app_name>
  minReplicas: <min_replicas>
  maxReplicas: <max_replicas>
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: <cpu_target>
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: <memory_target>
```

**Ingress**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: <app_name>-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - <host_name>
    secretName: <tls_secret_name>
  rules:
  - host: <host_name>
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: <app_name>
            port:
              number: <service_port>
```

## Advanced Features

### Multi-Environment Setup

Generate manifests for different environments (dev/staging/prod) using Kustomize.

### Database StatefulSet

For stateful applications, use a StatefulSet configuration.

## Best Practices Applied

1. **Resource Limits**: Always set requests and limits.
2. **Health Checks**: Implement liveness and readiness probes.
3. **Replicas**: Minimum 2 for high availability.
4. **Labels**: Use consistent labeling for service discovery.
5. **Security**: Use non-root containers and read-only file systems.
6. **Secrets**: Never commit sensitive data.

## Tool Requirements

- **Read**: Analyze application config
- **Write**: Generate manifest files
- **Glob**: Find relevant files
- **Grep**: Search for patterns

## Examples

### Example 1: Simple Web App

**User**: "Generate K8s manifests for my Node.js app"

**Output**:
- Deployment with 3 replicas
- ClusterIP Service
- ConfigMap for environment variables
- HPA (2-10 pods)
- Ingress with TLS

### Example 2: Microservices

**User**: "Create K8s setup for microservices architecture"

**Output**:
- Multiple Deployments (one per service)
- Services with ClusterIP
- NetworkPolicy for security
- Istio VirtualService/DestinationRule

## Error Handling

| Error | Quick Fix |
|-------|-----------|
| ImagePullBackOff | Check image name, tag, registry credentials |
| CrashLoopBackOff | Check logs: `kubectl logs <pod>` |
| OOMKilled | Increase memory limits |
| Pending | Check resources: `kubectl describe pod <pod>` |

## Resources

- Kubernetes documentation: https://kubernetes.io/docs/
- kubectl reference: https://kubernetes.io/docs/reference/kubectl/