# Kubernetes Infrastructure Reference

ArgoCD GitOps patterns, Helm configurations, and k3s homelab setup for this repository.

## Directory Structure

```
k8s/
├── argocd/
│   ├── app-of-apps.yaml          # Root application
│   ├── apps/                     # ArgoCD Application manifests
│   │   ├── cert-manager.yaml
│   │   ├── external-dns.yaml
│   │   ├── cloudflared.yaml
│   │   └── ...
│   ├── cluster-issuer/           # Cert-manager issuers
│   ├── external-secrets/         # ExternalSecrets store
│   ├── cloudflared/              # Cloudflare tunnel config
│   └── {app-name}/               # Per-app configs
│       ├── values.yaml           # Helm values
│       ├── secrets/              # ExternalSecret manifests
│       └── *.yaml                # Raw manifests
└── terraform/
    ├── main.tf                   # Root module
    ├── argocd/                   # ArgoCD Helm deployment
    └── metallb-config/           # MetalLB configuration
```

## ArgoCD Patterns

### App of Apps Pattern
Root application that manages other applications:

```yaml
# k8s/argocd/app-of-apps.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-of-apps
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/peterstorm/.dotfiles.git
    targetRevision: HEAD
    path: k8s/argocd/apps  # Directory containing Application manifests
  destination:
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Helm Chart Application
```yaml
# k8s/argocd/apps/my-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  sources:
  # Helm chart source
  - repoURL: https://charts.example.com
    targetRevision: 1.0.0
    chart: my-chart
    helm:
      valueFiles:
      - $values/k8s/argocd/my-app/values.yaml
  # Values file reference
  - repoURL: https://github.com/peterstorm/.dotfiles.git
    targetRevision: HEAD
    ref: values
  # Additional manifests (secrets, etc.)
  - repoURL: https://github.com/peterstorm/.dotfiles.git
    targetRevision: HEAD
    path: k8s/argocd/my-app/secrets
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Raw Manifests Application
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: echo-server
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/peterstorm/.dotfiles.git
    targetRevision: HEAD
    path: k8s/argocd/echo-server  # Contains deployment.yaml, service.yaml, etc.
  destination:
    server: https://kubernetes.default.svc
    namespace: echo-server
```

## External Secrets

### ClusterSecretStore (Azure Key Vault)
```yaml
# k8s/argocd/external-secrets/cluster-secret-store.yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: azure-store
spec:
  provider:
    azurekv:
      tenantId: "tenant-id"
      vaultUrl: "https://homelab-k8s.vault.azure.net/"
      authSecretRef:
        clientId:
          name: azure-secret-sp
          key: ClientID
          namespace: default
        clientSecret:
          name: azure-secret-sp
          key: ClientSecret
          namespace: default
```

### ExternalSecret Example
```yaml
# k8s/argocd/my-app/secrets/my-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: my-secret
spec:
  refreshInterval: 0h  # 0h = never refresh (manual only)
  secretStoreRef:
    kind: ClusterSecretStore
    name: azure-store
  target:
    name: my-secret  # Name of generated K8s Secret
  data:
    - secretKey: api-token     # Key in K8s Secret
      remoteRef:
        key: my-azure-secret   # Key in Azure Key Vault
```

## Cert-Manager

### ClusterIssuer with Cloudflare DNS-01
```yaml
# k8s/argocd/cluster-issuer/letsencrypt-prod.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your@email.com
    privateKeySecretRef:
      name: letsencrypt-prod-private-key
    solvers:
      - dns01:
          cloudflare:
            email: your@email.com
            apiTokenSecretRef:
              name: cloudflare-api-token-secret
              key: api-token
```

### Ingress with TLS
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    external-dns.alpha.kubernetes.io/target: homelab-tunnel.peterstorm.io
    external-dns.alpha.kubernetes.io/cloudflare-proxied: 'true'
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - my-app.peterstorm.io
    secretName: my-app-tls
  rules:
  - host: my-app.peterstorm.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

## Cloudflared Tunnel

### Values Configuration
```yaml
# k8s/argocd/cloudflared/values.yaml
cloudflare:
  tunnelName: homelab-k8s
  secretName: cloudflared-credentials  # From ExternalSecret
  ingress:
    - hostname: '*.peterstorm.io'
      service: https://ingress-nginx-controller.ingress-nginx
      originRequest:
        noTLSVerify: true
image:
  repository: cloudflare/cloudflared
  tag: "2024.1.2"
```

## Terraform Infrastructure

### Main Configuration
```hcl
# k8s/terraform/main.tf
provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

module "metallb" {
  source = "./metallb-config"
}

module "argocd" {
  source = "./argocd"
  depends_on = [module.metallb]
}
```

### MetalLB Configuration
```hcl
# k8s/terraform/metallb-config/main.tf
resource "helm_release" "metallb" {
  name             = "metallb"
  repository       = "https://metallb.github.io/metallb"
  chart            = "metallb"
  namespace        = "metallb-system"
  create_namespace = true
  version          = "0.13.12"
}

resource "kubectl_manifest" "ipaddresspool" {
  yaml_body = file("./metallb-config/metallb-ipaddresspool.yaml")
  depends_on = [helm_release.metallb]
}
```

### IP Address Pool
```yaml
# k8s/terraform/metallb-config/metallb-ipaddresspool.yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: metallb-ipaddress-pool
  namespace: metallb-system
spec:
  addresses:
    - 192.168.0.240-192.168.0.250
```

## k3s NixOS Role

```nix
# roles/k3s/default.nix
{ config, pkgs, lib, ... }:
{
  services.k3s = {
    enable = true;
    role = "server";
    extraFlags = "--disable servicelb --disable traefik --write-kubeconfig-mode=644";
  };
}
```

Key flags:
- `--disable servicelb`: Use MetalLB instead
- `--disable traefik`: Use nginx-ingress instead
- `--write-kubeconfig-mode=644`: Allow non-root kubeconfig access

## Adding New Applications

1. **Create app directory**: `k8s/argocd/my-app/`

2. **Add values.yaml** (for Helm charts):
```yaml
# k8s/argocd/my-app/values.yaml
replicaCount: 1
image:
  repository: myimage
  tag: latest
```

3. **Create secrets** (if needed):
```yaml
# k8s/argocd/my-app/secrets/my-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
# ... (see pattern above)
```

4. **Create Application manifest**:
```yaml
# k8s/argocd/apps/my-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
# ... (see patterns above)
```

5. **Commit and push** - ArgoCD auto-syncs via app-of-apps

## Common Commands

```bash
# Apply app-of-apps (initial setup)
kubectl apply -f k8s/argocd/app-of-apps.yaml

# Check ArgoCD app status
kubectl -n argocd get applications

# Force sync
argocd app sync my-app

# Get app logs
argocd app logs my-app

# Terraform
cd k8s/terraform
terraform init
terraform plan
terraform apply

# k3s kubeconfig
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```
