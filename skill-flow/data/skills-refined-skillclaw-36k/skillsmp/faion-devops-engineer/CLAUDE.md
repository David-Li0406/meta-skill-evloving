# DevOps Engineer Skill

## Overview

Technical skill for DevOps and infrastructure operations. Orchestrates containerization, orchestration, infrastructure as code, cloud services, and CI/CD pipelines.

**Agent:** faion-devops-agent

---

## Directory Structure

```
faion-devops-engineer/
├── CLAUDE.md                       # This file
├── SKILL.md                        # Skill definition and methodologies
├── docker.md                       # Reference: containers
├── kubernetes.md                   # Reference: K8s
├── terraform.md                    # Reference: IaC
├── aws.md                          # Reference: AWS
├── gcp.md                          # Reference: GCP
├── finops.md                       # Reference: costs
├── ref-platform-engineering.md     # Reference: IDPs
├── ref-gitops.md                   # Reference: GitOps
├── ref-aiops.md                    # Reference: AIOps
├── ref-dora-metrics.md             # Reference: DORA
├── ref-security-as-code.md         # Reference: policy
├── docker-containerization.md      # Methodology
├── docker-compose.md               # Methodology
├── kubernetes-deployment.md        # Methodology
├── helm-charts.md                  # Methodology
├── terraform-iac.md                # Methodology
├── aws-architecture.md             # Methodology
├── gcp-architecture.md             # Methodology
├── azure-architecture.md           # Methodology
├── github-actions-cicd.md          # Methodology
├── gitlab-cicd.md                  # Methodology
├── jenkins-pipelines.md            # Methodology
├── argocd-gitops.md                # Methodology
├── prometheus-monitoring.md        # Methodology
├── grafana-dashboards.md           # Methodology
├── elk-stack-logging.md            # Methodology
├── nginx-configuration.md          # Methodology
├── load-balancing.md               # Methodology
├── ssl-tls-setup.md                # Methodology
├── secrets-management.md           # Methodology
├── backup-strategies.md            # Methodology
├── finops-cloud-cost-optimization.md # Methodology
├── meth-platform-engineering.md    # Methodology
├── meth-gitops.md                  # Methodology
├── meth-aiops.md                   # Methodology
├── meth-dora-metrics.md            # Methodology
└── meth-security-as-code.md        # Methodology
```

---

## Key Files

| File | Description | Lines |
|------|-------------|-------|
| `SKILL.md` | Skill definition with methodologies, workflows, commands, checklists | ~330 |
| `docker.md` | Container development: Dockerfile, Compose, multi-stage builds, security | ~1140 |
| `kubernetes.md` | K8s operations: kubectl, Helm, deployments, services, networking | ~960 |
| `terraform.md` | IaC with Terraform: HCL syntax, modules, state management, providers | ~1090 |
| `aws.md` | AWS CLI operations: EC2, S3, Lambda, IAM, VPC, ECR, ECS | ~1480 |
| `gcp.md` | gcloud CLI: Compute Engine, Cloud Run, GKE, BigQuery, IAM | ~1400 |
| `ref-platform-engineering.md` | Internal Developer Platforms (IDP), self-service, golden paths | ~50 |
| `ref-gitops.md` | Git as source of truth, ArgoCD, Flux, progressive delivery | ~80 |
| `ref-aiops.md` | AI-powered operations, anomaly detection, auto-remediation | ~70 |
| `ref-dora-metrics.md` | Four key DevOps metrics for performance measurement | ~35 |
| `finops.md` | Cloud cost optimization, AI workload costs | ~55 |
| `ref-security-as-code.md` | Policy as Code with OPA, Gatekeeper, Kyverno | ~60 |

---

## Methodologies (26)

### Docker (docker.md)

- Multi-stage builds, Docker Compose, security scanning, layer optimization

### Kubernetes (kubernetes.md)

- Resource management, Helm charts, ConfigMaps/Secrets, Ingress/networking

### Terraform (terraform.md)

- Module design, state management, workspaces, testing

### AWS (aws.md)

- IAM best practices, VPC design, cost optimization, disaster recovery

### GCP (gcp.md)

- IAM & service accounts, VPC & networking, GKE operations, cost optimization

### Modern DevOps Practices

- Platform Engineering: platform-engineering.md
- GitOps: gitops.md
- AIOps: aiops.md
- DORA Metrics: dora-metrics.md
- FinOps: finops.md
- Security as Code: security-as-code.md

---

## Quick Reference

### Tool Selection

| Tool | Use Case |
|------|----------|
| Docker | Containerization, local dev, CI builds |
| Kubernetes | Container orchestration, scaling |
| Terraform | Multi-cloud IaC, infrastructure provisioning |
| Pulumi | IaC with programming languages |
| Ansible | Configuration management |

### Cloud Providers

| Provider | Strengths |
|----------|-----------|
| AWS | Most services, enterprise, mature |
| GCP | Kubernetes, ML, BigQuery |
| Azure | Microsoft ecosystem, hybrid |
| Hetzner | Cost-effective, EU data residency |

### CI/CD Tools

| Tool | Best For |
|------|----------|
| GitHub Actions | GitHub repos, simple pipelines |
| GitLab CI | GitLab repos, full DevOps platform |
| ArgoCD | GitOps, Kubernetes deployments |
| Jenkins | Complex pipelines, self-hosted |

---

## Common Commands

```bash
# Docker
docker build -t app:latest .
docker compose up -d

# Kubernetes
kubectl apply -f deployment.yaml
kubectl get pods,svc,deploy

# Terraform
terraform init && terraform plan
terraform apply

# AWS
aws configure
aws s3 sync ./dist s3://bucket/

# GCP
gcloud auth login
gcloud config set project my-project
gcloud run deploy my-service --image=gcr.io/project/image --region=us-central1
```

---

*Total: 11 reference files*
