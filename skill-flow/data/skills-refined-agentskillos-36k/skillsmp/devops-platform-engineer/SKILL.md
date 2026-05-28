---
name: devops-platform-engineer
description: DevOps guidance for DigitalOcean deployment artifacts and runtime configuration.
---

# DevOps Platform Engineer

> **Status**: PRODUCTION
> **Location**: `deploy/`, `Dockerfile.*`, `Procfile`
> **Primary Function**: Document deployment artifacts and runtime configuration.

## Overview
DevOps assets in this repo focus on DigitalOcean App Platform specs, Docker images, and health/verification scripts. There is no Terraform or Kubernetes configuration checked in.

## Verified Code References
- `deploy/social-xpress/do-app-spec.dev.yaml`
- `deploy/social-xpress/do-app-spec.staging.yaml`
- `deploy/social-xpress/do-app-spec.prod.yaml`
- `Dockerfile.api`
- `Dockerfile.front`
- `Procfile`
- `do-check-deployment.ps1`
- `verify-all.js`

## Current State

### What Already Exists
- DO App Platform specs for dev, staging, and prod
- Dockerfiles for API and worker builds
- Health verification script for live endpoints
- Runtime configuration via environment variables

### What Still Needs to be Built
- Infrastructure-as-code for repeatable provisioning
- CI/CD workflows stored in repo
- Centralized monitoring and alerting configuration

## Nextier-Specific Example
```typescript
// apps/api/src/main.ts
const app = await NestFactory.create<NestFastifyApplication>(
  AppModule,
  new FastifyAdapter({
    disableRequestLogging: true,
    bodyLimit: ONE_HUNDRED_MB,
  }),
  {
    rawBody: true,
    bufferLogs: true,
  },
);
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `code-quality-enforcer` | CI gates and build verification scripts |
| `workflow-orchestration-engine` | Runtime dependencies on Redis, DB, and providers |
| `signalhouse-integration` | Environment configuration for external services |
| `cost-guardian` | Platform costs tracked outside the repo |

## Cost Information
- DigitalOcean and infrastructure costs are not tracked in code.

## Multi-Tenant Considerations
- Deployment artifacts support a shared multi-tenant runtime; tenant isolation is handled in app code.
