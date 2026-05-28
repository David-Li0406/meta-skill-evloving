---
name: kubernetes
description: Kubernetes cluster management commands including pods, services, deployments, debugging, and resource operations.
---

# Kubernetes — Common Commands

**Basic Operations**

```bash
# Create namespace
kubectl create ns demo-ns

# Run pod
kubectl run whoami --image=traefik/whoami -n demo-ns

# Expose pod as service
kubectl expose pod whoami --type=NodePort --port=80 --name=whoami-svc -n demo-ns

# Get resources with details
kubectl get pods -n demo-ns -o wide
kubectl get svc -n demo-ns -o wide

# List all resources in all namespaces
kubectl get all -A

# Show cluster info
kubectl cluster-info
```

**Debugging**

```bash
# Run temporary debug pod
kubectl run -n demo-ns -it --rm --image=curlimages/curl:8.1.2 curly -- /bin/sh

# Exec into pod
kubectl exec -n demo-ns -it whoami -- /bin/bash

# Print logs
kubectl logs pod_name

# Run command in pod
kubectl exec pod_name -- ls /

# Resource usage
kubectl top pod|node

# Order events by timestamp
kubectl get events --sort-by='.metadata.creationTimestamp'
```

**Labels & Annotations**

```bash
# Add label to pod
kubectl label pods name unhealthy=true

# Explain resource fields
kubectl explain pods.spec.containers
```

**Context & Configuration**

```bash
# Switch context
kubectl config use-context CONTEXT_NAME

# Autocomplete in bash
source <(kubectl completion bash)

# List global options
kubectl options
```

**Other Useful**

```bash
kubectl get resourcequota -n demo-ns
kubectl get deploy -n demo-ns
kubectl get rs -n demo-ns
kubectl get po -n demo-ns
kubectl get services -n demo-ns
kubectl get ingresses -n demo-ns
kubectl describe service whoami-svc -n demo-ns
kubectl rollout restart deployment.apps/spring-boot-app -n demo-ns

# Delete namespace stuck in terminating state
(
NAMESPACE=your-rogue-namespace
kubectl proxy &
kubectl get namespace $NAMESPACE -o json |jq '.spec = {"finalizers":[]}' >temp.json
curl -k -H "Content-Type: application/json" -X PUT --data-binary @temp.json 127.0.0.1:8001/api/v1/namespaces/$NAMESPACE/finalize
)

# Install Gateway API CRDs
kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
  kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml

# Create docker registry secret
kubectl create secret docker-registry gitlab-registry --docker-server=https://docker.io --docker-username=jyasu --docker-password=jyasu --docker-email=jyasu@example.com --dry-run=client -o yaml
```

**Cleanup**

```bash
kubectl delete svc whoami-svc -n demo-ns
kubectl delete pod whoami -n demo-ns
kubectl delete pod curly -n demo-ns
```

**Manifest Templates**

```yaml
# --- Deployment ---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <app-name>
spec:
  replicas: 1
  revisionHistoryLimit: 3
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: <app-name>
  template:
    metadata:
      labels:
        app: <app-name>
    spec:
      containers:
      - name: <container-name>
        image: <registry>/<repo>:<tag>
        ports:
        - containerPort: <port>
        imagePullPolicy: IfNotPresent
        volumeMounts:
        - name: <volume-name>
          mountPath: /data
        env:
        - name: TZ
          value: Asia/Taipei
        envFrom:
        - configMapRef:
            name: <configmap-name>
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "200m"
            memory: "256Mi"
      volumes:
      - name: <volume-name>
        nfs:
          server: <nfs-server>
          path: <nfs-path>

---
# --- Service ---
apiVersion: v1
kind: Service
metadata:
  name: <svc-name>
spec:
  selector:
    app: <app-name>
  ports:
  - port: <svc-port>
    targetPort: <container-port>
  type: ClusterIP

---
# --- HTTPRoute (Gateway API) ---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: <route-name>
spec:
  parentRefs:
  - name: <gateway-name>
    sectionName: https
    namespace: <gateway-namespace>
  - name: <gateway-name>
    sectionName: http
    namespace: <gateway-namespace>
  hostnames:
  - "<host.example.com>"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: <svc-name>
      port: <svc-port>
```

🔗 [Kubernetes Command Reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)