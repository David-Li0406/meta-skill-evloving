---
name: deploy-checklist
description: Generate deployment checklists with pre-flight checks, rollout strategy, and verification steps. Analysis only - does not execute deployments.
license: MIT
compatibility:
  - runtime:any
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git:log)
  - Bash(git:diff)
  - Bash(git:show)
metadata:
  author: thoreinstein
  version: 1.0.0
---

# Deploy Checklist

Generate comprehensive deployment checklists for safe, documented releases.

## When to Use This Skill

- Before deploying a new release to any environment
- When preparing for production deployments
- When you need a documented rollback plan
- For compliance or audit requirements around deployments
- When onboarding team members to deployment processes

## Input

Provide the following:

1. **Target**
   - Service or application name
   - Target environment (staging, production, etc.)
   - Release version or tag

2. **Scope**
   - Commits or PRs included in this release
   - Features being released
   - Bug fixes included

3. **Strategy Preference** (optional)
   - Rolling update
   - Blue-green
   - Canary
   - Or let the checklist recommend based on risk

## Workflow

### Step 1: Analyze Changes

Review what's being deployed:
- List commits since last deployment
- Identify database migrations
- Note configuration changes
- Check dependency updates
- Flag feature flag changes

### Step 2: Assess Risk

Evaluate deployment risk:
- Breaking changes
- Migration complexity
- Rollback difficulty
- Blast radius

### Step 3: Generate Pre-flight Checklist

Create verification items for:
- **Code Readiness** - tests pass, reviewed, merged
- **Environment Readiness** - resources available, configs updated
- **Observability** - dashboards ready, alerts configured
- **Communication** - stakeholders notified, runbook available

### Step 4: Define Rollout Strategy

Based on risk assessment, recommend:
- Rollout type (rolling, blue-green, canary)
- Traffic progression (for canary)
- Rollout steps with verification gates
- Timeline estimate

### Step 5: Create Verification Checklist

Define what to check after deployment:
- **Immediate (0-5 min)** - pods healthy, no errors
- **Short-term (5-30 min)** - metrics normal, features working
- **Extended (30 min - 2 hr)** - performance stable, no regressions

### Step 6: Document Rollback Plan

For every deployment, include:
- Rollback trigger conditions
- Rollback commands/steps
- Rollback verification
- Communication plan if rollback needed

## Output

Produce a deployment checklist following the template in `references/deploy-checklist-template.md`.

The checklist should include:
- Summary (service, environment, version, date)
- Changes included (features, fixes, migrations, dependencies)
- Pre-flight checklist
- Deployment strategy with steps
- Verification checklist by time window
- Rollback triggers and plan

## Investigation Areas

| Area               | What to Check                                    |
| ------------------ | ------------------------------------------------ |
| **Code**           | Changes, migrations, config, dependencies, flags |
| **Infrastructure** | Manifests, resources, scaling, env config        |
| **History**        | Previous deployments, known issues, incidents    |

## Constraints

- **Checklist only** - this skill generates documentation, not executes deployments
- **Always include rollback** - every checklist must have a rollback plan
- **Be specific** - include actual commands, not just descriptions
- **Risk-appropriate** - match strategy complexity to deployment risk

## Example

### Example: API Service Production Deploy

**Input:**
- Service: `user-api`
- Environment: `production`
- Version: `v2.3.0`
- Changes: 3 features, 1 migration, 2 bug fixes

**Output Summary:**
```
Deployment: user-api v2.3.0 → production

Risk Assessment: MEDIUM
- Database migration (additive, backward compatible)
- New authentication flow (feature flagged)

Strategy: Canary (10% → 50% → 100%)

Pre-flight:
✓ All tests passing
✓ Migration tested in staging
✓ Feature flag configured (disabled by default)
✓ Dashboards bookmarked
✓ On-call notified

Rollback Triggers:
- Error rate > 1%
- P99 latency > 500ms
- Migration failure

Rollback Command:
kubectl rollout undo deployment/user-api -n production
```

---

Begin by analyzing the changes included in this deployment before generating the checklist.
