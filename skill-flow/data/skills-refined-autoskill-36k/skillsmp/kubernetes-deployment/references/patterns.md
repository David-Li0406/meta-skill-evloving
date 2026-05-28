# Kubernetes Deployment

## Patterns


---
  #### **Name**
Production-Ready Deployment
  #### **Description**
Deployment manifest with all production-critical fields configured
  #### **When**
Any production workload
  #### **Example**
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: api-server
      labels:
        app: api-server
        version: v1.2.3
    spec:
      replicas: 3
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxUnavailable: 1
          maxSurge: 1
      selector:
        matchLabels:
          app: api-server
      template:
        metadata:
          labels:
            app: api-server
            version: v1.2.3
        spec:
          containers:
          - name: api
            image: myapp/api:v1.2.3  # Pinned tag, never :latest
            ports:
            - containerPort: 8080
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "500m"
            livenessProbe:
              httpGet:
                path: /health
                port: 8080
              initialDelaySeconds: 10
              periodSeconds: 10
            readinessProbe:
              httpGet:
                path: /ready
                port: 8080
              initialDelaySeconds: 5
              periodSeconds: 5
            securityContext:
              runAsNonRoot: true
              readOnlyRootFilesystem: true
    

---
  #### **Name**
ConfigMap Checksum for Auto-Reload
  #### **Description**
Force pod restart when ConfigMap changes
  #### **When**
Application needs to reload on config changes
  #### **Example**
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: api-server
    spec:
      template:
        metadata:
          annotations:
            # Checksum changes when ConfigMap changes -> triggers rollout
            checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        spec:
          containers:
          - name: api
            envFrom:
            - configMapRef:
                name: api-config
    
    # Alternative: Use Reloader
    # Add annotation: reloader.stakater.com/auto: "true"
    

---
  #### **Name**
Horizontal Pod Autoscaler
  #### **Description**
Auto-scale based on CPU/memory or custom metrics
  #### **When**
Variable load patterns, need automatic scaling
  #### **Example**
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: api-server-hpa
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: api-server
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
          stabilizationWindowSeconds: 300  # Wait 5 min before scale down
    

---
  #### **Name**
External Secrets Integration
  #### **Description**
Sync secrets from external vault to Kubernetes
  #### **When**
Production secrets that shouldn't live in Git
  #### **Example**
    # Using External Secrets Operator
    apiVersion: external-secrets.io/v1beta1
    kind: ExternalSecret
    metadata:
      name: api-secrets
    spec:
      refreshInterval: 1h
      secretStoreRef:
        name: aws-secrets-manager
        kind: ClusterSecretStore
      target:
        name: api-secrets
        creationPolicy: Owner
      data:
      - secretKey: DATABASE_URL
        remoteRef:
          key: prod/api/database-url
      - secretKey: API_KEY
        remoteRef:
          key: prod/api/api-key
    

---
  #### **Name**
Pod Disruption Budget
  #### **Description**
Ensure minimum availability during voluntary disruptions
  #### **When**
Production workloads that need high availability
  #### **Example**
    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: api-server-pdb
    spec:
      minAvailable: 2  # Or use maxUnavailable: 1
      selector:
        matchLabels:
          app: api-server
    
    # Protects against:
    # - Node drains
    # - Cluster upgrades
    # - Voluntary evictions
    # Does NOT protect against node failures
    

---
  #### **Name**
Network Policy for Zero Trust
  #### **Description**
Restrict pod-to-pod communication by default
  #### **When**
Security-sensitive workloads, compliance requirements
  #### **Example**
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
    # Allow specific traffic
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: allow-api-to-db
    spec:
      podSelector:
        matchLabels:
          app: database
      ingress:
      - from:
        - podSelector:
            matchLabels:
              app: api-server
        ports:
        - port: 5432
    

## Anti-Patterns


---
  #### **Name**
Naked Pods
  #### **Description**
Creating Pods directly instead of using Deployments/StatefulSets
  #### **Why**
Naked pods don't reschedule on node failure. Node dies, pod dies forever. No rolling updates, no rollback, no scaling.
  #### **Instead**
Always use Deployments for stateless, StatefulSets for stateful workloads.

---
  #### **Name**
Latest Tag
  #### **Description**
Using :latest or untagged images in production
  #### **Why**
Non-deterministic deployments. Same manifest produces different results. Rollback doesn't work - you're rolling back to :latest which changed.
  #### **Instead**
Pin exact version tags (v1.2.3). Use image digests for maximum reproducibility.

---
  #### **Name**
Missing Resource Limits
  #### **Description**
Pods without memory and CPU limits
  #### **Why**
One pod memory leaks, consumes all node memory, causes OOMKilled cascade. Scheduler can't make good decisions.
  #### **Instead**
Always set requests AND limits. Monitor actual usage and adjust.

---
  #### **Name**
Root Containers
  #### **Description**
Running containers as root user
  #### **Why**
Container escape vulnerabilities become root on host. One compromise, entire node compromised.
  #### **Instead**
Use runAsNonRoot, runAsUser, readOnlyRootFilesystem in securityContext.

---
  #### **Name**
Secrets in ConfigMaps
  #### **Description**
Storing sensitive data in ConfigMaps instead of Secrets
  #### **Why**
ConfigMaps aren't encrypted at rest. RBAC can't distinguish sensitive data. Audit logs don't flag access.
  #### **Instead**
Use Secrets for sensitive data. Enable encryption at rest. Use external secret managers.

---
  #### **Name**
Hardcoded Replicas with HPA
  #### **Description**
Setting replicas in Deployment when using HorizontalPodAutoscaler
  #### **Why**
Every helm upgrade resets replicas to hardcoded value. HPA scales to 10, helm upgrade drops to 3.
  #### **Instead**
Omit replicas from Deployment when using HPA, or use helm lookup function.