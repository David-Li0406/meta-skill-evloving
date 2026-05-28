# Infrastructure Architect

## Patterns


---
  #### **Name**
GitOps Deployment Pipeline
  #### **Description**
ArgoCD-based continuous deployment with progressive rollouts
  #### **When**
Any production deployment to Kubernetes
  #### **Example**
    # Application manifest with ArgoCD
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: memory-service-api
      namespace: argocd
    spec:
      project: production
      source:
        repoURL: https://github.com/org/memory-service-manifests
        targetRevision: main
        path: apps/api/overlays/production
      destination:
        server: https://kubernetes.default.svc
        namespace: memory-service
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
          - PrunePropagationPolicy=foreground
        retry:
          limit: 5
          backoff:
            duration: 5s
            factor: 2
            maxDuration: 3m
    
    ---
    # Rollout strategy with Argo Rollouts
    apiVersion: argoproj.io/v1alpha1
    kind: Rollout
    metadata:
      name: memory-service-api
    spec:
      replicas: 5
      strategy:
        canary:
          steps:
            - setWeight: 10
            - pause: {duration: 5m}
            - setWeight: 30
            - pause: {duration: 5m}
            - setWeight: 50
            - pause: {duration: 10m}
          analysis:
            templates:
              - templateName: success-rate
            startingStep: 2
      selector:
        matchLabels:
          app: memory-service-api
      template:
        metadata:
          labels:
            app: memory-service-api
        spec:
          containers:
            - name: api
              image: memory-service-api:v1.2.3
              resources:
                requests:
                  memory: "256Mi"
                  cpu: "100m"
                limits:
                  memory: "512Mi"
                  cpu: "500m"
              livenessProbe:
                httpGet:
                  path: /health/live
                  port: 8080
                initialDelaySeconds: 10
                periodSeconds: 10
              readinessProbe:
                httpGet:
                  path: /health/ready
                  port: 8080
                initialDelaySeconds: 5
                periodSeconds: 5
    

---
  #### **Name**
Terraform Module Structure
  #### **Description**
Reusable, composable infrastructure modules
  #### **When**
Creating or organizing Terraform code
  #### **Example**
    # Module structure
    # modules/
    #   kubernetes-cluster/
    #     main.tf
    #     variables.tf
    #     outputs.tf
    #     versions.tf
    #   networking/
    #   database/
    
    # modules/kubernetes-cluster/main.tf
    resource "google_container_cluster" "primary" {
      name     = var.cluster_name
      location = var.region
    
      # Use separately managed node pool
      remove_default_node_pool = true
      initial_node_count       = 1
    
      # Network configuration
      network    = var.network
      subnetwork = var.subnetwork
    
      # Private cluster
      private_cluster_config {
        enable_private_nodes    = true
        enable_private_endpoint = var.private_endpoint
        master_ipv4_cidr_block  = var.master_cidr
      }
    
      # Workload identity
      workload_identity_config {
        workload_pool = "${var.project_id}.svc.id.goog"
      }
    
      # Security
      master_authorized_networks_config {
        dynamic "cidr_blocks" {
          for_each = var.authorized_networks
          content {
            cidr_block   = cidr_blocks.value.cidr
            display_name = cidr_blocks.value.name
          }
        }
      }
    
      # Maintenance window
      maintenance_policy {
        recurring_window {
          start_time = "2024-01-01T04:00:00Z"
          end_time   = "2024-01-01T08:00:00Z"
          recurrence = "FREQ=WEEKLY;BYDAY=SA,SU"
        }
      }
    }
    
    resource "google_container_node_pool" "primary" {
      name       = "${var.cluster_name}-primary"
      location   = var.region
      cluster    = google_container_cluster.primary.name
      node_count = var.node_count
    
      autoscaling {
        min_node_count = var.min_nodes
        max_node_count = var.max_nodes
      }
    
      node_config {
        machine_type = var.machine_type
        disk_size_gb = var.disk_size
    
        # Security
        workload_metadata_config {
          mode = "GKE_METADATA"
        }
    
        shielded_instance_config {
          enable_secure_boot = true
        }
    
        oauth_scopes = [
          "https://www.googleapis.com/auth/cloud-platform"
        ]
      }
    }
    
    # modules/kubernetes-cluster/variables.tf
    variable "cluster_name" {
      description = "Name of the GKE cluster"
      type        = string
    }
    
    variable "region" {
      description = "GCP region"
      type        = string
    }
    
    variable "node_count" {
      description = "Initial node count per zone"
      type        = number
      default     = 1
    }
    
    variable "min_nodes" {
      description = "Minimum nodes for autoscaling"
      type        = number
      default     = 1
    }
    
    variable "max_nodes" {
      description = "Maximum nodes for autoscaling"
      type        = number
      default     = 10
    }
    

---
  #### **Name**
Service Mesh Configuration
  #### **Description**
Istio service mesh for traffic management and security
  #### **When**
