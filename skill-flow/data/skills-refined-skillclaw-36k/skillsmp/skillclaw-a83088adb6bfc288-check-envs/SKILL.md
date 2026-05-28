---
name: check-envs
description: Use this skill when verifying environment setup or troubleshooting configuration issues by checking and validating all required environment variables in the .env file.
---

# Environment Variables Checker Skill

This skill validates the presence and configuration of environment variables required for the project.

## What This Skill Does

- Reads the `.env` file from the project root
- Checks for all required environment variables
- Categorizes variables by platform (Cloudflare, Supabase)
- Displays detailed status of each variable
- Provides setup guidance for missing variables
- Cross-platform support (Unix/Mac/Windows)

## Environment Variables Checked

### Cloudflare Workers (Required)

- `CLOUDFLARE_API` - API token for Cloudflare Workers deployment
- `CLOUDFLARE_ACCOUNT_ID` - Cloudflare account identifier

### Supabase (Optional)

- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_ANON_KEY` - Anonymous/public key for client-side use
- `SUPABASE_SERVICE_ROLE_KEY` - Service role key for server-side use
- `SUPABASE_PROJECT_REF` - Project reference ID for CLI operations

## Usage

### Via Claude Code Skill

```
/check-envs
```

### Manual Execution

**Unix/Mac/Linux:**

```bash
.claude/skills/check-envs/scripts/check-envs.sh
```

**Windows PowerShell:**

```powershell
.claude/skills/check-envs/scripts/check-envs.ps1
```

## Output Format

The skill provides color-coded output:

- ✅ **Green** - Variable is set and configured
- ⚠️ **Yellow** - Variable is set but has placeholder value
- ❌ **Red** - Variable is missing or not set

## Example Output

```
╔═══════════════════════════════════════════╗
║   Environment Variables Check             ║
╚═══════════════════════════════════════════╝

Cloudflare Workers (Required)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ CLOUDFLARE_API: Set
✅ CLOUDFLARE_ACCOUNT_ID: Set

Supabase (Optional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  SUPABASE_URL: Placeholder value detected
⚠️  SUPABASE_ANON_KEY: Placeholder value detected
❌ SUPABASE_SERVICE_ROLE_KEY: Not set
✅ SUPABASE_PROJECT_REF: Set

Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Required variables: 2/2 configured ✅
Optional variables: 2/4 configured
```

## When to Use This Skill

Use this skill when:

- Setting up the project for the first time
- Troubleshooting deployment issues
- Verifying environment configuration before deployment
- Onboarding new team members
- Switching between environments
- After updating credentials