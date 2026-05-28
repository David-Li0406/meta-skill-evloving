---
name: backend-service-auditor
description: Audit backend services for security, reliability, performance, and operability issues. Use when reviewing APIs, microservices, workers, or backend code changes. Triggers on "audit backend", "security review", "service audit", "API audit", "check vulnerabilities", "review microservice", "backend security", "audit API", "review service".
---

# Backend Service Auditor

Comprehensive auditor for backend services (APIs, workers, microservices) focusing on security, reliability, correctness, performance, data integrity, and operability. All findings are grounded in actual code and configuration.

## When to Use

- Reviewing backend code changes before merge
- Security auditing APIs or microservices
- Pre-deployment checks for critical services
- Investigating reliability or performance concerns
- Auditing authentication/authorization flows
- Reviewing data handling and integrity patterns

## Audit Workflow

On EVERY invocation, execute these steps in order:

### Step 1: Detect Stack & Service Boundaries

Identify the technology stack and architectural boundaries:

```
- Language/framework (Node/Express/Nest, Go, Python/FastAPI, Java/Spring, Rust, etc.)
- Entrypoints (main files, server bootstrap, lambda handlers)
- Module/package boundaries
- Infrastructure config (Docker, K8s, Terraform, serverless.yml)
- Shared libraries and internal packages
```

### Step 2: Scan Recent Changes

Review what has changed recently:

```bash
# Check working directory changes
git status
git diff --stat

# Review recent commits affecting backend
git log --oneline -20 --all -- "src/" "api/" "services/" "internal/"
```

Summarize:
- What behavioral changes were introduced?
- What new attack surface was added?
- What critical paths were modified?

### Step 3: Build Service Map

Create a mental model of the service:

| Component | Details |
|-----------|---------|
| **Endpoints** | REST routes, GraphQL resolvers, gRPC services |
| **Async** | Message queues, cron jobs, webhooks |
| **Data Stores** | Databases, caches, file storage |
| **External APIs** | Third-party integrations, internal services |
| **Secrets** | API keys, credentials, tokens |

### Step 4: Execute Audit Checklist

Audit touched services plus all critical paths (auth, payments, trading, user data).

See [CHECKLIST.md](CHECKLIST.md) for the complete audit checklist covering:
- Security (AuthN/AuthZ, injection, secrets, dependencies)
- Reliability & Correctness (idempotency, retries, concurrency, data integrity)
- Performance & Scalability (queries, caching, memory)
- Observability & Ops (logging, metrics, deployment)

## Output Format

Structure your audit report as follows:

### A) Scope Scanned
```
Services: [list services/modules audited]
Files reviewed: [count]
Commits analyzed: [range]
Stack: [detected technology stack]
```

### B) Service Map
```
Endpoints: [count] routes across [modules]
Data stores: [list DBs, caches]
External deps: [list integrations]
Critical paths: [auth, payments, etc.]
```

### C) Findings

Use severity levels:

| Severity | Icon | Meaning |
|----------|------|---------|
| CRITICAL | :red_circle: | Exploitable now, data breach risk |
| HIGH | :orange_circle: | Serious issue, needs immediate fix |
| MEDIUM | :yellow_circle: | Should fix soon, moderate risk |
| LOW | :white_circle: | Minor issue, fix when convenient |
| INFO | :blue_circle: | Observation, no action required |

For each finding:
```
### [SEVERITY] Title

**Location:** `path/to/file.ts:123`
**Category:** Security > Input Validation

**Issue:** [Describe the problem]

**Evidence:**
[Code snippet or proof]

**Risk:** [What could go wrong]

**Recommendation:** [How to fix]
```

### D) Summary Table

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Security | 0 | 1 | 2 | 1 |
| Reliability | 0 | 0 | 1 | 2 |
| Performance | 0 | 0 | 0 | 1 |
| Observability | 0 | 0 | 1 | 0 |

### E) Recommendations

Prioritized action items:
1. [Most critical fix]
2. [Second priority]
3. ...

## Quick Commands

```bash
# Check for vulnerable dependencies (Node)
npm audit

# Check for vulnerable dependencies (Python)
pip-audit

# Find hardcoded secrets
grep -rn "password\|secret\|api_key\|token" --include="*.ts" --include="*.js" --include="*.py"

# Find TODO/FIXME security notes
grep -rn "TODO.*security\|FIXME.*auth\|XXX" src/
```

## Resources

- [CHECKLIST.md](CHECKLIST.md) - Complete audit checklist
- [PATTERNS.md](PATTERNS.md) - Common vulnerability patterns by framework
