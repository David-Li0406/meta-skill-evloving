---
name: deep-env
description: Secure credential manager for environment variables. Use this skill when you see .env.example without .env.local, when user provides API keys or credentials, when setting up a new project, or when there are missing environment variable errors.
---

# deep-env - Credential Management

Use this skill to manage environment variables securely across all of Andrew's Macs.

## Architecture

**All credentials are stored in a SINGLE keychain entry as JSON.** This means only ONE keychain password prompt, ever - no matter how many credentials you have.

## When to Use This Skill

Automatically invoke this skill when:
- You see a `.env.example`, `.env.template`, or `.env.sample` file without a corresponding `.env.local`
- User provides an API key, secret, or credential
- Error messages mention missing environment variables (e.g., "ANTHROPIC_API_KEY is not defined")
- Setting up or cloning a new project
- User asks about credentials, secrets, or environment variables

## Known Projects

| Shortcut | Project | Path |
|----------|---------|------|
| `dp` | Deep Personality | `~/Deep-Personality` |

## Global vs Project-Specific Credentials

Credentials can be:
- **Global**: Available to all projects (e.g., ANTHROPIC_API_KEY, SUPABASE_*)
- **Project-specific**: Only for one project (e.g., ADMIN_EMAILS for Deep Personality)

### Current Project Assignments

**Global (all projects):**
- ANTHROPIC_API_KEY
- GMAIL_USER, GMAIL_APP_PASSWORD
- NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY
- SUPABASE_SERVICE_ROLE_KEY
- FIRECRAWL_API_KEY, APIFY_API_KEY

**Deep-Personality only:**
- ADMIN_EMAILS
- API_SECRET_KEY
- NEXT_PUBLIC_APP_URL

## Commands

### Sync credentials to a project
```bash
deep-env sync .                    # Current directory
deep-env sync ~/Deep-Personality   # Specific path
deep-env sync dp                   # Using shortcut
```

### Store credentials

```bash
# Global credential (available to all projects)
deep-env store ANTHROPIC_API_KEY "sk-ant-xxx"

# Project-specific credential
deep-env store -p dp ADMIN_EMAILS "admin@example.com"
deep-env store --project deep-personality API_SECRET_KEY "xxx"

# Push to iCloud after storing
deep-env push
```

### Assign existing keys to projects

```bash
# Assign to Deep Personality
deep-env assign ADMIN_EMAILS -p dp

# Make a key global
deep-env assign SOME_KEY --global
deep-env assign SOME_KEY -g

# Interactive assignment
deep-env assign KEY_NAME
```

### List credentials (grouped by project)
```bash
deep-env list
```

Output shows:
```
Global (all projects)
  ANTHROPIC_API_KEY       sk-a..._gAA
  GMAIL_USER              andr....com

Deep-Personality
  ADMIN_EMAILS            andr....com
  API_SECRET_KEY          kgg/...nSE=
```

### Backup and restore
```bash
deep-env backup            # Create timestamped backup
deep-env restore           # List available backups
deep-env restore <file>    # Restore from specific backup
deep-env validate          # Check keychain data integrity
deep-env --version         # Show version number
```

### Other commands
```bash
deep-env get KEY_NAME      # Get single value (for scripting)
deep-env delete KEY_NAME   # Remove a credential
deep-env import .env       # Import from existing file
deep-env export            # Output as shell exports
```

## Workflow

### When you see .env.example but no .env.local:
1. Run `deep-env sync .`
2. If keys are missing, ask user for values
3. Determine if key is project-specific or global:
   - URLs specific to the project (NEXT_PUBLIC_APP_URL) → project-specific
   - Admin emails, project secrets → project-specific
   - API keys for services (Anthropic, Supabase, etc.) → global
4. Store appropriately:
   - Global: `deep-env store KEY "value"`
   - Project: `deep-env store -p dp KEY "value"`
5. Push to iCloud: `deep-env push`
6. Re-run `deep-env sync .`

### When user provides a credential:
1. Determine if global or project-specific
2. Store it:
   - Global: `deep-env store KEY "value"`
   - Project: `deep-env store -p PROJECT KEY "value"`
3. Push to iCloud: `deep-env push`
4. If in a project, sync: `deep-env sync .`

### Cross-Mac sync
```bash
# On main Mac (after storing new credentials)
deep-env push

# On other Macs
deep-env pull          # Pulls credentials + project assignments
deep-env sync .        # Generate .env.local
```

### On a new Mac (if deep-env not installed):
```bash
# 1. Copy deep-env from iCloud
mkdir -p ~/.local/bin
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/deep-env ~/.local/bin/
chmod +x ~/.local/bin/deep-env

# 2. Ensure ~/.local/bin is in PATH (add to ~/.zshrc if needed)
export PATH="$HOME/.local/bin:$PATH"

# 3. Migrate any old individual keychain entries (one-time, safe to run)
deep-env migrate

# 4. Pull credentials from iCloud (will ask for sync password)
deep-env pull

# 5. Sync to projects as needed
deep-env sync /path/to/project
```

## Important Notes

