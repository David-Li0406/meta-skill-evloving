# Enterprise Guide

Additional controls for regulated industries and large organizations.

**Read [Quick Start](QUICK_START.md) first.** This guide adds controls on top of the core workflow.

---

## Regulatory Considerations

### Before You Start

| Regulation | Key Concerns | Action Required |
|------------|--------------|-----------------|
| **HIPAA** | PHI in prompts, audit trails | Legal review required |
| **SOX** | Change management, audit trails | Document AI-assisted changes |
| **PCI-DSS** | Cardholder data, code review | Exclude payment code from AI |
| **GDPR** | Data residency, processing | Check Anthropic's DPA |
| **FedRAMP** | Cloud authorization | Verify Anthropic's compliance status |

**Consult your legal/compliance team before using AI on regulated systems.**

### Code Classification

Not all code should be AI-assisted. Classify first:

| Classification | AI-Assisted? | Examples |
|----------------|--------------|----------|
| **Critical** | No | Auth, payments, encryption, PII handling |
| **Sensitive** | With controls | Business logic with customer data |
| **Standard** | Yes | Utilities, CRUD, internal tools |
| **Low-risk** | Yes | Tests, documentation, scripts |

Add classification to CLAUDE.md:

```markdown
## Code Classification

DO NOT use AI for files in:
- src/auth/
- src/payments/
- src/encryption/

Human implementation required for security-critical code.
```

---

## Security Controls

### Tier 1: Prompt Hygiene (Required)

Prevent secrets in prompts:

```markdown
## CLAUDE.md Security Section

NEVER include in prompts or specs:
- API keys, tokens, credentials
- Customer data or PII
- Internal hostnames or IPs
- Database connection strings
```

### Tier 2: Server-Side Enforcement (Recommended)

Pre-commit hooks can be bypassed. Add server-side checks:

**GitHub Branch Protection:**
- Require PR reviews (human, not just AI)
- Require status checks (linting, security scans)
- Restrict who can push to main

**CI Pipeline Checks:**
```yaml
# .github/workflows/security.yml
- name: Secrets scan
  uses: trufflesecurity/trufflehog@main

- name: SAST scan
  uses: github/codeql-action/analyze@v2
```

### Tier 3: Network Controls (Large Orgs)

| Control | Implementation |
|---------|----------------|
| Egress filtering | Restrict Claude to approved domains |
| Prompt logging | Log all prompts for audit (sanitize secrets) |
| Data residency | Use region-specific API endpoints |
| Token budgets | Set per-team limits in Anthropic Console |

---

## Audit & Compliance

### What to Log

```
- Timestamp
- Developer ID
- Prompt hash (not full prompt—may contain sensitive data)
- Files modified
- Approval decision (approved/rejected)
- Reviewer ID
```

### Audit Trail Example

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "developer": "jsmith@company.com",
  "action": "ai_code_generation",
  "files_modified": ["src/routes/users.ts"],
  "tests_generated": 4,
  "iterations": 2,
  "approved_by": "jsmith@company.com",
  "review_duration_seconds": 180
}
```

### Change Management

For SOX/regulated environments:

1. **Document AI involvement** in PR descriptions
2. **Require human review** for all AI-generated code
3. **Tag commits** with `ai-assisted` label
4. **Maintain approval records** outside git (audit system)

---

## Large Organization Considerations

### Multi-Team Rollout

Don't transform everyone at once.

**Phase 1: Pilot (1 team, 1 month)**
- Low-risk internal project
- Measure: time saved, bugs introduced, cost
- Document learnings

**Phase 2: Expand (3-5 teams, 2 months)**
- Include one customer-facing project
- Refine based on pilot feedback
- Create internal playbook

**Phase 3: Scale (organization-wide)**
- Only after Phase 2 success
- Provide opt-out for teams where it doesn't fit
- Continuous feedback loop

### Monorepo Support

For large monorepos, create per-package CLAUDE.md files:

```
monorepo/
├── CLAUDE.md              # Repo-wide defaults
├── packages/
│   ├── auth/
│   │   └── CLAUDE.md      # "DO NOT use AI for this package"
│   ├── payments/
│   │   └── CLAUDE.md      # "DO NOT use AI for this package"
│   └── utils/
│       └── CLAUDE.md      # Package-specific context
```

### Cost Management

| Team Size | Estimated Monthly Cost | Budget Recommendation |
|-----------|------------------------|----------------------|
| 1-5 devs | $200-1,000 | Set alerts at 80% |
| 5-20 devs | $1,000-5,000 | Per-team budgets |
| 20+ devs | $5,000+ | Chargeback to teams |

Set up Anthropic Console alerts before rollout.

---

## Incident Response

### AI-Related Incident Types

1. **AI-generated bug in production**
2. **Sensitive data in prompt logs**
3. **Unauthorized code modification**
4. **Cost overrun**

### Response Playbook Addition

Add to existing incident response:

```markdown
## AI-Assisted Code Incidents

If production issue traced to AI-generated code:
1. Identify the commit and PR
2. Check audit log for approval chain
3. Review the original spec and generated tests
4. Determine if spec was ambiguous or AI hallucinated
5. Document in post-mortem
6. Update CLAUDE.md with new constraints if needed
```

---

## Migration & Rollback

### Hybrid Operation

Run traditional and AI-assisted workflows in parallel:

- AI-assisted for new features
- Traditional for legacy maintenance
- Team choice for bug fixes

### Rollback Triggers

Consider reverting if:
- Bug escape rate increases
- Developer satisfaction drops
- Costs exceed budget by 50%+
- Security incident occurs

### Rollback Steps

1. Remove AI-related git hooks
2. Archive CLAUDE.md files (don't delete—useful context)
3. Continue with traditional PR workflow
4. Conduct retrospective

---

## Checklist: Enterprise Readiness

Before organization-wide rollout:

- [ ] Legal/compliance review completed
- [ ] Code classification defined
- [ ] Server-side security controls in place
- [ ] Audit logging configured
- [ ] Cost budgets set per team
- [ ] Incident response playbook updated
- [ ] Pilot completed with documented results
- [ ] Rollback plan documented
- [ ] Training materials prepared
- [ ] Opt-out process defined for unsuitable teams
