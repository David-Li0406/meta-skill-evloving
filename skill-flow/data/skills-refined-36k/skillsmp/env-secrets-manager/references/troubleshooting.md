# Troubleshooting Guide

## "API token is invalid"

**Cause:** Token expired, revoked, or wrong type

**Fix:**
```bash
# 1. Check token is set
echo $NOTION_TOKEN

# 2. Test token directly
curl -H "Authorization: Bearer $NOTION_TOKEN" \
     -H "Notion-Version: 2022-06-28" \
     https://api.notion.com/v1/users/me

# 3. If invalid, rotate token
/env-secrets-manager rotate NOTION_TOKEN
```

## "Secret not found in GitHub Actions"

**Cause:** Secret not added to repository secrets

**Fix:**
```bash
# Add secret to repo
gh secret set NOTION_TOKEN < .env.local

# Or use the skill
/env-secrets-manager sync
```

## "Secrets out of sync across repos"

**Cause:** Secrets updated in one place but not others

**Fix:**
```bash
# Sync all secrets across all repos
/env-secrets-manager sync --all

# Or audit to see differences
/env-secrets-manager audit
```

## "Hardcoded secret detected by GitHub"

**Cause:** Secret committed to git history

**Fix:**
```bash
# Scan for hardcoded secrets
/env-secrets-manager scan

# Remove from history (USE WITH CAUTION)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env.local" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (coordinate with team first!)
git push origin --force --all
```

## Common Token Testing

### Notion
```bash
curl -H "Authorization: Bearer $NOTION_TOKEN" \
     -H "Notion-Version: 2022-06-28" \
     https://api.notion.com/v1/users/me
```

### GitHub
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/user
```

### Supabase
```bash
curl "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/" \
     -H "apikey: $SUPABASE_SERVICE_ROLE_KEY"
```
