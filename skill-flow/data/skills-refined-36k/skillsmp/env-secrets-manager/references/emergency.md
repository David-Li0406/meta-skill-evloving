# Emergency Procedures

## If Token is Compromised

1. **Immediately revoke** the token at source (GitHub, Notion, etc.)
2. **Generate new token** with same permissions
3. **Rotate across all projects**:
   ```bash
   /env-secrets-manager rotate COMPROMISED_TOKEN --emergency
   ```
4. **Scan git history** to ensure token not in commits:
   ```bash
   /env-secrets-manager scan --history --secret COMPROMISED_TOKEN
   ```
5. **Monitor** for unauthorized usage

## If .env File Accidentally Committed

1. **DO NOT just delete** the file in next commit (secret remains in history)
2. **Rotate all secrets** in that file immediately
3. **Remove from git history**:
   ```bash
   /env-secrets-manager scan --fix --file .env.local
   ```
4. **Force push** (coordinate with team)

## Manual Git History Cleanup

```bash
# Remove .env from entire git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env.local" \
  --prune-empty --tag-name-filter cat -- --all

# Force push all branches
git push origin --force --all

# Force push tags
git push origin --force --tags
```

## Token Revocation Links

- **GitHub**: https://github.com/settings/tokens
- **Notion**: https://www.notion.so/my-integrations
- **Supabase**: Project Settings → API
- **OpenAI**: https://platform.openai.com/api-keys
- **Vercel**: https://vercel.com/account/tokens
