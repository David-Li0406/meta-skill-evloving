# DevOps Skill

## Philosophy

This skill embodies the DevOps philosophy of "Everything as Code" - infrastructure, configuration, processes, and documentation should all be version-controlled and automated. We prefer immutable infrastructure (rebuild rather than modify) and practice continuous everything: integration, deployment, testing, and monitoring.

## Core Principles

### 1. Automation First
Every manual process is a future automation opportunity. If you do it twice, automate it. Infrastructure, configuration, and deployment processes should be code that can be versioned, reviewed, and tested.

### 2. Concurrent Operations
DevOps tasks should execute concurrently when possible. In a single session:
- Create CI pipeline configurations
- Set up CD workflows
- Configure monitoring and alerting
- Implement security scanning
- Establish infrastructure as code
- Generate comprehensive documentation

Never work sequentially when parallel execution is possible - this is inefficient and contradicts DevOps principles.

### 3. Security by Default
Security must be built in at every layer:
- Secrets management with proper encryption
- Container and dependency vulnerability scanning
- Role-based access control with least privilege
- Network policies restricting communication paths
- Audit logging and active monitoring
- Supply chain security verification

### 4. Observability Built-In
Monitoring and alerting aren't afterthoughts - they're integral to every deployment:
- Prometheus metrics collection
- Structured logging with proper indexing
- Distributed tracing for microservices
- SLOs and error budgets
- Runbook-linked alerts
- Dashboard visualizations (RED/USE methods)

### 5. Deployment Safety
Deployments should be boring and predictable:
- Multiple deployment strategies (blue-green, canary, rolling)
- Automated health checks and readiness probes
- Instant rollback capabilities
- Progressive traffic shifting
- Comprehensive pre/post-deployment checklists

### 6. Infrastructure as Cattle, Not Pets
Treat infrastructure as disposable and replaceable:
- Immutable infrastructure patterns
- Automated provisioning and teardown
- No manual configuration changes
- Version everything
- Drift detection and remediation

## What This Skill Provides

### Workflows
- **setup-ci**: Create CI/CD pipelines with GitHub Actions, GitLab CI, etc.
- **deploy**: Execute deployments with proper strategies and safety checks
- **monitor**: Establish monitoring, alerting, and observability
- **rollback**: Safely revert to previous stable versions
- **scale**: Implement auto-scaling and load balancing

### Knowledge Domains
- **Patterns**: CI/CD pipeline patterns, deployment strategies, monitoring approaches
- **Configurations**: Production-ready templates for GitHub Actions, Docker, Nginx
- **Checklists**: Pre/post-deployment validation and verification

### Technology Coverage
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI
- **Containers**: Docker, Kubernetes, Docker Compose
- **IaC**: Terraform, CloudFormation, Ansible, Pulumi
- **Cloud**: AWS, GCP, Azure, hybrid cloud
- **Monitoring**: Prometheus, Grafana, ELK Stack, DataDog

## When to Use This Skill

Use the devops skill when you need to:
- Set up automated testing and deployment pipelines
- Deploy applications to staging or production
- Configure container orchestration
- Implement infrastructure as code
- Establish monitoring and alerting systems
- Troubleshoot deployment issues
- Implement deployment strategies (blue-green, canary)
- Set up development environments with Docker Compose
- Configure reverse proxies and load balancers
- Scale applications or infrastructure
- Rollback failed deployments

## Integration Points

### With Architecture Skill
DevOps implements architectural designs, translating architecture specifications into deployed infrastructure. Architecture defines the "what" and "why"; DevOps defines the "how" and "when".

### With Implementation Skill
DevOps deploys the applications built by implementation workflows. Implementation creates the code; DevOps creates the pipeline that tests, builds, and deploys it.

### With Quality Skill
DevOps ensures production quality through automated testing gates, security scanning, and continuous monitoring. Quality defines standards; DevOps enforces them in pipelines.

## Success Metrics

A successful DevOps implementation achieves:
- **Zero-downtime deployments** with instant rollback capability
- **Automated testing** at multiple stages (unit, integration, e2e, security)
- **Complete observability** with metrics, logs, and traces
- **Infrastructure as code** with version control and automation
- **Security scanning** in every pipeline run
- **Fast feedback loops** from commit to production
- **Reliable, predictable deployments** that are "boring"

## The DevOps Mindset

> "Make deployments boring, predictable, and fully automated. Infrastructure should be cattle, not pets. Every manual process is a future automation opportunity. Reliability is a feature, not an afterthought."

This skill transforms the chaos of manual deployments into the calm of automated, monitored, and reliable production systems.
