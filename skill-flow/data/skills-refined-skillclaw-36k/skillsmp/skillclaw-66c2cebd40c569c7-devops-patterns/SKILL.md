---
name: devops-patterns
description: Use this skill when containerizing applications, setting up CI/CD pipelines, or deploying services across various platforms.
---

# DevOps Patterns

This skill provides best practices and patterns for DevOps practices, supporting on-demand loading across multiple platforms.

## Trigger Conditions

- Containerizing applications (Docker)
- Configuring CI/CD pipelines
- Deploying services to cloud platforms
- Setting up monitoring and alerts
- Infrastructure as Code

## Platform-Specific Patterns

Load the corresponding platform-specific files based on project requirements:

| Platform   | Load File        | Content                          |
|------------|------------------|----------------------------------|
| Docker     | `docker.md`      | Containerization, Compose, Image Optimization |
| CI/CD      | `ci-cd.md`       | GitHub Actions, GitLab CI       |
| Kubernetes  | `kubernetes.md`  | K8s Deployment, Services, Configuration |

**Loading Method**: Detect project files such as `Dockerfile`, `.github/workflows`, or `k8s/` to determine requirements.

---

## General DevOps Principles

### 12-Factor App Principles

```
┌─────────────────────────────────────────────────────────────┐
│                    12-Factor App Core Principles            │
├─────────────────────────────────────────────────────────────┤
│  1. Codebase        One codebase, many deployments          │
│  2. Dependencies    Explicitly declare dependencies         │
│  3. Config          Store configuration in environment variables |
│  4. Backing Services Treat backing services as attached resources |
│  5. Build/Release/Run Strictly separate build, release, run |
│  6. Processes       Execute the app as one or more stateless processes |
│  7. Port Binding    Export services via port binding       |
│  8. Concurrency     Scale out via the process model       |
│  9. Disposability   Maximize robustness with fast startup and graceful shutdown |
│ 10. Dev/Prod Parity Keep development, staging, and production as similar as possible |
│ 11. Logs            Treat logs as event streams            |
│ 12. Admin Processes Run admin/management tasks as one-off processes |
└─────────────────────────────────────────────────────────────┘
```

### Environment Management

```
┌─────────────────────────────────────────────────────────────┐
│                      Environment Flow                        │
├─────────────────────────────────────────────────────────────┤
│  Development → Staging → Production                         │
│       ↓           ↓           ↓                             │
│   Local Dev      Pre-release  Production                    │
│   .env.local     .env.staging  .env.production              │
└─────────────────────────────────────────────────────────────┘
```

**Environment Variable Management**:

```bash
# .env.example (commit to Git as a template)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
API_KEY=your-api-key-here

# .env.local (do not commit, for local development)
DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp_dev
```

---

## Deployment Strategies

### Blue-Green Deployment

```
         ┌──────────────┐
         │   Load Balancer  │
         └──────┬───────┘
```