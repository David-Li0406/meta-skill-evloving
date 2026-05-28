# Severity Classification Guide

## Severity Levels

### Critical (Score: 25 points deduction)

**Definition:** Immediate risk of significant harm. Production systems or sensitive data at risk.

**Response Time:** 15 minutes

**Examples:**
- AWS root account credentials
- Production AWS access keys (AKIA*)
- Production database credentials with write access
- GCP service account keys with owner/editor roles
- Azure service principal secrets (production)
- Payment processor live keys (Stripe sk_live_*, PayPal production)
- Private signing keys (code signing, TLS)
- Production SSH keys
- Admin/root passwords
- Encryption keys for production data

**Indicators:**
- `live`, `prod`, `production` in context
- Broad IAM permissions
- Access to PII/financial data
- Signing/encryption capability

---

### High (Score: 15 points deduction)

**Definition:** Significant risk but limited scope or requires additional factors to exploit.

**Response Time:** 1 hour

**Examples:**
- Staging/pre-prod database credentials
- GitHub tokens (ghp_*, github_pat_*)
- GitLab tokens (glpat-*)
- NPM publish tokens
- PyPI API tokens
- CI/CD pipeline credentials
- OAuth client secrets
- OAuth refresh tokens
- JWT signing secrets
- VPN credentials
- Docker registry credentials
- Anthropic API keys (sk-ant-*)
- OpenAI API keys (sk-*)
- AWS STS session tokens
- Database connection strings (staging)
- Kubernetes service account tokens

**Indicators:**
- Can modify code/infrastructure
- Access to internal systems
- Can impersonate service
- May contain user data

---

### Medium (Score: 5 points deduction)

**Definition:** Limited risk, constrained scope, or development/test environments.

**Response Time:** 24 hours

**Examples:**
- Slack tokens (xoxb-*, xoxp-*)
- Slack webhook URLs
- SendGrid API keys
- Twilio credentials
- Mailgun API keys
- Datadog API keys
- Sentry DSN tokens
- New Relic keys
- Segment write keys
- Discord bot tokens
- Development database credentials
- Local/development API keys
- Bearer tokens in test code
- Firebase credentials
- Supabase anon keys

**Indicators:**
- Third-party services
- Analytics/monitoring
- Communication services
- Scoped permissions
- Non-production data

---

### Low (Score: 2 points deduction)

**Definition:** Minimal risk, limited impact, or already partially mitigated.

**Response Time:** 1 week

**Examples:**
- Test/sandbox API keys (sk_test_*, sandbox-*)
- Mailchimp API keys (marketing, no PII)
- Public API keys (rate-limited, read-only)
- Expired credentials (still flag for cleanup)
- Credentials for decommissioned services
- Demo/tutorial credentials
- Publishable keys (Stripe pk_*)
- Hugging Face tokens (read-only models)

**Indicators:**
- Test/sandbox mode
- Read-only access
- No sensitive data access
- Rate-limited
- Already expired

---

### Informational (Score: 0 points deduction)

**Definition:** Not a secret, but may indicate presence of secrets or expose infrastructure details.

**Examples:**
- Public SSH keys
- X.509 certificates (public)
- AWS ARNs (resource identifiers)
- API endpoints (URLs without credentials)
- Service hostnames
- Account IDs (AWS account numbers)
- UUIDs/identifiers
- Content hashes

---

## Severity Modifiers

### Increase Severity

| Factor | Adjustment |
|--------|------------|
| Verified active (TruffleHog) | +1 level |
| Production context | +1 level |
| Public repository exposure | +1 level |
| Broad permissions | +1 level |
| Access to PII/financial data | +1 level |
| Can modify code/infrastructure | +1 level |
| Long-lived token | +1 level |

### Decrease Severity

| Factor | Adjustment |
|--------|------------|
| Test/example file | -1 level |
| Expired credential | -1 level |
| Sandbox/test environment | -1 level |
| Read-only permissions | -1 level |
| Internal/private repo only | -1 level |
| Short-lived token | -1 level |
| Rate-limited | -1 level |

---

## Risk Score Calculation

```
Base Score: 100
Deductions:
  - Critical findings × 25
  - High findings × 15
  - Medium findings × 5
  - Low findings × 2

Risk Score = max(0, 100 - total_deductions)
```

### Risk Levels

| Score Range | Level | Interpretation |
|-------------|-------|----------------|
| 95-100 | Excellent | No significant secrets detected |
| 80-94 | Low | Minor issues, review recommended |
| 60-79 | Medium | Several findings need attention |
| 40-59 | High | Significant exposure risk |
| 0-39 | Critical | Immediate action required |

---

## Classification Decision Tree

```
Is it a real secret (not placeholder/example)?
├─ No → Informational / False Positive
└─ Yes
   │
   Is it production/live?
   ├─ Yes → Is it infrastructure/signing/admin?
   │        ├─ Yes → CRITICAL
   │        └─ No → HIGH
   └─ No
      │
      Is it staging/internal?
      ├─ Yes → Is there sensitive data access?
      │        ├─ Yes → HIGH
      │        └─ No → MEDIUM
      └─ No (test/sandbox)
         │
         Can it be used to access other systems?
         ├─ Yes → MEDIUM
         └─ No → LOW
```

---

## Service-Specific Classification

### AWS
| Pattern | Default Severity |
|---------|-----------------|
| AKIA* (access key) | Critical |
| ASIA* (session key) | High |
| Root account | Critical |
| IAM user key | Critical/High |

### GitHub
| Pattern | Default Severity |
|---------|-----------------|
| ghp_* (PAT) | High |
| github_pat_* | High |
| GITHUB_TOKEN in workflow | Low |
| Deploy keys | High |

### Databases
| Context | Severity |
|---------|----------|
| Production connection string | Critical |
| Staging connection string | High |
| Local/development | Medium |
| Test fixtures | Low |

### API Services
| Service | Live | Test |
|---------|------|------|
| Stripe | Critical | Low |
| OpenAI | High | Medium |
| Anthropic | High | Medium |
| Twilio | Medium | Low |
| SendGrid | Medium | Low |

---

## Audit Trail

When classifying findings, document:

1. **Finding ID** - Unique identifier
2. **Initial classification** - Automated severity
3. **Manual adjustment** - Changed severity + reason
4. **Justification** - Why this classification
5. **Action taken** - Rotated/ignored/baseline
6. **Reviewer** - Who made the classification

Example:
```json
{
  "finding_id": "f-12345",
  "type": "aws_access_key",
  "initial_severity": "critical",
  "adjusted_severity": "high",
  "reason": "Key scoped to read-only S3 bucket, no sensitive data",
  "action": "rotated",
  "reviewer": "security-team",
  "date": "2024-01-15"
}
```
