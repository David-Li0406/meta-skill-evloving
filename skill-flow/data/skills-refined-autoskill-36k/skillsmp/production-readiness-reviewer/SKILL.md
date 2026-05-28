---
name: production-readiness-reviewer
description: Verify whether a service, feature, or contract is safe to deploy to production. Use when preparing for deployment, reviewing release candidates, or validating production configs. Triggers on "production ready", "deploy review", "release check", "pre-deploy", "go-live checklist", "launch readiness", "deployment review", "ready for prod".
---

# Production Readiness Reviewer

Verify whether a service, feature, or smart contract is safe to deploy to production. Ensures all operational, reliability, and safety requirements are met before go-live.

## Core Guardrails

:red_circle: **If rollback is impossible, it's a red flag.**
:red_circle: **If you can't observe it, you can't operate it.**

## When to Use

- Preparing a service for first production deployment
- Reviewing release candidates before deploy
- Validating production configuration changes
- Pre-launch checklist for new features
- Smart contract deployment verification
- Infrastructure changes going to production

## Review Workflow

On EVERY invocation, execute these steps in order:

### Step 1: Identify Deployable Unit

Determine what is being deployed:

| Type | Examples |
|------|----------|
| **Service** | API, worker, microservice, lambda |
| **Frontend** | Web app, mobile app build |
| **Smart Contract** | Solidity, Vyper, Rust/Anchor |
| **Infrastructure** | Terraform, K8s manifests, cloud resources |
| **Configuration** | Feature flags, env vars, secrets |
| **Database** | Migration, schema change |

Document:
```
Deployable: [name]
Type: [service/frontend/contract/infra/config/database]
Version: [tag/commit/hash]
Target environment: [staging/production]
```

### Step 2: Inspect Configuration

Review all configuration for production readiness:

```bash
# Find environment variables
grep -rn "process.env\|os.environ\|env::" --include="*.ts" --include="*.py" --include="*.go"

# Find config files
ls -la *.config.* .env* config/ 2>/dev/null

# Check for hardcoded values
grep -rn "localhost\|127.0.0.1\|:3000\|:8080" --include="*.ts" --include="*.yaml"

# Find feature flags
grep -rn "feature.*flag\|isEnabled\|FF_" --include="*.ts" --include="*.tsx"
```

Verify:
- [ ] All env vars documented and have production values
- [ ] No hardcoded development URLs/ports
- [ ] Secrets come from vault/env, not code
- [ ] Feature flags set correctly for production
- [ ] Resource limits configured (memory, CPU, connections)

### Step 3: Review Failure Modes

For each external dependency, answer:

| Dependency | What if unavailable? | What if slow? | What if returns bad data? |
|------------|---------------------|---------------|---------------------------|
| Database | [behavior] | [behavior] | [behavior] |
| Cache | [behavior] | [behavior] | [behavior] |
| External API | [behavior] | [behavior] | [behavior] |
| Queue | [behavior] | [behavior] | [behavior] |

### Step 4: Execute Checklist

See [CHECKLIST.md](CHECKLIST.md) for the complete production readiness checklist.

## Output Format

### A) Deployable Unit & Scope

```
Deployable: [name]
Type: [type]
Version: [version]
Changes since last deploy: [summary]
Blast radius: [what could break]
```

### B) Blocking Issues

Issues that MUST be fixed before deployment:

```
### :red_circle: BLOCKER: [Title]

**Issue:** [Description]
**Risk:** [What could go wrong in production]
**Required fix:** [What must be done]
```

### C) Non-Blocking Risks

Issues to be aware of, but not deployment blockers:

```
### :yellow_circle: RISK: [Title]

**Issue:** [Description]
**Likelihood:** [Low/Medium/High]
**Impact:** [Low/Medium/High]
**Mitigation:** [How to reduce risk]
**Follow-up:** [Post-deploy action item]
```

### D) Rollback & Recovery Plan

```
Rollback method: [How to revert]
Rollback time estimate: [minutes]
Rollback complexity: [Simple/Complex/Impossible]
Data rollback needed: [Yes/No]
Rollback tested: [Yes/No]

Recovery steps:
1. [Step 1]
2. [Step 2]
3. ...

Escalation path:
- L1: [Who handles first]
- L2: [Escalate to]
- L3: [Final escalation]
```

### E) Production Readiness Verdict

```
┌─────────────────────────────────────────────────────────────┐
│  VERDICT: [READY / NOT READY / READY WITH CONDITIONS]       │
├─────────────────────────────────────────────────────────────┤
│  Blocking issues: [count]                                    │
│  Non-blocking risks: [count]                                 │
│  Rollback feasible: [Yes/No]                                 │
│  Observability complete: [Yes/No]                            │
├─────────────────────────────────────────────────────────────┤
│  Recommendation: [Deploy / Fix blockers / Needs discussion]  │
└─────────────────────────────────────────────────────────────┘
```

**Verdict definitions:**

| Verdict | Meaning |
|---------|---------|
| :white_check_mark: **READY** | Safe to deploy, no blocking issues |
| :yellow_circle: **READY WITH CONDITIONS** | Can deploy if [conditions] are met |
| :red_circle: **NOT READY** | Blocking issues must be resolved first |

## Quick Commands

```bash
# Check for debug/dev flags
grep -rn "DEBUG\|DEV_MODE\|development" --include="*.ts" --include="*.yaml"

# Find TODO/FIXME comments
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.go"

# Check health endpoints
curl -s http://localhost:8080/health | jq

# Verify environment variables are set
env | grep -E "^(DB_|API_|AWS_|KUCOIN_)" | wc -l

# Check for missing error handling
grep -rn "catch\s*{\s*}" --include="*.ts"  # Empty catch blocks

# Find hardcoded secrets
grep -rn "password.*=.*['\"]" --include="*.ts" --include="*.env*"
```

## Resources

- [CHECKLIST.md](CHECKLIST.md) - Complete production readiness checklist
- [RUNBOOK-TEMPLATE.md](RUNBOOK-TEMPLATE.md) - Template for operational runbooks
