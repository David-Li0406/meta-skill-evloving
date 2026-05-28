# ArgoCD Repository Configuration

## HTTPS Authentication

### Username/Password or Token

```bash
# GitHub/GitLab token (use token as password, any username)
argocd repo add https://github.com/org/repo.git \
  --username git \
  --password ghp_xxxxxxxxxxxx

# Basic auth
argocd repo add https://git.example.com/repo.git \
  --username myuser \
  --password mypassword
```

### Declarative Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: git
  url: https://github.com/org/repo.git
  username: git
  password: ghp_xxxxxxxxxxxx
```

## SSH Authentication

```bash
argocd repo add git@github.com:org/repo.git \
  --ssh-private-key-path ~/.ssh/id_rsa
```

### Declarative Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-ssh-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: git
  url: git@github.com:org/repo.git
  sshPrivateKey: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    ...
    -----END OPENSSH PRIVATE KEY-----
```

## GitHub App Authentication

```bash
argocd repo add https://github.com/org/repo.git \
  --github-app-id 12345 \
  --github-app-installation-id 67890 \
  --github-app-private-key-path key.pem
```

### For GitHub Enterprise

```bash
argocd repo add https://github.example.com/org/repo.git \
  --github-app-id 12345 \
  --github-app-installation-id 67890 \
  --github-app-private-key-path key.pem \
  --github-app-enterprise-base-url https://github.example.com/api/v3
```

## Credential Templates

Reusable credentials for URL patterns:

```bash
# All repos under org
argocd repocreds add https://github.com/org \
  --username git \
  --password ghp_xxxxxxxxxxxx

# SSH credential template
argocd repocreds add git@github.com:org \
  --ssh-private-key-path ~/.ssh/id_rsa
```

### Declarative

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: github-creds
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repo-creds
type: Opaque
stringData:
  type: git
  url: https://github.com/org
  username: git
  password: ghp_xxxxxxxxxxxx
```

## TLS Certificates

### Self-Signed CA

```bash
argocd cert add-tls git.example.com --from ~/ca-cert.pem
```

### Skip TLS Verification (not recommended)

```bash
argocd repo add https://git.example.com/repo.git \
  --insecure-skip-server-verification
```

### Declarative ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-tls-certs-cm
  namespace: argocd
data:
  git.example.com: |
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
```

## SSH Known Hosts

```bash
# Add from ssh-keyscan
ssh-keyscan github.com | argocd cert add-ssh --batch

# List known hosts
argocd cert list --cert-type ssh
```

### Declarative ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-ssh-known-hosts-cm
  namespace: argocd
data:
  ssh_known_hosts: |
    github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmd...
    gitlab.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsj2b...
```

## Helm Repositories

```bash
# Public Helm repo
argocd repo add https://charts.bitnami.com/bitnami --type helm --name bitnami

# Private Helm repo
argocd repo add https://charts.example.com \
  --type helm \
  --name private \
  --username admin \
  --password secret

# OCI Helm registry
argocd repo add registry-1.docker.io \
  --type helm \
  --name dockerhub \
  --enable-oci \
  --username myuser \
  --password mytoken
```

## Google Cloud Source

```bash
argocd repo add https://source.developers.google.com/p/project/r/repo \
  --gcp-service-account-key-path service-account.json
```

## CLI Commands

```bash
# List repositories
argocd repo list

# Get repository details
argocd repo get https://github.com/org/repo.git

# Remove repository
argocd repo rm https://github.com/org/repo.git

# List credential templates
argocd repocreds list
```

## Troubleshooting

**GitLab 301 redirects:** Add `.git` suffix to URL
```bash
argocd repo add https://gitlab.example.com/org/repo.git  # Note .git suffix
```

**Permission denied:** Check SSH key permissions (600) and known hosts

**Certificate errors:** Add CA cert or use `--insecure-skip-server-verification` for testing
