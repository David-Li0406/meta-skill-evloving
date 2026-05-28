---
name: faion-devops-engineer
description: "DevOps Engineer role: Docker, Kubernetes, Terraform, AWS/GCP/Azure, CI/CD (GitHub Actions, GitLab CI), infrastructure as code, monitoring (Prometheus, Grafana), logging, secrets management, nginx, load balancing, Platform Engineering, GitOps, AIOps, DORA metrics. 26 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---

# DevOps Domain Skill

**Communication: User's language. Config/code: English.**

## Purpose

Orchestrates infrastructure and deployment activities. Covers containerization, orchestration, infrastructure as code, cloud services, and CI/CD pipelines.

---

## Agents

| Agent | Purpose |
|-------|---------|
| faion-devops-agent | Infrastructure and deployment automation |

---

## References

Detailed technical context for each area:

| Reference | Content | Lines |
|-----------|---------|-------|
| [docker.md](docker.md) | Containers, Compose, multi-stage builds | ~1140 |
| [kubernetes.md](kubernetes.md) | K8s resources, Helm, operators | ~960 |
| [terraform.md](terraform.md) | IaC, modules, state management | ~1090 |
| [aws.md](aws.md) | AWS CLI, services, IAM, networking | ~1480 |
| [gcp.md](gcp.md) | gcloud CLI, GCE, GKE, Cloud Run, BigQuery | ~1400 |
| [ref-platform-engineering.md](ref-platform-engineering.md) | Platform Engineering, IDPs | ~50 |
| [ref-gitops.md](ref-gitops.md) | GitOps, ArgoCD, Flux | ~80 |
| [ref-aiops.md](ref-aiops.md) | AIOps, anomaly detection | ~70 |
| [ref-dora-metrics.md](ref-dora-metrics.md) | DORA metrics | ~35 |
| [finops.md](finops.md) | Cloud cost optimization | ~55 |
| [ref-security-as-code.md](ref-security-as-code.md) | Policy as Code | ~60 |

**Total:** ~6,270 lines of technical reference

---

## Quick Reference

### Tool Selection

| Tool | Use Case |
|------|----------|
| **Docker** | Containerization, local dev, CI builds |
| **Kubernetes** | Container orchestration, scaling |
| **Terraform** | Multi-cloud IaC, infrastructure provisioning |
| **Pulumi** | IaC with programming languages |
| **Ansible** | Configuration management, server setup |

### Cloud Provider Selection

| Provider | Strengths |
|----------|-----------|
| **AWS** | Most services, enterprise, mature |
| **GCP** | Kubernetes, ML, BigQuery |
| **Azure** | Microsoft ecosystem, hybrid |
| **Hetzner** | Cost-effective, EU data residency |
| **DigitalOcean** | Simple, developer-friendly |

### CI/CD Tools

| Tool | Best For |
|------|----------|
| **GitHub Actions** | GitHub repos, simple pipelines |
| **GitLab CI** | GitLab repos, full DevOps platform |
| **Jenkins** | Complex pipelines, self-hosted |
| **ArgoCD** | GitOps, Kubernetes deployments |

---

## Methodologies (20)

### Docker

| Name | Purpose |
|------|---------|
| docker-containerization | Multi-stage builds, smaller production images |
| docker-compose | Multi-container local dev |
| security-scanning (in docker) | Vulnerability detection |
| layer-optimization (in docker) | Build cache efficiency |

### Kubernetes

| Name | Purpose |
|------|---------|
| kubernetes-deployment | Resource management, requests, limits, QoS |
| helm-charts | Package management |
| secrets-management | ConfigMaps, Secrets, configuration management |
| load-balancing | Ingress, traffic routing |

### Terraform

| Name | Purpose |
|------|---------|
| terraform-iac | Module design, reusable infrastructure |
| state-management (in terraform) | Remote state, locking |
| workspaces (in terraform) | Environment separation |
| testing (in terraform) | Terratest, plan validation |

### AWS

| Name | Purpose |
|------|---------|
| aws-architecture | IAM best practices, least privilege, roles |
| vpc-design (in aws) | Networking, security groups |
| finops-cloud-cost-optimization | Reserved, spot, rightsizing |
| backup-strategies | Disaster recovery, backup, multi-region |

