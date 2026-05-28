---
name: check-envs
description: Check and validate all required environment variables in .env file. Use when verifying environment setup or troubleshooting configuration issues.
---

# Environment Variables Checker Skill

This skill validates the presence and configuration of environment variables required for the project.

## What This Skill Does

- Reads the `.env` file from project root
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

## Error Handling

### .env File Not Found

If the `.env` file doesn't exist, the skill will:

1. Report that no `.env` file was found
2. Suggest creating one from `.env.example`
3. Provide instructions on how to obtain credentials

### Missing Required Variables

If required Cloudflare variables are missing:

1. Display which variables are missing
2. Provide links to obtain the credentials
3. Exit with error status

### Placeholder Values Detected

If variables contain placeholder values like:

- `your-*-here`
- `<your-*>`
- `xxxxx`

The skill will warn that these need to be replaced with actual values.

## Setup Instructions Provided

When variables are missing or have placeholders, the skill provides:

### For Cloudflare:

- Link to Cloudflare Dashboard
- Link to API token generation
- Required permissions list

### For Supabase:

- Link to Supabase Dashboard
- Navigation path to API settings
- Explanation of each key type and usage

## Integration with Other Skills

This skill works well with:

- `/dependencies` - Check environment before installing dependencies
- `/deployment` - Validate configuration before deployment

## Future Enhancements

Planned improvements:

- Validate format of environment variables (URL format, token length, etc.)
- Check for common configuration mistakes
- Suggest fixes for detected issues
- Support for multiple environment files (.env.development, .env.production)
- Export environment report to file
- Integration with CI/CD pipelines
