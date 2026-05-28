**Skill**: [Doppler Credential Workflows](../SKILL.md)

## Multi-Service / Multi-Account Patterns

### Multiple PyPI Packages

```bash
# Package 1
doppler run --project claude-config --config dev \
  --command='uv publish --token "$PYPI_TOKEN"'

# Package 2
doppler run --project claude-config --config dev \
  --command='uv publish --token "$PYPI_TOKEN_GCD"'
```

### Multiple AWS Accounts

```bash
# Deploy to staging
doppler run --project aws-credentials --config staging \
  --command='aws s3 sync dist/ s3://staging-bucket/'

# Deploy to production
doppler run --project aws-credentials --config prod \
  --command='aws s3 sync dist/ s3://prod-bucket/'
```