### GCP

| Name | Purpose |
|------|---------|
| gcp-architecture | IAM, service accounts, workload identity |
| vpc-networking (in gcp) | Shared VPC, firewall rules, Cloud NAT |
| gke-operations (in gcp) | Autopilot, node pools, workload identity |
| cost-optimization (in gcp) | Committed use, preemptible/spot, rightsizing |

---

## Workflows

### Container Deployment

```
1. Write Dockerfile
2. Build and test locally
3. Push to registry
4. Update K8s manifests
5. Apply to cluster
6. Verify deployment
7. Monitor logs/metrics
```

### Infrastructure Change

```
1. Create feature branch
2. Write Terraform code
3. Run `terraform plan`
4. Review plan output
5. Create PR
6. Apply after approval
7. Verify resources
```

### CI/CD Pipeline

```yaml
# GitHub Actions example
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push
        run: |
          docker build -t app:${{ github.sha }} .
          docker push registry/app:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to K8s
        run: |
          kubectl set image deployment/app \
            app=registry/app:${{ github.sha }}
```

---

## Common Commands

### Docker

```bash
# Build image
docker build -t app:latest .

# Run container
docker run -d -p 8080:80 app:latest

# View logs
docker logs -f container_id

# Compose up
docker compose up -d

# Clean up
docker system prune -af
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deployment.yaml

# Get resources
kubectl get pods,svc,deploy

# View logs
kubectl logs -f pod/app-xxx

# Port forward
kubectl port-forward svc/app 8080:80

# Scale
kubectl scale deploy/app --replicas=3
```

### Terraform

```bash
# Initialize
terraform init

# Plan
terraform plan -out=tfplan

# Apply
terraform apply tfplan

# Destroy
terraform destroy

# State list
terraform state list
```

### AWS CLI

```bash
# Configure
aws configure

# S3
aws s3 sync ./dist s3://bucket/

# ECR login
aws ecr get-login-password | docker login --username AWS --password-stdin xxx.ecr.region.amazonaws.com

# Lambda invoke
aws lambda invoke --function-name func output.json
```

### gcloud CLI

```bash
# Configure
gcloud auth login
gcloud config set project my-project

# Cloud Storage
gcloud storage rsync -r ./dist gs://bucket/

# Artifact Registry login
gcloud auth configure-docker us-central1-docker.pkg.dev

# Cloud Run deploy
gcloud run deploy my-service --image=us-central1-docker.pkg.dev/project/repo/image --region=us-central1

# GKE credentials
gcloud container clusters get-credentials my-cluster --zone=us-central1-a
```

---

## Security Checklist

### Container Security

- [ ] Non-root user in Dockerfile
- [ ] Minimal base image (distroless, alpine)
- [ ] No secrets in image
- [ ] Image scanning enabled
- [ ] Read-only root filesystem

### Kubernetes Security

- [ ] RBAC configured
- [ ] Network policies defined
- [ ] Pod security standards
- [ ] Secrets encrypted at rest
- [ ] Resource limits set

### Infrastructure Security

- [ ] Least privilege IAM
- [ ] Private subnets for workloads
- [ ] Security groups restrictive
- [ ] Encryption enabled
- [ ] Logging to central system

---

## Monitoring Stack

### Observability Triad

| Pillar | Tools |
|--------|-------|
| **Metrics** | Prometheus, Grafana, CloudWatch |
| **Logs** | Loki, ELK, CloudWatch Logs |
| **Traces** | Jaeger, Tempo, X-Ray |

### Alerting

```yaml
# Prometheus alert example
groups:
  - name: app
    rules:
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m])
          / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-software-developer | Application code to deploy |
| faion-ml-engineer | ML model deployment |

---

## Error Handling

| Issue | Action |
|-------|--------|
| Unknown cloud provider | Ask user or check existing config |
| Complex infrastructure | Read reference files for patterns |
| Multi-cloud setup | Combine relevant references |

---

*DevOps Domain Skill v1.1*
*6 Reference Files | 20 Methodologies*
*Aggregated from: docker, kubernetes, terraform, aws, gcp, best-practices*
