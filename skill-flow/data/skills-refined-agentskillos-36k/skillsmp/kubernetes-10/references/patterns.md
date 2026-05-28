# Kubernetes & Container Orchestration

## Patterns


---
  #### **Name**
Basic Deployment
  #### **Description**
Production-ready deployment with all required fields
  #### **When**
Deploying any application
  #### **Example**
    # PRODUCTION DEPLOYMENT:
    
    """
    Every production deployment needs:
    1. Resource limits
    2. Health checks
    3. Security context
    4. Labels for selection
    """
    
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-app
      namespace: production
      labels:
        app: my-app
        version: v1.0.0
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: my-app
      template:
        metadata:
          labels:
            app: my-app
            version: v1.0.0
        spec:
          # Security: Don't run as root
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            fsGroup: 1000
    
          containers:
            - name: my-app
              image: myregistry/my-app:v1.0.0
              imagePullPolicy: IfNotPresent
    
              ports:
                - containerPort: 3000
                  name: http
    
              # Resource limits (REQUIRED)
              resources:
                requests:
                  cpu: 100m
                  memory: 128Mi
                limits:
                  cpu: 500m
                  memory: 512Mi
    
              # Startup probe (for slow-starting apps)
              startupProbe:
                httpGet:
                  path: /health
                  port: http
                failureThreshold: 30
                periodSeconds: 10
    
              # Liveness probe (is the container alive?)
              livenessProbe:
                httpGet:
                  path: /health
                  port: http
                initialDelaySeconds: 0
                periodSeconds: 10
                timeoutSeconds: 5
                failureThreshold: 3
    
              # Readiness probe (can it receive traffic?)
              readinessProbe:
                httpGet:
                  path: /ready
                  port: http
                initialDelaySeconds: 5
                periodSeconds: 5
                timeoutSeconds: 3
                failureThreshold: 3
    
              # Environment from ConfigMap and Secret
              envFrom:
                - configMapRef:
                    name: my-app-config
                - secretRef:
                    name: my-app-secrets
    
              # Container security
              securityContext:
                allowPrivilegeEscalation: false
                readOnlyRootFilesystem: true
                capabilities:
                  drop:
                    - ALL
    

---
  #### **Name**
Service and Ingress
  #### **Description**
Expose application to network
  #### **When**
Making app accessible
  #### **Example**
    # SERVICE (internal load balancer):
    
    apiVersion: v1
    kind: Service
    metadata:
      name: my-app
      namespace: production
    spec:
      type: ClusterIP
      selector:
        app: my-app
      ports:
        - port: 80
          targetPort: http
          protocol: TCP
          name: http
    
    
    ---
    # INGRESS (external access):
    
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: my-app
      namespace: production
      annotations:
        # For nginx ingress controller
        nginx.ingress.kubernetes.io/rewrite-target: /
        # For cert-manager TLS
        cert-manager.io/cluster-issuer: letsencrypt-prod
    spec:
      ingressClassName: nginx
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
                    name: my-app
                    port:
                      number: 80
    

---
  #### **Name**
ConfigMaps and Secrets
  #### **Description**
External configuration
  #### **When**
App needs configuration
  #### **Example**
    # CONFIGMAP (non-sensitive config):
    
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: my-app-config
      namespace: production
    data:
      NODE_ENV: production
      LOG_LEVEL: info
      API_URL: https://api.example.com
    
    
    ---
    # SECRET (sensitive data):
    
    """
    IMPORTANT: Secrets are base64 encoded, NOT encrypted!
    Anyone with cluster access can decode them.
    Use external secrets managers for real security.
    """
    
    apiVersion: v1
    kind: Secret
    metadata:
      name: my-app-secrets
      namespace: production
    type: Opaque
    stringData:  # Will be base64 encoded automatically
      DATABASE_URL: postgresql://user:pass@db:5432/app
      API_KEY: sk_live_xxxxx
    
    
    ---
    # Using secrets securely in pods:
    
    env:
      - name: DATABASE_URL
        valueFrom:
          secretKeyRef:
            name: my-app-secrets
            key: DATABASE_URL
    
    # Or mount as file (more secure than env vars):
    volumes:
      - name: secrets
        secret:
          secretName: my-app-secrets
    volumeMounts:
      - name: secrets
        mountPath: /etc/secrets
        readOnly: true
    

---
  #### **Name**
Horizontal Pod Autoscaler
  #### **Description**
Auto-scale based on metrics
  #### **When**
Need to handle variable load
  #### **Example**
    # HPA (autoscaling):
    
    """
    Scale based on CPU, memory, or custom metrics.
    Requires metrics-server in cluster.
    """
    
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: my-app-hpa
      namespace: production
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: my-app
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
          stabilizationWindowSeconds: 300  # Wait 5 min before scale down
          policies:
            - type: Percent
              value: 10
              periodSeconds: 60
        scaleUp:
          stabilizationWindowSeconds: 0  # Scale up immediately
          policies:
            - type: Percent
              value: 100
              periodSeconds: 15
    
    
    # Also set PodDisruptionBudget:
    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: my-app-pdb
      namespace: production
    spec:
      minAvailable: 1  # Or use maxUnavailable
      selector:
        matchLabels:
          app: my-app
    

