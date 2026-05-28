# Secret Exposure Prevention

## Pre-Commit Hooks

### Git Hooks with detect-secrets

```bash
# Install detect-secrets
pip install detect-secrets

# Initialize baseline (tracks known false positives)
detect-secrets scan > .secrets.baseline

# Add pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
detect-secrets-hook --baseline .secrets.baseline $(git diff --cached --name-only)
EOF
chmod +x .git/hooks/pre-commit
```

### Git Hooks with TruffleHog

```bash
# Install TruffleHog
brew install trufflehog  # or download from releases

# Pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
trufflehog git file://. --since-commit HEAD --only-verified --fail
EOF
chmod +x .git/hooks/pre-commit
```

### Using pre-commit Framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.63.0
    hooks:
      - id: trufflehog
        args: ['--only-verified']
```

```bash
# Install and setup
pip install pre-commit
pre-commit install
```

---

## .gitignore Best Practices

### Essential Entries

```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.production
.env.development

# Credentials
credentials.json
service-account.json
*.pem
*.key
*.p12
*.pfx
*.jks

# SSH keys
id_rsa
id_dsa
id_ecdsa
id_ed25519
*.pub  # Optional - public keys aren't secrets

# AWS
.aws/credentials
.aws/config

# Cloud configs
.gcloud/
.azure/

# IDE secrets
.idea/secrets.xml
.vscode/settings.json  # May contain secrets

# Database
*.sqlite
*.db
dump.sql

# Logs (may contain secrets)
*.log
logs/

# OS files
.DS_Store
Thumbs.db
```

### Template Files (DO commit)

```gitignore
# Don't ignore example files
!.env.example
!.env.template
!credentials.example.json
```

---

## Environment Variable Management

### dotenv Pattern

```bash
# .env.example (commit this)
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
API_KEY=your_api_key_here
SECRET_KEY=generate_a_secure_random_string

# .env (never commit)
DATABASE_URL=postgresql://realuser:realpassword@prod-host:5432/proddb
API_KEY=sk-real-api-key-here
SECRET_KEY=actually-secure-random-string
```

### direnv for Project-Specific Secrets

```bash
# Install direnv
brew install direnv

# .envrc file (add to .gitignore)
export DATABASE_URL="postgresql://..."
export API_KEY="sk-..."

# Allow in project
direnv allow
```

---

## Secret Managers

### AWS Secrets Manager

```python
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# Usage
db_password = get_secret('prod/database/password')
```

### HashiCorp Vault

```python
import hvac

client = hvac.Client(url='https://vault.example.com')
client.token = os.environ['VAULT_TOKEN']

secret = client.secrets.kv.v2.read_secret_version(path='myapp/config')
api_key = secret['data']['data']['api_key']
```

### 1Password CLI

```bash
# Reference secrets in .env
DATABASE_URL=op://vault/database/connection-string

# Load with 1Password CLI
op run --env-file=.env -- npm start
```

### Doppler

```bash
# Setup
doppler setup

# Run with secrets injected
doppler run -- npm start
```

---

## CI/CD Best Practices

### GitHub Actions

```yaml
# Use secrets, not hardcoded values
env:
  API_KEY: ${{ secrets.API_KEY }}

# Use OIDC for cloud providers (no static credentials)
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/my-role
      aws-region: us-east-1
```

### GitLab CI

```yaml
# Use CI/CD variables (Settings > CI/CD > Variables)
variables:
  API_KEY: $API_KEY  # Masked variable

# Use Vault integration
secrets:
  DATABASE_PASSWORD:
    vault: production/db/password@secrets
```

### Avoid These Patterns

```yaml
# BAD: Secret in workflow file
env:
  API_KEY: "sk-actual-secret-key"

# BAD: Secret in run command
run: curl -H "Authorization: Bearer sk-secret" https://api.example.com

# BAD: Echo secrets (visible in logs)
run: echo ${{ secrets.API_KEY }}
```

---

## Code Patterns to Avoid

### Hardcoded Secrets

```python
# BAD
api_key = "sk-1234567890abcdef"
connection_string = "postgresql://admin:password123@localhost/db"

# GOOD
api_key = os.environ.get('API_KEY')
connection_string = os.environ.get('DATABASE_URL')
```

### Default Values with Real Secrets

```javascript
// BAD - fallback is a real secret
const apiKey = process.env.API_KEY || 'sk-production-key';

// GOOD - fail if not set
const apiKey = process.env.API_KEY;
if (!apiKey) throw new Error('API_KEY is required');

// GOOD - safe default for development
const apiKey = process.env.API_KEY || 'development-placeholder';
```

### Logging Secrets

```python
# BAD
logger.info(f"Connecting with credentials: {username}:{password}")

# GOOD
logger.info(f"Connecting as user: {username}")
```

---

## Development Environment

### Local Development

1. **Use `.env.example`** as template
2. **Copy to `.env`** and fill in values
3. **Never commit `.env`** - verify with `git status`
4. **Use test/sandbox credentials** when possible

### Shared Development Secrets

Options for team secret sharing:
- 1Password/LastPass team vaults
- Doppler for environment management
- AWS Secrets Manager with developer access
- HashiCorp Vault with LDAP/SSO

---

## Audit and Monitoring

### Regular Scans

```bash
# Scan repository
trufflehog git file://. --only-verified

# Scan git history
trufflehog git file://. --since-commit $(git rev-list --max-parents=0 HEAD)
```

### GitHub Secret Scanning

Enable in repository settings:
- Settings > Security > Code security and analysis
- Enable "Secret scanning"
- Enable "Push protection" to block commits with secrets

### Automated Alerts

- Set up CI job to run secret scans on PRs
- Configure Slack/email alerts for findings
- Use GitHub Secret Scanning partner alerts
