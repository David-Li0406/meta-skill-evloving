# Homelab Components

Additional k8s components used in this repo's homelab setup.

## MetalLB (Load Balancer)

Bare-metal load balancer for k3s. Config in `k8s/terraform/metallb-config/`.

### IP Address Pool

```yaml
# metallb-ipaddresspool.yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default-pool
  namespace: metallb-system
spec:
  addresses:
    - 192.168.1.200-192.168.1.250  # range for LoadBalancer IPs
```

### L2 Advertisement

```yaml
# metallb-l2advertisement.yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: default
  namespace: metallb-system
spec:
  ipAddressPools:
    - default-pool
```

### Troubleshooting MetalLB

```bash
# Check speaker pods (one per node)
kubectl get pods -n metallb-system

# Check IP assignments
kubectl get svc -A | grep LoadBalancer

# Verify pool has available IPs
kubectl get ipaddresspool -n metallb-system -o yaml

# Check for conflicts (another device using the IP)
arping -I <interface> <assigned-ip>
```

## External-DNS

Automatic DNS record management. Creates DNS records for Ingress/Service resources.

### Cloudflare Integration

```yaml
# values.yaml for external-dns helm chart
provider: cloudflare
env:
  - name: CF_API_TOKEN
    valueFrom:
      secretKeyRef:
        name: cloudflare-api-token
        key: api-token
sources:
  - ingress
  - service
domainFilters:
  - example.com
txtOwnerId: "k3s-cluster"  # identifies records managed by this cluster
policy: sync  # sync = create/update/delete, upsert-only = no delete
```

### Troubleshooting External-DNS

```bash
# Check external-dns logs
kubectl logs -n external-dns -l app.kubernetes.io/name=external-dns

# Verify DNS records created
dig @1.1.1.1 app.example.com

# Check annotations on ingress
kubectl get ingress <name> -n <ns> -o yaml | grep -A5 annotations

# Common issues:
# - Missing annotation: external-dns.alpha.kubernetes.io/hostname
# - Wrong domain filter (domain not in domainFilters)
# - API token permissions (needs Zone:Read and DNS:Edit)
```

### Ingress Annotations

```yaml
metadata:
  annotations:
    # Explicit hostname (optional, uses spec.rules[].host by default)
    external-dns.alpha.kubernetes.io/hostname: app.example.com
    # TTL for DNS record
    external-dns.alpha.kubernetes.io/ttl: "300"
    # Target override (useful for CNAME to tunnel)
    external-dns.alpha.kubernetes.io/target: tunnel.example.com
```

## Cloudflared (Tunnel)

Secure tunnel to expose services without opening ports. No inbound firewall rules needed.

### How It Works

```
Internet -> Cloudflare Edge -> Tunnel -> cloudflared pod -> k8s Service
```

### Deployment Pattern

```yaml
# values.yaml for cloudflared
tunnel: <tunnel-id>
credentials:
  secretName: cloudflared-credentials
config:
  ingress:
    - hostname: app.example.com
      service: http://app-service.namespace:80
    - hostname: api.example.com
      service: http://api-service.namespace:8080
    - service: http_status:404  # catch-all
```

### Creating Tunnel

```bash
# Login to Cloudflare
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create <tunnel-name>
# Outputs: Created tunnel <tunnel-name> with id <tunnel-id>

# Get credentials file
cat ~/.cloudflared/<tunnel-id>.json
# Store this as k8s secret

# Create DNS CNAME (or use external-dns)
cloudflared tunnel route dns <tunnel-name> app.example.com
```

### Troubleshooting Cloudflared

```bash
# Check tunnel status
kubectl logs -n cloudflared -l app=cloudflared

# Verify tunnel connected
cloudflared tunnel info <tunnel-name>

# Test from inside cluster
kubectl run curl --rm -it --image=curlimages/curl -- curl -v http://app-service.namespace

# Common issues:
# - Credentials secret missing/wrong
# - Service hostname/port mismatch in config
# - DNS not pointing to tunnel (should be CNAME to <tunnel-id>.cfargotunnel.com)
```

### Combined External-DNS + Cloudflared

For tunnel-based services, external-dns creates CNAME to tunnel:

```yaml
# Ingress annotation to point DNS at tunnel
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/target: <tunnel-id>.cfargotunnel.com
```

This makes external-dns create:
```
app.example.com CNAME <tunnel-id>.cfargotunnel.com
```

## k9s (Terminal UI)

Recommended TUI for k8s management. Not deployed in cluster, run locally.

```bash
# Install
brew install k9s  # macOS
nix-env -iA nixpkgs.k9s  # nix

# Usage
k9s                    # default context
k9s -n <namespace>     # specific namespace
k9s --context <ctx>    # specific context

# Key bindings
:pods                  # switch to pods view
:svc                   # services
:deploy                # deployments
:logs                  # logs for selected pod
/pattern               # filter
d                      # describe
l                      # logs
s                      # shell
ctrl-d                 # delete
```