Implementing mTLS, traffic routing, or observability at network level
  #### **Example**
    # Strict mTLS for namespace
    apiVersion: security.istio.io/v1beta1
    kind: PeerAuthentication
    metadata:
      name: default
      namespace: memory-service
    spec:
      mtls:
        mode: STRICT
    
    ---
    # Virtual Service for traffic management
    apiVersion: networking.istio.io/v1beta1
    kind: VirtualService
    metadata:
      name: memory-service-api
      namespace: memory-service
    spec:
      hosts:
        - memory-service-api
      http:
        - match:
            - headers:
                x-canary:
                  exact: "true"
          route:
            - destination:
                host: memory-service-api
                subset: canary
        - route:
            - destination:
                host: memory-service-api
                subset: stable
              weight: 100
          retries:
            attempts: 3
            perTryTimeout: 2s
            retryOn: 5xx,reset,connect-failure
          timeout: 10s
    
    ---
    # Destination Rule with circuit breaking
    apiVersion: networking.istio.io/v1beta1
    kind: DestinationRule
    metadata:
      name: memory-service-api
      namespace: memory-service
    spec:
      host: memory-service-api
      trafficPolicy:
        connectionPool:
          tcp:
            maxConnections: 100
          http:
            h2UpgradePolicy: UPGRADE
            http1MaxPendingRequests: 100
            http2MaxRequests: 1000
        outlierDetection:
          consecutive5xxErrors: 5
          interval: 30s
          baseEjectionTime: 30s
          maxEjectionPercent: 50
      subsets:
        - name: stable
          labels:
            version: stable
        - name: canary
          labels:
            version: canary
    

---
  #### **Name**
Kubernetes Security Hardening
  #### **Description**
Pod security, RBAC, and network policies
  #### **When**
Securing Kubernetes workloads
  #### **Example**
    # Pod Security Standards (Restricted)
    apiVersion: v1
    kind: Namespace
    metadata:
      name: memory-service
      labels:
        pod-security.kubernetes.io/enforce: restricted
        pod-security.kubernetes.io/audit: restricted
        pod-security.kubernetes.io/warn: restricted
    
    ---
    # RBAC for application
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: memory-service-api
      namespace: memory-service
    
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: memory-service-api
      namespace: memory-service
    rules:
      - apiGroups: [""]
        resources: ["configmaps"]
        verbs: ["get", "list", "watch"]
      - apiGroups: [""]
        resources: ["secrets"]
        resourceNames: ["memory-service-api-secrets"]
        verbs: ["get"]
    
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: memory-service-api
      namespace: memory-service
    subjects:
      - kind: ServiceAccount
        name: memory-service-api
    roleRef:
      kind: Role
      name: memory-service-api
      apiGroup: rbac.authorization.k8s.io
    
    ---
    # Network Policy - default deny
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: default-deny-all
      namespace: memory-service
    spec:
      podSelector: {}
      policyTypes:
        - Ingress
        - Egress
    
    ---
    # Network Policy - allow specific traffic
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: memory-service-api
      namespace: memory-service
    spec:
      podSelector:
        matchLabels:
          app: memory-service-api
      policyTypes:
        - Ingress
        - Egress
      ingress:
        - from:
            - namespaceSelector:
                matchLabels:
                  name: istio-system
          ports:
            - protocol: TCP
              port: 8080
      egress:
        - to:
            - namespaceSelector:
                matchLabels:
                  name: memory-service
          ports:
            - protocol: TCP
              port: 5432  # PostgreSQL
        - to:
            - namespaceSelector: {}
          ports:
            - protocol: UDP
              port: 53  # DNS
    

## Anti-Patterns


---
  #### **Name**
kubectl apply from Laptop
  #### **Description**
Deploying directly from developer machines
  #### **Why**
No audit trail, no review, no consistency. GitOps exists for a reason.
  #### **Instead**
All changes through Git, ArgoCD syncs from repo

---
  #### **Name**
No Resource Limits
  #### **Description**
Pods without CPU/memory limits
  #### **Why**
One runaway pod can starve the entire node. OOMKiller picks victims randomly.
  #### **Instead**
Always set requests AND limits, use LimitRanges as defaults

---
  #### **Name**
Running as Root
  #### **Description**
Containers running as root user
  #### **Why**
Container escape + root = full node compromise. Defense in depth.
  #### **Instead**
Use non-root users, drop capabilities, use securityContext

---
  #### **Name**
Latest Tag in Production
  #### **Description**
Using :latest instead of specific versions
  #### **Why**
No reproducibility, no rollback capability, surprise changes.
  #### **Instead**
Use immutable tags, digest pinning for critical images

---
  #### **Name**
Secrets in ConfigMaps
  #### **Description**
Storing sensitive data in ConfigMaps
  #### **Why**
ConfigMaps are not encrypted at rest, visible in logs, no access control.
  #### **Instead**
Use Secrets with encryption, external secrets operator, vault