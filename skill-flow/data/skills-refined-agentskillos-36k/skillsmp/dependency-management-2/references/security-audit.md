# Security Audit

Scanning and addressing dependency vulnerabilities.

## Audit Tools

### Node.js

```bash
# Built-in audit
npm audit

# Detailed report
npm audit --json

# Fix automatically (safe fixes only)
npm audit fix

# Force fix (may include breaking changes)
npm audit fix --force

# Third-party alternatives
npx snyk test
npx auditjs ossi
```

### Python

```bash
# pip-audit
pip install pip-audit
pip-audit

# Safety
pip install safety
safety check

# Detailed report
pip-audit --format json
```

### Ruby

```bash
# bundler-audit
gem install bundler-audit
bundle audit check --update

# Detailed report
bundle audit check --format json
```

### Go

```bash
# govulncheck (official)
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...

# Nancy
go list -json -deps | nancy sleuth
```

## Vulnerability Severity

### CVSS Scoring

| Score | Severity | Response |
|-------|----------|----------|
| 9.0-10.0 | Critical | Immediate |
| 7.0-8.9 | High | 24-48 hours |
| 4.0-6.9 | Medium | This sprint |
| 0.1-3.9 | Low | Next sprint |

### Contextual Risk Assessment

```markdown
## Vulnerability Assessment: CVE-YYYY-XXXXX

### Vulnerability Info
- **Package:** affected-package
- **CVSS Score:** 7.5 (High)
- **Type:** Remote Code Execution

### Our Exposure
- [ ] Is the vulnerable code path used?
- [ ] Is the input controlled by attackers?
- [ ] Is the service exposed to the internet?
- [ ] Are there mitigating controls?

### Adjusted Risk
Based on our usage, actual risk is: [Lower/Same/Higher]

### Decision
- [ ] Patch immediately
- [ ] Patch this sprint
- [ ] Accept risk (document reason)
- [ ] Remove dependency
```

## Response Procedures

### Critical/High Severity

```markdown
## Emergency Security Patch

### 1. Assess (30 min)
- [ ] Confirm vulnerability affects us
- [ ] Identify patched version
- [ ] Check for breaking changes

### 2. Fix (1-2 hours)
- [ ] Create hotfix branch
- [ ] Update package
- [ ] Run critical tests
- [ ] Build and verify

### 3. Deploy (1 hour)
- [ ] Deploy to staging
- [ ] Smoke test
- [ ] Deploy to production
- [ ] Verify with security scan

### 4. Document
- [ ] Create incident report
- [ ] Update security log
- [ ] Notify stakeholders
```

### Medium/Low Severity

```markdown
## Planned Security Update

### During Sprint Planning
- [ ] Add to sprint backlog
- [ ] Estimate effort
- [ ] Assign owner

### During Sprint
- [ ] Update package
- [ ] Run full test suite
- [ ] Deploy normally
- [ ] Verify with audit
```

## Security Scanning CI/CD

### GitHub Actions

```yaml
name: Security Audit

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run audit
        run: npm audit --audit-level=high

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### GitLab CI

```yaml
security_audit:
  stage: test
  script:
    - npm ci
    - npm audit --audit-level=high
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

## Handling Unpatchable Vulnerabilities

### When No Fix Available

```markdown
## Vulnerability Without Fix: CVE-YYYY-XXXXX

### Options Analysis

#### Option 1: Wait for Patch
- **Pros:** Minimal effort
- **Cons:** Unknown timeline, continued exposure
- **Decision:** Not acceptable for high severity

#### Option 2: Fork and Patch
- **Pros:** Immediate fix
- **Cons:** Maintenance burden
- **Decision:** Consider for critical issues

#### Option 3: Replace Dependency
- **Pros:** Long-term solution
- **Cons:** Migration effort
- **Decision:** Best for medium-term

#### Option 4: Mitigate
- **Pros:** Quick, no code changes
- **Cons:** May not fully address
- **Decision:** Use as interim measure

### Chosen Approach
[Document decision and rationale]

### Mitigation Steps
1. [Specific mitigations applied]
2. [Monitoring added]
3. [Review schedule]
```

## Security Audit Schedule

```markdown
## Security Audit Calendar

### Daily (Automated)
- CI/CD security scans
- Alert on critical vulnerabilities

### Weekly
- [ ] Review security alerts
- [ ] Plan critical patches
- [ ] Check for new advisories

### Monthly
- [ ] Full dependency audit
- [ ] Review and update audit tools
- [ ] Security metrics review

### Quarterly
- [ ] Comprehensive security review
- [ ] Update security policies
- [ ] Third-party penetration test
```

## Reporting

### Security Log Format

```markdown
# Security Log: 2024-Q1

## Critical Updates

| Date | Package | CVE | Action |
|------|---------|-----|--------|
| 2024-01-15 | lodash | CVE-2021-23337 | Patched |
| 2024-02-01 | axios | CVE-2023-45857 | Patched |

## Accepted Risks

| Package | CVE | Reason | Review Date |
|---------|-----|--------|-------------|
| legacy-dep | CVE-2023-XXXXX | Not exploitable in our usage | 2024-04-01 |

## Metrics

- Vulnerabilities found: 12
- Vulnerabilities fixed: 10
- Average fix time: 2.3 days
- Open critical: 0
- Open high: 0
```