---
  #### **Name**
Helm Chart Structure
  #### **Description**
Package K8s manifests
  #### **When**
Reusable deployment
  #### **Example**
    # HELM CHART:
    
    """
    Helm packages Kubernetes manifests with templating.
    Great for reusable deployments across environments.
    """
    
    # Chart structure:
    my-app/
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
        └── hpa.yaml
    
    
    # Chart.yaml
    apiVersion: v2
    name: my-app
    description: My Application Helm Chart
    version: 1.0.0
    appVersion: "1.0.0"
    
    
    # values.yaml (defaults)
    replicaCount: 2
    
    image:
      repository: myregistry/my-app
      tag: latest
      pullPolicy: IfNotPresent
    
    service:
      type: ClusterIP
      port: 80
    
    ingress:
      enabled: true
      host: myapp.example.com
    
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 512Mi
    
    
    # templates/deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: {{ include "my-app.fullname" . }}
      labels:
        {{- include "my-app.labels" . | nindent 4 }}
    spec:
      replicas: {{ .Values.replicaCount }}
      selector:
        matchLabels:
          {{- include "my-app.selectorLabels" . | nindent 6 }}
      template:
        spec:
          containers:
            - name: {{ .Chart.Name }}
              image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
              resources:
                {{- toYaml .Values.resources | nindent 12 }}
    
    
    # Install with:
    helm install my-app ./my-app -f values-production.yaml
    

---
  #### **Name**
Kustomize Overlays
  #### **Description**
Environment-specific customization
  #### **When**
Different configs per environment
  #### **Example**
    # KUSTOMIZE:
    
    """
    Kustomize patches base manifests for different environments.
    Built into kubectl: kubectl apply -k overlays/production
    """
    
    # Directory structure:
    my-app/
    ├── base/
    │   ├── kustomization.yaml
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   └── configmap.yaml
    └── overlays/
        ├── staging/
        │   ├── kustomization.yaml
        │   └── patch-replicas.yaml
        └── production/
            ├── kustomization.yaml
            ├── patch-replicas.yaml
            └── patch-resources.yaml
    
    
    # base/kustomization.yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    
    resources:
      - deployment.yaml
      - service.yaml
      - configmap.yaml
    
    
    # overlays/production/kustomization.yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    
    namespace: production
    
    resources:
      - ../../base
    
    patches:
      - path: patch-replicas.yaml
      - path: patch-resources.yaml
    
    configMapGenerator:
      - name: my-app-config
        behavior: merge
        literals:
          - NODE_ENV=production
    
    images:
      - name: myregistry/my-app
        newTag: v1.2.3
    
    
    # overlays/production/patch-replicas.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-app
    spec:
      replicas: 5
    
    
    # Apply:
    kubectl apply -k overlays/production
    

## Anti-Patterns


---
  #### **Name**
No Resource Limits
  #### **Description**
Pods without CPU/memory limits
  #### **Why**
    Without limits, one pod can consume all node resources and affect
    other pods. In multi-tenant clusters, this is a nightmare. Your
    pod might also get OOMKilled unpredictably.
    
  #### **Instead**
    # Always set both requests and limits
    resources:
      requests:      # Scheduler uses for placement
        cpu: 100m
        memory: 128Mi
      limits:        # Enforced at runtime
        cpu: 500m
        memory: 512Mi
    

---
  #### **Name**
No Health Checks
  #### **Description**
Pods without liveness/readiness probes
  #### **Why**
    Without probes, Kubernetes can't tell if your app is healthy.
    Dead apps keep receiving traffic. Rolling updates can cause
    downtime. You lose the main benefit of orchestration.
    
  #### **Instead**
    # Three types of probes:
    startupProbe:    # For slow-starting apps
    livenessProbe:   # Is the process alive?
    readinessProbe:  # Can it handle traffic?
    

---
  #### **Name**
Using :latest Tag
  #### **Description**
Deploying with :latest image tag
  #### **Why**
    :latest is a moving target. Deployments become non-reproducible.
    Rollbacks don't work. You can't tell what's running. ImagePullPolicy
    defaults might not pull the new version.
    
  #### **Instead**
    # Use specific tags
    image: myregistry/my-app:v1.2.3
    
    # Or use SHA
    image: myregistry/my-app@sha256:abc123...
    

---
  #### **Name**
Secrets in ConfigMaps
  #### **Description**
Putting sensitive data in ConfigMaps
  #### **Why**
    ConfigMaps are not encrypted and often logged/displayed. Secrets
    at least get base64 encoding and can have RBAC restrictions.
    
  #### **Instead**
    # Use Secrets for sensitive data
    # Better: Use external secrets manager
    # Best: Use sealed-secrets or external-secrets operator
    

---
  #### **Name**
kubectl apply from Laptop
  #### **Description**
Deploying manually from local machine
  #### **Why**
    No audit trail, no review process, no reproducibility. "It worked
    on my laptop" becomes "it worked when I deployed it." Drift
    between what's in Git and what's running.
    
  #### **Instead**
    # Use GitOps
    - Store manifests in Git
    - Use ArgoCD or Flux
    - CI/CD deploys, not humans
    