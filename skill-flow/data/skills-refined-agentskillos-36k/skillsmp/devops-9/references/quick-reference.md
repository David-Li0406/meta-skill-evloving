# DevOps Quick Reference

Quick reference tables for common DevOps tools, commands, and configurations.

## Security Scanning Tools

| Tool | Purpose | Command |
|------|---------|---------|
| Trivy | Container vulnerabilities | `trivy image myapp:latest` |
| tfsec | Terraform security | `tfsec .` |
| checkov | IaC policy | `checkov -d .` |
| kubesec | K8s manifests | `kubesec scan pod.yaml` |
| kube-bench | CIS benchmarks | `kube-bench run` |
| Falco | Runtime security | Runtime monitoring |
| Grype | SBOM-based scanning | `grype myapp:latest` |
| Docker Scout | Container analysis | `docker scout cves myapp:latest` |
| Hadolint | Dockerfile linter | `hadolint Dockerfile` |
| terrascan | IaC compliance | `terrascan scan -t aws` |
| Infracost | Cost estimation | `infracost breakdown --path .` |

## Common Port Numbers

| Service | Port | Protocol |
|---------|------|----------|
| HTTP | 80 | TCP |
| HTTPS | 443 | TCP |
| SSH | 22 | TCP |
| PostgreSQL | 5432 | TCP |
| MySQL | 3306 | TCP |
| Redis | 6379 | TCP |
| MongoDB | 27017 | TCP |
| Prometheus | 9090 | TCP |
| Grafana | 3000 | TCP |
| Elasticsearch | 9200 | TCP |
| Kibana | 5601 | TCP |
| RabbitMQ | 5672 | TCP |
| RabbitMQ Management | 15672 | TCP |
| Kafka | 9092 | TCP |
| etcd | 2379 | TCP |
| Consul | 8500 | TCP |
| Vault | 8200 | TCP |

## Kubernetes Commands

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes

# Namespaces
kubectl get namespaces
kubectl create namespace <name>

# Pods
kubectl get pods -n <namespace>
kubectl describe pod <name> -n <namespace>
kubectl logs <pod> -n <namespace>
kubectl exec -it <pod> -n <namespace> -- /bin/sh

# Deployments
kubectl get deployments -n <namespace>
kubectl rollout status deployment/<name>
kubectl rollout restart deployment/<name>
kubectl scale deployment/<name> --replicas=3

# Services
kubectl get svc -n <namespace>
kubectl port-forward svc/<name> 8080:80

# Secrets
kubectl get secrets -n <namespace>
kubectl create secret generic <name> --from-literal=key=value

# Debug
kubectl get events --sort-by='.lastTimestamp'
kubectl top pods -n <namespace>
```

## Terraform Commands

```bash
# Initialize
terraform init
terraform init -upgrade

# Plan
terraform plan
terraform plan -out=tfplan
terraform plan -var-file=prod.tfvars

# Apply
terraform apply
terraform apply tfplan
terraform apply -auto-approve

# State management
terraform state list
terraform state show <resource>
terraform state mv <source> <dest>
terraform state rm <resource>

# Workspace
terraform workspace list
terraform workspace new <name>
terraform workspace select <name>

# Import
terraform import <resource> <id>

# Destroy
terraform destroy
terraform destroy -target=<resource>
```

## Docker Commands

```bash
# Build
docker build -t myapp:v1 .
docker build --no-cache -t myapp:v1 .
docker build --target builder -t myapp:builder .

# Run
docker run -d --name myapp -p 8080:80 myapp:v1
docker run -it --rm myapp:v1 /bin/sh
docker run --env-file .env myapp:v1

# Manage
docker ps -a
docker logs -f myapp
docker exec -it myapp /bin/sh
docker stop myapp && docker rm myapp

# Images
docker images
docker rmi myapp:v1
docker image prune -a

# Registry
docker login
docker tag myapp:v1 registry.example.com/myapp:v1
docker push registry.example.com/myapp:v1
docker pull registry.example.com/myapp:v1

# Compose
docker compose up -d
docker compose down
docker compose logs -f
docker compose ps
```

## Helm Commands

```bash
# Repo management
helm repo add <name> <url>
helm repo update
helm search repo <chart>

# Install/Upgrade
helm install <release> <chart>
helm install <release> <chart> -f values.yaml
helm upgrade <release> <chart>
helm upgrade --install <release> <chart>

# Manage releases
helm list
helm status <release>
helm history <release>
helm rollback <release> <revision>
helm uninstall <release>

# Templates
helm template <release> <chart>
helm template <release> <chart> -f values.yaml > manifests.yaml

# Debug
helm lint <chart>
helm get values <release>
helm get manifest <release>
```

## GitHub Actions Syntax

```yaml
# Workflow triggers
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'

# Job configuration
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

# Matrix builds
strategy:
  matrix:
    node: [18, 20, 22]
    os: [ubuntu-latest, macos-latest]

# Conditionals
if: github.event_name == 'push' && github.ref == 'refs/heads/main'

# Secrets
env:
  API_KEY: ${{ secrets.API_KEY }}
```
