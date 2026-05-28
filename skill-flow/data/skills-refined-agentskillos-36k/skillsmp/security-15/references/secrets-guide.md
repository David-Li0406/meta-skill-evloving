# Secrets Management Guide

Patterns for detecting, preventing, and managing secrets in code.

## Secret Patterns to Detect

### High-Confidence Patterns

```regex
# API Keys
(?i)(api[_-]?key|apikey)\s*[:=]\s*['"][a-zA-Z0-9]{16,}['"]

# AWS
AKIA[0-9A-Z]{16}
(?i)aws[_-]?secret[_-]?access[_-]?key

# Private Keys
-----BEGIN\s*(RSA|DSA|EC|OPENSSH)?\s*PRIVATE KEY-----

# Generic Secrets
(?i)(password|passwd|pwd|secret|token)\s*[:=]\s*['"][^'"]{8,}['"]

# Connection Strings
(?i)(mongodb|postgres|mysql|redis):\/\/[^:]+:[^@]+@
```

### Platform-Specific Patterns

| Platform | Pattern | Example |
|----------|---------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | `AKIAIOSFODNN7EXAMPLE` |
| AWS Secret Key | 40 char base64 | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| GitHub Token | `ghp_[a-zA-Z0-9]{36}` | `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| GitLab Token | `glpat-[a-zA-Z0-9]{20}` | `glpat-xxxxxxxxxxxxxxxxxxxx` |
| Slack Token | `xox[baprs]-...` | `xoxb-123456789012-...` |
| Stripe | `sk_live_[a-zA-Z0-9]{24}` | `sk_live_EXAMPLE_KEY_ONLY` |
| OpenAI | `sk-[a-zA-Z0-9]{48}` | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

## Secure Secret Storage

### Environment Variables

```bash
# .env (never commit)
DATABASE_URL=postgres://user:pass@host/db
API_KEY=your-api-key-here

# .env.example (commit this)
DATABASE_URL=postgres://user:pass@localhost/db_dev
API_KEY=your-api-key-here
```

### Secret Managers

```javascript
// AWS Secrets Manager
const { SecretsManager } = require('@aws-sdk/client-secrets-manager');
const client = new SecretsManager({ region: 'us-east-1' });

async function getSecret(secretName) {
  const response = await client.getSecretValue({ SecretId: secretName });
  return JSON.parse(response.SecretString);
}

// HashiCorp Vault
const vault = require('node-vault')({ endpoint: process.env.VAULT_ADDR });
const secret = await vault.read('secret/data/myapp');
```

### Git Configuration

```gitignore
# .gitignore - Always include
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
secrets.yaml
config/secrets/
```

## Secret Scanning Tools

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.63.0
    hooks:
      - id: trufflehog
```

### CI Integration

```yaml
# GitHub Actions
- name: Gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# GitLab CI
secret_detection:
  stage: test
  image: registry.gitlab.com/gitlab-org/security-products/secret-detection:latest
  script:
    - /analyzer run
```

## Remediation

### If Secret Was Committed

1. **Rotate immediately** - Consider the secret compromised
2. **Remove from history** (if recent):
   ```bash
   # Using git-filter-repo (preferred)
   git filter-repo --invert-paths --path secrets.env

   # Force push (coordinate with team)
   git push --force-with-lease
   ```
3. **Add to .gitignore** to prevent recurrence
4. **Audit access logs** for the compromised credential

### Secret Rotation Checklist

- [ ] Generate new credential
- [ ] Update secret manager/environment
- [ ] Deploy updated configuration
- [ ] Revoke old credential
- [ ] Audit for unauthorized use
- [ ] Document incident