- Never commit `.env.local` to git
- Always `deep-env push` after storing new credentials
- The sync password is known only to the user - ask if needed
- **All credentials stored in a single keychain entry** = only 1 password prompt ever
- Credentials are stored in macOS Keychain (hardware-backed on Apple Silicon)
- iCloud sync uses AES-256 encryption
- Project assignments are stored in `~/.config/deep-env/project-keys.json`
- Run `deep-env migrate` once per Mac to move old individual entries to new format
- Multi-line values (like PEM keys) are fully supported

## New Mac Setup Checklist

1. [ ] Copy CLI: `cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/deep-env ~/.local/bin/`
2. [ ] Make executable: `chmod +x ~/.local/bin/deep-env`
3. [ ] Add to PATH: `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc`
4. [ ] Pull credentials: `deep-env pull` (enter sync password)
5. [ ] Validate: `deep-env validate`
6. [ ] Verify: `deep-env list` (should show all credentials)
7. [ ] Test sync: `cd ~/some-project && deep-env sync .`

## Common Issues and Fixes

### "Pulled 0 credentials" But iCloud Has Data

**Symptoms:**
- `deep-env pull` reports success
- Says "Pulled 0 credentials from iCloud"
- `deep-env list` shows "No credentials stored yet"
- But `credentials.enc` exists in iCloud

**Diagnosis:**
```bash
# Check if encrypted file exists
ls -lh ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/credentials.enc

# Try manual decryption (replace PASSWORD)
openssl enc -d -aes-256-cbc -pbkdf2 \
  -in ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/credentials.enc \
  -pass pass:PASSWORD | wc -c
```

If the manual decryption shows a large number (>15000 bytes), the payload is too large for a single keychain entry.

**Fix:**
1. **Split credentials by project:**
   ```bash
   # Move project-specific credentials
   deep-env store CRON_SECRET "value" --project
   deep-env store SESSION_SECRET "value" --project
   ```

2. **Use environment-specific credentials:**
   Keep global API keys (Anthropic, OpenAI) global, but store app-specific secrets per project.

3. **Manual recovery (if needed):**
   ```bash
   # Decrypt and store manually
   openssl enc -d -aes-256-cbc -pbkdf2 \
     -in ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/credentials.enc \
     -pass pass:YOUR_PASSWORD | \
     security add-generic-password -s "deep-env-credentials" -a "deep-env" -w /dev/stdin
   ```

### iCloud Sync Not Working

**Diagnosis:**
```bash
# Check iCloud Drive status
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/

# Check file modification time
stat ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/credentials.enc
```

**Fix:**
1. Open System Settings → Apple ID → iCloud Drive
2. Ensure iCloud Drive is enabled
3. Wait 2-3 minutes for sync to complete
4. Try `deep-env pull` again

### Large Credential Sets (80+ keys)

If you have many credentials, the JSON payload may exceed macOS Keychain's limit (~16KB per entry).

**Solution: Use Project-Specific Storage**

Instead of storing everything globally:
```bash
# Global (shared across all projects)
deep-env store ANTHROPIC_API_KEY "sk-ant-..." --global
deep-env store OPENAI_API_KEY "sk-..." --global

# Project-specific (only for this project)
cd ~/my-project
deep-env store CRON_SECRET "abc123" --project
deep-env store SESSION_SECRET "xyz789" --project
```

This splits the credentials into smaller chunks that fit within Keychain limits.

## Troubleshooting

### "No credentials stored" but you had credentials

This usually means corrupted data. Run diagnostics:
```bash
deep-env validate
```

**If validation fails:**
1. Check for backups: `ls ~/.config/deep-env/backups/`
2. Restore from backup: `deep-env restore <backup_file>`
3. Or pull from iCloud: `deep-env pull`

### Sync password forgotten

The sync password is stored locally in `~/.config/deep-env/.sync_pass`. If you have another Mac with deep-env working:
1. On working Mac: `cat ~/.config/deep-env/.sync_pass`
2. Use that password on new Mac

### Pull fails with "Decryption failed"

Wrong sync password. Check another Mac or re-push from a Mac with working credentials.

### Credentials not syncing to other Macs

After storing credentials, always run:
```bash
deep-env push
```

Then on other Macs:
```bash
deep-env pull
```

### Validate shows "hex-encoded" or "literal newlines"

The keychain data is corrupted. Recovery options:
1. Restore from backup: `deep-env restore`
2. Pull from iCloud: `deep-env pull`

## Recovery Procedures

### From Local Backup
```bash
# List backups
deep-env restore

# Restore specific backup
deep-env restore ~/.config/deep-env/backups/credentials_20260115_120000.json
```

### From iCloud (if local is corrupted)
```bash
deep-env pull
# Enter sync password
```

### Manual Recovery (last resort)

If keychain has hex-encoded data, decode and fix:
```bash
# Read hex, decode to file
security find-generic-password -a "deep-env" -s "deep-env-credentials" -w | xxd -r -p > /tmp/raw.json

# Fix any issues in the JSON manually, then:
security delete-generic-password -a "deep-env" -s "deep-env-credentials"
security add-generic-password -a "deep-env" -s "deep-env-credentials" -w "$(cat /tmp/fixed.json)"

# Clean up
rm /tmp/raw.json /tmp/fixed.json
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-15 | Added backup/restore/validate commands, fixed push/pull JSON corruption, auto-backup before pull |
| 1.0.0 | 2024-12-01 | Initial release with single keychain entry storage |
