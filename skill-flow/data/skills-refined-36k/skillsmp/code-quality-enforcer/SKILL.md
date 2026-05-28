---
name: code-quality-enforcer
description: Code quality guidelines and verification artifacts for the Nextier monorepo.
---

# Code Quality Enforcer

> **Status**: PRODUCTION
> **Location**: `eslint.config.mjs`, `jest.config.js`, `cspell.json`
> **Primary Function**: Document code quality gates and verification scripts.

## Overview
Quality enforcement is handled through ESLint, Jest config, spellcheck, and repo scripts. This skill documents the existing quality tooling and patterns.

## Verified Code References
- `eslint.config.mjs`
- `jest.config.js`
- `cspell.json`
- `verify-all.js`
- `apps/api/src/app/common/filters/global-exception.filter.ts`

## Current State

### What Already Exists
- ESLint configuration at repo root
- Jest configuration for testing
- Spellcheck configuration
- Verification script for system health checks
- Consistent error handling via `GlobalExceptionFilter`

### What Still Needs to be Built
- Pre-commit hooks and CI workflows for lint/test enforcement
- Standardized test coverage reporting
- Automated multi-tenant safety checks in CI

## Nextier-Specific Example
```typescript
// apps/api/src/app/common/filters/global-exception.filter.ts
const errorResponse: ErrorResponse = {
  error: message,
  code: this.getErrorCode(exception, status),
  correlationId,
  timestamp,
  path: request.url,
};

response.status(status).send(errorResponse);
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `devops-platform-engineer` | Build and deployment validation scripts |
| `workflow-orchestration-engine` | AI error handling and logging patterns |
| `technical-documentation-agent` | Keeps quality docs up to date |

## Cost Information
- No external API costs for quality tooling.

## Multi-Tenant Considerations
- Error logs include `correlationId` and route context for tenant debugging.
