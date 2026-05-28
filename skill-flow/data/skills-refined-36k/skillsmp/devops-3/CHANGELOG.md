# Changelog - DevOps Skill

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-28

### Added

- **Initial release** as standalone skill extracted from `backend-developer/devops`
- **30 agents** across 6 domains:

#### cicd/ - Pipelines CI/CD (6 agents)
- `orchestrator` - Coordination CI/CD
- `github-actions` - GitHub Actions workflows
- `gitlab-ci` - GitLab CI pipelines
- `pipelines` - Pipeline patterns and best practices
- `quality-gates` - SonarQube, coverage gates
- `artifacts` - Artifact management, releases

#### containers/ - Conteneurisation (5 agents)
- `orchestrator` - Coordination containers
- `docker` - Dockerfile, multi-stage builds
- `docker-compose` - Local orchestration
- `registries` - Docker Hub, ECR, GCR
- `security` - Trivy, Snyk, image hardening

#### kubernetes/ - Orchestration K8s (6 agents)
- `orchestrator` - Coordination K8s
- `deployments` - Deployment, ReplicaSet
- `services` - Service, Ingress
- `helm` - Helm charts, values
- `scaling` - HPA, VPA, Keda
- `config` - ConfigMaps, Secrets

#### infrastructure/ - Infrastructure as Code (5 agents)
- `orchestrator` - Coordination IaC
- `terraform` - Terraform modules, state
- `aws` - EC2, RDS, S3, EKS
- `gcp` - GCE, GKE, Cloud SQL
- `networking` - VPC, subnets, security groups

#### monitoring/ - Observabilité (5 agents)
- `orchestrator` - Coordination monitoring
- `prometheus` - Metrics, exporters
- `grafana` - Dashboards, panels
- `logging` - ELK, Loki, Fluentd
- `alerting` - Alertmanager, PagerDuty

#### deployment/ - Stratégies de déploiement (3 agents)
- `orchestrator` - Coordination déploiement
- `strategies` - Blue-Green, Canary, ArgoCD
- `rollback` - Recovery procedures

### Architecture

- **Position**: NIVEAU 3 IMPLÉMENTATION
- **Reports to**: `direction-technique` (strategy), `web-dev-process` (process)
- **Coordinates with**: `lead-dev` (releases), `backend-developer`, `frontend-developer`

### Documentation

- SKILL.md with full routing rules
- orchestrator.md with delegation matrix
- Test suite with 100% agent coverage
- CI workflow for validation

### Migration Notes

- Extracted from `backend-developer` v1.0.0
- `backend-developer` now redirects DevOps queries to this skill
- See [ADR-007](../web-agency/docs/adr/007-skill-extraction-pattern.md) for extraction rationale
