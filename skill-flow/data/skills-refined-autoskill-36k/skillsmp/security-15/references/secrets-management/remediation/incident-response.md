# Secret Exposure Incident Response

## Severity Classification

### Critical (Respond within 15 minutes)
- Production AWS/GCP/Azure credentials
- Production database credentials
- Payment processor keys (Stripe live, etc.)
- Private signing keys
- Admin/root credentials

### High (Respond within 1 hour)
- API keys with broad permissions
- OAuth refresh tokens
- CI/CD pipeline credentials
- SSH keys to production systems
- VPN/network credentials

### Medium (Respond within 24 hours)
- Development/staging credentials
- Test API keys
- Third-party service keys (analytics, monitoring)
- Sandbox payment keys

### Low (Respond within 1 week)
- Public API keys (rate-limited, read-only)
- Expired credentials
- Credentials for decommissioned services

---

## Immediate Response Steps

### Step 1: Revoke (0-15 minutes)

**Do not wait to assess impact.** Revoke immediately.

```bash
# AWS - deactivate key
aws iam update-access-key --access-key-id AKIA... --status Inactive

# GitHub - delete token
gh auth token | gh api -X DELETE /user/tokens/ID

# Database - change password
psql -c "ALTER USER username WITH PASSWORD 'new_password';"
```

### Step 2: Assess Exposure (15-60 minutes)

**Determine scope:**

1. **Where was it exposed?**
   - Public GitHub repository
   - Public S3 bucket
   - Paste site
   - Internal repo (less severe)

2. **How long was it exposed?**
   ```bash
   # Find when secret was added
   git log -p --all -S 'AKIA' --source --remotes
   ```

3. **Who had access?**
   - Public internet
   - Organization members only
   - Specific team members

4. **Was it indexed?**
   - Check GitHub search for the pattern
   - Check Google cache
   - Check archive.org

### Step 3: Generate New Credentials (30-60 minutes)

Create replacement credentials with same permissions:

```bash
# AWS
aws iam create-access-key --user-name USERNAME

# New database user
CREATE USER new_app_user WITH PASSWORD 'secure_password';
GRANT app_role TO new_app_user;
```

### Step 4: Update All Consumers (1-4 hours)

Identify and update all systems using the credential:

- [ ] Production applications
- [ ] Staging/development environments
- [ ] CI/CD pipelines
- [ ] Scheduled jobs/cron
- [ ] Third-party integrations
- [ ] Team members' local environments
- [ ] Documentation (remove or update)

### Step 5: Remove from Git History (if needed)

**Warning:** Rewriting history affects all collaborators.

```bash
# Using git-filter-repo (recommended)
pip install git-filter-repo
git filter-repo --invert-paths --path path/to/secret/file

# Or use BFG Repo-Cleaner
java -jar bfg.jar --delete-files secrets.env
java -jar bfg.jar --replace-text passwords.txt

# Force push (coordinate with team!)
git push --force --all
git push --force --tags
```

For GitHub:
1. Contact GitHub Support to clear caches
2. Rotate all credentials (history removal doesn't guarantee removal from forks/caches)

### Step 6: Monitor for Abuse (24-72 hours)

Check logs for unauthorized access:

**AWS:**
```bash
# CloudTrail - check for API calls with compromised key
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIA...
```

**Database:**
```sql
-- Check for unusual connections
SELECT * FROM pg_stat_activity
WHERE usename = 'compromised_user';

-- Check recent queries (if logging enabled)
SELECT * FROM pg_stat_statements
WHERE userid = 'compromised_user_id';
```

**Application logs:**
```bash
# Look for unusual patterns
grep -r "Bearer" /var/log/app/ | grep -v expected_patterns
```

---

## Post-Incident Actions

### Documentation

Create incident report including:

1. **Timeline**
   - When secret was committed
   - When exposure was discovered
   - When revocation completed
   - When new credentials deployed

2. **Impact Assessment**
   - Systems affected
   - Data potentially accessed
   - Cost (if applicable)

3. **Root Cause**
   - How was secret committed?
   - Why wasn't it caught?

4. **Remediation Steps Taken**
   - Credentials rotated
   - Systems updated
   - Monitoring added

5. **Prevention Measures**
   - Pre-commit hooks installed
   - Secret scanning enabled
   - Training conducted

### Prevention Improvements

After each incident, implement at least one improvement:

- [ ] Enable pre-commit secret scanning
- [ ] Enable GitHub push protection
- [ ] Add secret scanning to CI/CD
- [ ] Implement secret manager
- [ ] Reduce credential scope/permissions
- [ ] Implement credential rotation automation
- [ ] Add monitoring/alerting
- [ ] Conduct team training

---

## Communication Templates

### Internal Notification (Slack/Email)

```
🚨 SECURITY INCIDENT: Secret Exposure

What happened: [Brief description]
Impact: [Affected systems/data]
Status: [Investigating/Contained/Resolved]
Action required: [Update your local .env / Pull latest config]

Timeline:
- HH:MM - Exposure discovered
- HH:MM - Credentials revoked
- HH:MM - New credentials deployed

Contact: [Incident lead]
```

### External Notification (if customer data involved)

Work with legal/compliance team. Generally include:
- What happened
- What data was potentially affected
- What you're doing about it
- What customers should do (change passwords, etc.)
- Contact information

---

## Service-Specific Abuse Indicators

### AWS
- Unexpected EC2 instances (crypto mining)
- Unusual S3 access patterns
- New IAM users/roles created
- CloudTrail disabled
- Billing spikes

### GitHub
- New SSH keys added
- Webhooks modified
- Repository settings changed
- Branch protection disabled
- New collaborators added

### Database
- New users created
- Permission escalation
- Data export queries
- Connection from unusual IPs
- Schema modifications

### Stripe
- Unusual charge patterns
- New connected accounts
- Webhook endpoints modified
- Payout destinations changed

---

## Runbook Template

```markdown
# [Service] Credential Exposure Runbook

## Detection
- Alert source: [How discovered]
- Monitoring: [Dashboard link]

## Immediate Actions
1. [ ] Revoke credential: [command/console steps]
2. [ ] Generate new credential: [steps]
3. [ ] Update secrets manager: [steps]

## Systems to Update
- [ ] Production app: [deployment steps]
- [ ] Staging: [steps]
- [ ] CI/CD: [where to update]

## Verification
- [ ] Test application functionality
- [ ] Verify old credential rejected
- [ ] Check monitoring for errors

## Contacts
- On-call: [PagerDuty/phone]
- Service owner: [name]
- Security team: [channel]
```
