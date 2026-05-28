# Infra Architect - Sharp Edges

## Hpa Metric Lag

### **Id**
hpa-metric-lag
### **Summary**
HPA scales on 15-second-old metrics, causing oscillation
### **Severity**
high
### **Situation**
Auto-scaling based on CPU or custom metrics
### **Why**
  HPA checks metrics every 15 seconds by default. Under sudden load spikes,
  by the time HPA sees high CPU and scales up, the original pods may already
  be overwhelmed. New pods take 30-60 seconds to start. Meanwhile, HPA sees
  even higher metrics and over-scales. Then load drops, HPA scales down
  aggressively, and the cycle repeats.
  
### **Solution**
  1. Set stabilization windows to prevent thrashing:
     behavior:
       scaleDown:
         stabilizationWindowSeconds: 300  # 5 min before scale down
       scaleUp:
         stabilizationWindowSeconds: 60   # 1 min before scale up
  2. Use predictive scaling for known patterns
  3. Set minReplicas to handle baseline + reasonable spikes
  4. Use PodDisruptionBudgets to limit concurrent terminations
  
### **Symptoms**
  - Pods constantly scaling up and down
  - "0/1 pods ready" during traffic spikes
  - HPA events showing rapid replica changes
### **Detection Pattern**
stabilizationWindowSeconds|behavior:\s*scaleDown

## Termination Grace Period

### **Id**
termination-grace-period
### **Summary**
Pods killed before draining connections
### **Severity**
high
### **Situation**
Deployments with active connections (APIs, websockets)
### **Why**
  Default terminationGracePeriodSeconds is 30s. But your app might need:
  - Time to finish in-flight requests
  - Time to close database connections gracefully
  - Time for load balancer to stop sending traffic
  
  Kubernetes sends SIGTERM, waits grace period, then SIGKILL. If your app
  doesn't handle SIGTERM or needs more time, connections are severed mid-request.
  
### **Solution**
  1. Set grace period longer than your longest request:
     terminationGracePeriodSeconds: 60
  2. Add preStop hook to delay shutdown:
     lifecycle:
       preStop:
         exec:
           command: ["/bin/sh", "-c", "sleep 10"]
  3. Handle SIGTERM in your app - stop accepting new connections
  4. Configure readiness probe to fail on shutdown
  
### **Symptoms**
  - 502/504 errors during deployments
  - "connection reset by peer" in client logs
  - Database connection pool errors during shutdown
### **Detection Pattern**
terminationGracePeriodSeconds|preStop

## Pvc Zone Affinity

### **Id**
pvc-zone-affinity
### **Summary**
Pod stuck Pending because PVC is in different zone
### **Severity**
high
### **Situation**
StatefulSets or pods using PersistentVolumeClaims
### **Why**
  Cloud provider disks (AWS EBS, GCP PD) are zone-specific. If you create
  a PVC in us-east-1a, only pods in us-east-1a can mount it. If that zone
  goes down or has no capacity, pod is stuck forever pending.
  
### **Solution**
  1. Use regional PVs where available (GCP regional PD)
  2. Set pod anti-affinity to spread across zones
  3. Use volumeBindingMode: WaitForFirstConsumer
     storageClass:
       volumeBindingMode: WaitForFirstConsumer
  4. For databases, use operator-managed replication across zones
  
### **Symptoms**
  - Pod stuck in Pending state
  - Events showing "node(s) had volume node affinity conflict"
  - Pod scheduled to different zone than PVC
### **Detection Pattern**
volumeBindingMode|WaitForFirstConsumer

## Terraform State Corruption

### **Id**
terraform-state-corruption
### **Summary**
Concurrent Terraform runs corrupt state file
### **Severity**
critical
### **Situation**
Multiple team members or CI pipelines running Terraform
### **Why**
  Terraform state is a single file tracking infrastructure. Two concurrent
  runs can read the same state, make different changes, and overwrite each
  other. Result: state no longer matches reality. Resources orphaned,
  duplicated, or destroyed unexpectedly.
  
### **Solution**
  1. Use remote state with locking:
     terraform {
       backend "s3" {
         bucket         = "tf-state"
         key            = "prod/terraform.tfstate"
         region         = "us-east-1"
         dynamodb_table = "tf-locks"  # Locking!
         encrypt        = true
       }
     }
  2. Never run terraform apply locally for shared infra
  3. Use CI/CD with single execution at a time
  4. Enable state file versioning for recovery
  
