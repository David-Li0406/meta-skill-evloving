# Secret Pattern Reference

## Secret Patterns (Regex)

| Pattern Name | Regex | Severity | Example |
|--------------|-------|----------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | CRITICAL | `AKIAIOSFODNN7EXAMPLE` |
| GitHub PAT | `ghp_[a-zA-Z0-9]{36}` | CRITICAL | `ghp_abcdef1234...` |
| Anthropic API | `sk-ant-api03-[a-zA-Z0-9_-]{95,}` | CRITICAL | `sk-ant-api03-...` |
| OpenAI API | `sk-proj-[a-zA-Z0-9_-]{48,}` | CRITICAL | `sk-proj-abc123...` |
| Generic API Key | `api[_-]?key[\s]*[=:]['"]?[a-zA-Z0-9]{20,}` | HIGH | `api_key = "sk_live..."` |
| JWT Token | `eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*` | HIGH | `eyJhbGc...` |
| Private Key | `-----BEGIN (RSA|EC|OPENSSH )?PRIVATE KEY-----` | CRITICAL | PEM format |
| DB URL | `(postgres|mysql|mongodb)://[^:]+:[^@]+@` | CRITICAL | `postgres://user:pass@host` |
| Password | `password[\s]*[=:][\s]*['"][^'"]{8,}` | HIGH | `password = "secret123"` |
| Bearer Token | `bearer\s+[a-zA-Z0-9]{20,}` | HIGH | `Bearer abc123...` |

---

## Forbidden File Patterns

```bash
*.env*                    # Environment files
*credentials*.json        # Credential files
*-key.json               # Key files
*_key.json
*.pem                    # Private keys
*.p12                    # Certificates
gcp-key.json             # GCP service account
service-account*.json    # Service accounts
```

---

## False Positive Indicators

Lines containing these keywords are likely safe:
- `example`, `placeholder`, `your-key-here`
- `test`, `fake`, `dummy`, `sample`, `mock`
- Prefixes: `FAKE_`, `TEST_`, `EXAMPLE_`
- Located in `tests/` or `docs/` directories

---

## Remediation

### If Secret Detected

```bash
# 1. Unstage the file
git reset HEAD <file>

# 2. Remove secret from code

# 3. Use SecretManager instead:
from src.secrets_manager import SecretManager
manager = SecretManager()
api_key = manager.get_secret("ANTHROPIC-API")

# 4. Commit clean version
```

### If Already Pushed

1. **Rotate immediately** - secret is compromised
2. Generate new secret
3. Update in GCP Secret Manager
4. Never try to hide with git rebase (history persists)

---

## Required .gitignore Entries

```gitignore
# Secrets
.env
.env.*
*.key
*.pem
*.p12
*-key.json
*_key.json
*credentials*.json
secrets/
.secrets/
```
