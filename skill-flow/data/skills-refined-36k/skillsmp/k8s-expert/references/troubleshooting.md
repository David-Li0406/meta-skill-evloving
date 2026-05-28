# Kubernetes Troubleshooting Guide

Extended debugging workflows for common k8s issues.

## Pod Lifecycle Issues

### CrashLoopBackOff

```bash
# Get crash reason
kubectl describe pod <pod> -n <ns> | grep -A 5 "Last State"

# Check previous container logs
kubectl logs <pod> -n <ns> --previous

# Common causes:
# - Missing environment variables
# - Failed liveness/readiness probes
# - Application error on startup
# - OOMKilled (check resources)

# Check if OOMKilled
kubectl get pod <pod> -n <ns> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

### ImagePullBackOff

```bash
# Check image name/tag
kubectl describe pod <pod> -n <ns> | grep Image

# Private registry - verify imagePullSecrets
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.imagePullSecrets}'
kubectl get secret <secret> -n <ns> -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d

# Create docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<password> \
  -n <ns>
```

### Pending - Scheduling Issues

```bash
# Check node resources
kubectl describe nodes | grep -A 5 "Allocated resources"

# Check pod requests vs available
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.containers[*].resources}'

# Check node selectors/affinity
kubectl get pod <pod> -n <ns> -o yaml | grep -A 10 nodeSelector
kubectl get pod <pod> -n <ns> -o yaml | grep -A 20 affinity

# Check taints and tolerations
kubectl describe nodes | grep Taints
kubectl get pod <pod> -n <ns> -o yaml | grep -A 10 tolerations
```

## Networking Issues

### DNS Resolution

```bash
# Test DNS from debug pod
kubectl run dns-test --rm -it --image=busybox -- nslookup kubernetes.default

# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns

# Verify service DNS
kubectl run dns-test --rm -it --image=busybox -- nslookup <svc>.<ns>.svc.cluster.local
```

### Service Discovery

```bash
# Verify service has endpoints
kubectl get endpoints <svc> -n <ns>

# If no endpoints:
# 1. Check selector matches pod labels
kubectl get svc <svc> -n <ns> -o jsonpath='{.spec.selector}'
kubectl get pods -n <ns> -l <key>=<value>

# 2. Check pod is Ready
kubectl get pods -n <ns> -o wide

# 3. Check readinessProbe passing
kubectl describe pod <pod> -n <ns> | grep -A 10 Readiness
```

### Network Policies

```bash
# List network policies
kubectl get networkpolicies -n <ns>

# Check policy details
kubectl describe networkpolicy <name> -n <ns>

# Test connectivity
kubectl run nettest --rm -it --image=nicolaka/netshoot -- curl -v http://<svc>.<ns>:port
```

## Storage Issues

### PVC Pending

```bash
# Check PVC status
kubectl describe pvc <name> -n <ns>

# Common issues:
# - No matching StorageClass
# - Insufficient capacity
# - Access mode mismatch

# Check available StorageClasses
kubectl get sc

# Check PV availability (for static provisioning)
kubectl get pv
```

### Volume Mount Errors

```bash
# Check pod events
kubectl describe pod <pod> -n <ns> | grep -A 10 "Events"

# Common errors:
# - "Unable to attach or mount volumes"
# - "FailedMount"

# For NFS issues
kubectl get events -n <ns> --field-selector reason=FailedMount
```

## Resource Issues

### OOMKilled

```bash
# Check memory usage
kubectl top pods -n <ns>

# Check limits
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.containers[*].resources.limits}'

# Increase memory limit or optimize application
```

### CPU Throttling

```bash
# Check CPU usage vs limits
kubectl top pods -n <ns>

# Check CPU limits
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.containers[*].resources.limits.cpu}'

# Symptoms: slow response, high latency
```

## Certificate Issues

### Cert-Manager Troubleshooting

```bash
# Check certificate status
kubectl get certificates -A
kubectl describe certificate <name> -n <ns>

# Check certificate request
kubectl get certificaterequests -n <ns>
kubectl describe certificaterequest <name> -n <ns>

# Check orders (ACME)
kubectl get orders -n <ns>
kubectl describe order <name> -n <ns>

# Check challenges
kubectl get challenges -n <ns>
kubectl describe challenge <name> -n <ns>

# Cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager
```

### Common Certificate Issues

```bash
# DNS01 challenge failing
# - Check external-dns is creating records
# - Verify API token has correct permissions
kubectl logs -n cert-manager -l app=cert-manager | grep -i error

# HTTP01 challenge failing
# - Ingress not routing to solver
# - Check ingress controller logs
```

## ArgoCD Issues

### Sync Failures

```bash
# Check app status
argocd app get <app>

# View sync result
argocd app sync <app> --dry-run

# Check for resource conflicts
kubectl get events -n <ns> --field-selector reason=FailedCreate

# Force sync (careful!)
argocd app sync <app> --force
```

### OutOfSync but No Changes

```bash
# Diff to see what's different
argocd app diff <app>

# Common causes:
# - Resource modified outside GitOps
# - Defaulted fields in cluster
# - Helm chart includes dynamic values

# Hard refresh
argocd app get <app> --hard-refresh
```

## Quick Debug Commands

```bash
# Everything in one namespace
kubectl get all,cm,secret,pvc,ingress -n <ns>

# Recent events
kubectl get events -n <ns> --sort-by='.lastTimestamp' | tail -20

# All pods not Running
kubectl get pods -A | grep -v Running

# Resource usage summary
kubectl top nodes
kubectl top pods -A --sort-by=memory | head -20

# API server logs (for cluster issues)
kubectl logs -n kube-system -l component=kube-apiserver
```
