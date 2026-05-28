# Secret Rotation Procedures

## Immediate Response Checklist

When a secret is exposed:

1. **Revoke immediately** - Don't wait to assess impact
2. **Generate new credentials** - Create replacement secrets
3. **Update all consumers** - Applications, CI/CD, team members
4. **Verify functionality** - Ensure new secrets work
5. **Monitor for abuse** - Check logs for unauthorized access
6. **Document incident** - Record timeline and actions taken

---

## Cloud Provider Credentials

### AWS Access Keys

```bash
# 1. Create new access key (AWS Console or CLI)
aws iam create-access-key --user-name USERNAME

# 2. Update applications with new key

# 3. Deactivate old key (allows rollback)
aws iam update-access-key --access-key-id OLD_KEY_ID --status Inactive --user-name USERNAME

# 4. Test thoroughly, then delete old key
aws iam delete-access-key --access-key-id OLD_KEY_ID --user-name USERNAME
```

**Best Practice**: Use IAM roles instead of access keys where possible.

### GCP Service Account Keys

```bash
# 1. Create new key
gcloud iam service-accounts keys create new-key.json \
  --iam-account SERVICE_ACCOUNT_EMAIL

# 2. Update applications

# 3. Delete old key
gcloud iam service-accounts keys delete OLD_KEY_ID \
  --iam-account SERVICE_ACCOUNT_EMAIL
```

**Best Practice**: Use Workload Identity for GKE, or short-lived tokens.

### Azure Service Principal

```bash
# 1. Create new client secret
az ad app credential reset --id APP_ID --append

# 2. Update applications

# 3. Remove old credential
az ad app credential delete --id APP_ID --key-id OLD_KEY_ID
```

---

## API Keys

### OpenAI

1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Update applications
4. Delete old key from dashboard

### Anthropic

1. Go to https://console.anthropic.com/settings/keys
2. Create new API key
3. Update applications
4. Delete old key

### Stripe

```bash
# Stripe keys can be rolled from Dashboard
# Settings > API Keys > Roll Key
```

1. Roll the secret key (creates new, old works for 24h)
2. Update applications within 24 hours
3. Old key automatically expires

### GitHub Tokens

1. Go to Settings > Developer settings > Personal access tokens
2. Generate new token with same scopes
3. Update applications
4. Delete old token

For fine-grained PATs, regenerate or delete from the same page.

---

## Database Credentials

### PostgreSQL

```sql
-- 1. Create new user or change password
ALTER USER username WITH PASSWORD 'new_secure_password';

-- Or create new user
CREATE USER new_username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dbname TO new_username;

-- 2. Update connection strings in applications

-- 3. Remove old user if created new one
DROP USER old_username;
```

### MySQL

```sql
-- Change password
ALTER USER 'username'@'host' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### MongoDB

```javascript
// Change password
db.changeUserPassword("username", "newPassword")
```

### Redis

```bash
# Update redis.conf
requirepass new_secure_password

# Or via CLI
CONFIG SET requirepass "new_secure_password"
```

---

## Communication Services

### Slack

1. Go to api.slack.com/apps > Your App > OAuth & Permissions
2. Reinstall app to workspace (generates new tokens)
3. Update applications
4. Old tokens are automatically revoked

### Twilio

1. Go to Console > Account > API Credentials
2. Create secondary credentials
3. Update applications
4. Delete primary credentials

### SendGrid

1. Go to Settings > API Keys
2. Create new API key
3. Update applications
4. Delete old key

---

## Certificates and Private Keys

### TLS Certificates

```bash
# 1. Generate new private key
openssl genrsa -out new-key.pem 4096

# 2. Generate CSR
openssl req -new -key new-key.pem -out new.csr

# 3. Submit CSR to CA and get new certificate

# 4. Deploy new certificate and key

# 5. Revoke old certificate with CA
```

### SSH Keys

```bash
# 1. Generate new key pair
ssh-keygen -t ed25519 -f ~/.ssh/new_key

# 2. Add new public key to authorized_keys on servers

# 3. Update applications/scripts to use new key

# 4. Remove old public key from authorized_keys

# 5. Delete old private key
```

### Let's Encrypt

```bash
# Force renewal (revokes and replaces)
certbot revoke --cert-path /etc/letsencrypt/live/domain/cert.pem
certbot certonly -d domain.com
```

---

## CI/CD Secrets

### GitHub Actions

1. Go to Repository Settings > Secrets and variables > Actions
2. Update secret value (same name replaces old)
3. Re-run workflows to verify

### GitLab CI

1. Go to Settings > CI/CD > Variables
2. Update variable value
3. Re-run pipelines to verify

### CircleCI

1. Go to Project Settings > Environment Variables
2. Delete old variable
3. Add new variable with same name
4. Re-run builds to verify

---

## Automation Tips

### Secret Rotation Script Template

```bash
#!/bin/bash
# Generic rotation script template

# 1. Generate new secret
NEW_SECRET=$(generate_new_secret)

# 2. Store in secret manager
aws secretsmanager update-secret --secret-id my-secret --secret-string "$NEW_SECRET"

# 3. Trigger application restart/reload
kubectl rollout restart deployment/my-app

# 4. Verify health
sleep 30
curl -f https://my-app.com/health || exit 1

# 5. Log rotation event
echo "$(date): Rotated my-secret" >> /var/log/secret-rotations.log
```

### Using Secret Managers

AWS Secrets Manager:
```bash
aws secretsmanager rotate-secret --secret-id my-secret
```

HashiCorp Vault:
```bash
vault write -force auth/token/revoke-self
vault token create -policy=my-policy
```

---

## Rotation Frequency Guidelines

| Secret Type | Recommended Frequency |
|-------------|----------------------|
| AWS Root Credentials | Never use, use IAM |
| AWS IAM Keys | 90 days |
| Database Passwords | 90 days |
| API Keys | Annually or on exposure |
| SSH Keys | Annually |
| TLS Certificates | Before expiry (automate) |
| Service Account Tokens | 90 days |
| Signing Keys | Annually |

**After any suspected exposure**: Rotate immediately regardless of schedule.