### **Symptoms**
  - Error acquiring state lock
  - Resources exist but not in state
  - Resources in state but deleted in cloud
### **Detection Pattern**
dynamodb_table|state.*lock

## Configmap Update No Restart

### **Id**
configmap-update-no-restart
### **Summary**
ConfigMap changes don't trigger pod restart
### **Severity**
medium
### **Situation**
Using ConfigMaps for application configuration
### **Why**
  ConfigMaps mounted as volumes eventually update (kubelet sync period,
  typically 1 minute). But ConfigMaps mounted as env vars NEVER update
  without pod restart. Your app might be running with stale config for
  days without anyone noticing.
  
### **Solution**
  1. Use Reloader to watch ConfigMaps and restart pods:
     annotations:
       reloader.stakater.com/auto: "true"
  2. Add config hash to deployment template:
     annotations:
       checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
  3. Use volume mounts instead of env vars for live updates
  4. Implement config watch in your application
  
### **Symptoms**
  - Config changes not taking effect
  - Pods running with old configuration
  - Inconsistent behavior across pods
### **Detection Pattern**
reloader|checksum/config|configmap.*env

## Ingress Class Missing

### **Id**
ingress-class-missing
### **Summary**
Ingress created but no controller processes it
### **Severity**
medium
### **Situation**
Creating Ingress resources for external access
### **Why**
  Multiple ingress controllers can run in a cluster (nginx, traefik, istio).
  Without ingressClassName, it's ambiguous which controller should handle it.
  Some controllers ignore unmarked ingresses, some fight over them, some
  process all of them creating duplicate load balancers.
  
### **Solution**
  1. Always specify ingressClassName:
     spec:
       ingressClassName: nginx
  2. Set default ingress class in cluster
  3. Use controller-specific annotations when needed
  4. Check which controllers are running: kubectl get ingressclass
  
### **Symptoms**
  - Ingress shows no ADDRESS
  - Multiple load balancers created for same ingress
  - DNS pointing to wrong IP
### **Detection Pattern**
ingressClassName|kubernetes.io/ingress.class

## Node Selector No Spread

### **Id**
node-selector-no-spread
### **Summary**
All pods scheduled to same node, single point of failure
### **Severity**
medium
### **Situation**
Deployments without topology constraints
### **Why**
  Kubernetes scheduler optimizes for resource utilization. Without
  constraints, it may pack all replicas onto one node - more efficient!
  Until that node fails and all your replicas go down together.
  
### **Solution**
  1. Use pod anti-affinity:
     affinity:
       podAntiAffinity:
         preferredDuringSchedulingIgnoredDuringExecution:
           - weight: 100
             podAffinityTerm:
               labelSelector:
                 matchLabels:
                   app: my-app
               topologyKey: kubernetes.io/hostname
  2. Use topology spread constraints:
     topologySpreadConstraints:
       - maxSkew: 1
         topologyKey: topology.kubernetes.io/zone
         whenUnsatisfiable: DoNotSchedule
  
### **Symptoms**
  - All pods on same node (kubectl get pods -o wide)
  - Complete outage when single node fails
  - Uneven resource utilization across nodes
### **Detection Pattern**
podAntiAffinity|topologySpreadConstraints

## Image Pull Backoff

### **Id**
image-pull-backoff
### **Summary**
ImagePullBackOff in production because registry auth not configured
### **Severity**
high
### **Situation**
Deploying from private container registries
### **Why**
  Works in dev because you're logged in locally. Fails in production
  because Kubernetes nodes don't have your docker credentials. Or
  imagePullSecrets reference a secret that doesn't exist in that namespace.
  
### **Solution**
  1. Create imagePullSecrets in every namespace:
     kubectl create secret docker-registry regcred \
       --docker-server=gcr.io \
       --docker-username=_json_key \
       --docker-password="$(cat key.json)"
  2. Reference in ServiceAccount for automatic use:
     apiVersion: v1
     kind: ServiceAccount
     metadata:
       name: default
     imagePullSecrets:
       - name: regcred
  3. Use workload identity instead of static credentials
  4. Sync secrets across namespaces with external-secrets
  
### **Symptoms**
  - ImagePullBackOff status
  - "unauthorized" or "not found" in pod events
  - Works locally but fails in cluster
### **Detection Pattern**
imagePullSecrets|docker-registry