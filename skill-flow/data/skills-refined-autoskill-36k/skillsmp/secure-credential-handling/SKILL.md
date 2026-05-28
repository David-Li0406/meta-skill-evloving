---
name: Secure Credential Handling
description: This skill should be used when the user asks to "store credentials", "secure API keys", "save SSH keys", "manage secrets", "prevent credential leaks", "encrypt tokens", or mentions system keychain, credential vault, or secret management. Provides comprehensive guidance for secure credential storage and leak prevention.
version: 1.0.0
---

# Secure Credential Handling

## Purpose

This skill provides guidance for securely storing, retrieving, and managing credentials (API keys, private keys, OAuth tokens, database passwords) using system-native keychains and implementing comprehensive leak prevention to protect secrets from accidental exposure in git commits, logs, or command execution.

## When to Use This Skill

Load this skill when working with:
- Storing API keys, tokens, or passwords securely
- Managing SSH private keys or GPG keys
- Implementing OAuth token storage with refresh
- Preventing credential leaks in git, bash commands, or file writes
- Setting up per-project credential isolation
- Integrating with system keychains (macOS Keychain, Windows Credential Manager, Linux Secret Service)

## System Keychain Integration

### Platform-Specific Implementations

**macOS - Keychain Access:**
```bash
# Store credential
security add-generic-password \
  -a "claude-code" \
  -s "project-context:project-name:credential-name" \
  -w "credential-value" \
  -U

# Retrieve credential
security find-generic-password \
  -a "claude-code" \
  -s "project-context:project-name:credential-name" \
  -w
```

**Linux - Secret Service (GNOME Keyring / KWallet):**
```bash
# Requires secret-tool (libsecret)
# Store credential
secret-tool store \
  --label="Project Context: credential-name" \
  service "claude-code" \
  project "project-name" \
  credential "credential-name"

# Retrieve credential
secret-tool lookup \
  service "claude-code" \
  project "project-name" \
  credential "credential-name"
```

**Windows - Credential Manager:**
```powershell
# Store credential
cmdkey /generic:"claude-code:project-name:credential-name" \
       /user:"credential-type" \
       /pass:"credential-value"

# Retrieve credential
$cred = Get-StoredCredential -Target "claude-code:project-name:credential-name"
$cred.GetNetworkCredential().Password
```

### Credential Naming Convention

Use hierarchical naming for credential isolation:
```
service:project:name
└─ claude-code:qenex-api:github-deploy-token
└─ claude-code:webapp:stripe-api-key
└─ claude-code:infra:aws-access-key
```

## Credential Types and Storage Patterns

### API Keys (String Tokens)

**Storage:**
```bash
# Direct string storage in keychain
/store-credential --name "github-api" --type "api-key" --value "$API_KEY"
```

**Retrieval:**
```python
# Never log or print - use directly
api_key = get_credential("github-api")
headers = {"Authorization": f"Bearer {api_key}"}
```

### Private Keys (SSH, GPG)

**Storage:**
```bash
# Store file contents
/store-credential --name "deploy-key" --type "ssh-key" --file ~/.ssh/deploy_key

# Or store key material directly
cat ~/.ssh/deploy_key | /store-credential --name "deploy-key" --type "ssh-key" --stdin
```

**Retrieval:**
```bash
# Write to temporary file with secure permissions
get_credential("deploy-key") > /tmp/deploy_key
chmod 600 /tmp/deploy_key
ssh -i /tmp/deploy_key user@host
rm -f /tmp/deploy_key
```

### OAuth Tokens (with Refresh)

**Storage:**
```json
{
  "access_token": "ya29.a0...",
  "refresh_token": "1//0g...",
  "expires_at": 1737542400,
  "token_type": "Bearer"
}
```

Store as JSON string in keychain with automatic refresh logic.

### Database Credentials

**Storage:**
```bash
# Store as structured JSON
/store-credential --name "prod-db" --type "database" \
  --username "admin" \
  --password "$DB_PASS" \
  --host "db.example.com" \
  --port "5432" \
  --database "production"
```

## Credential Leak Prevention

### Three-Layer Protection

**Layer 1: PreToolUse Hook - Command Scanning**

Intercept tool calls before execution to detect credential patterns:
```bash
# In hooks/hooks.json
{
  "PreToolUse": [{
    "matcher": "Bash|Edit|Write",
    "hooks": [{
      "type": "command",
      "command": "bash $CLAUDE_PLUGIN_ROOT/scripts/security/scan-tool-call.sh"
    }]
  }]
}
```

**Layer 2: Git Commit Scanning**

Prevent commits containing secrets:
```bash
# Pre-commit hook (git hooks integration)
git diff --cached | grep -E "(api[_-]?key|password|secret|token|private[_-]?key)" && {
  echo "ERROR: Potential credential detected in commit"
  exit 1
}
```

**Layer 3: File Write Detection**

Alert when writing files with credential patterns:
```python
# Pattern detection
CREDENTIAL_PATTERNS = [
    r'api[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
    r'password\s*[:=]\s*["\']?.{8,}',
    r'-----BEGIN (RSA|OPENSSH|PGP) PRIVATE KEY-----',
    r'[a-zA-Z0-9]{40}',  # GitHub tokens
    r'sk-[a-zA-Z0-9]{20,}',  # Anthropic API keys
]
```

See `scripts/security/detect-credentials.py` for full implementation.

### Safe Credential Usage Patterns

**Pattern 1: Environment Variables (Transient)**
```bash
# Set for single command execution
API_KEY=$(get_credential "api-key") curl -H "Authorization: Bearer $API_KEY" https://api.example.com

# Unset immediately after use
unset API_KEY
```

**Pattern 2: Temporary Files (Secure Permissions)**
```python
import tempfile
import os

def use_private_key(key_name):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
        key_content = get_credential(key_name)
        f.write(key_content)
        temp_path = f.name

    os.chmod(temp_path, 0o600)

    try:
        # Use key file
        subprocess.run(['ssh', '-i', temp_path, 'user@host'])
    finally:
        os.unlink(temp_path)  # Always cleanup
```

**Pattern 3: In-Memory Only (Never Write)**
```python
# BAD: Writing to file
with open('config.json', 'w') as f:
    json.dump({"api_key": get_credential("key")}, f)

# GOOD: Keep in memory
config = {"api_key": get_credential("key")}
make_api_call(config)  # Use directly, never persist
```

## Per-Project Credential Isolation

### Project Detection

Credentials are isolated per project root:
```bash
# Detect project root
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PROJECT_NAME=$(basename "$PROJECT_ROOT")

# Credentials scoped to project
CREDENTIAL_KEY="claude-code:${PROJECT_NAME}:api-key"
```

### Credential Inheritance

Projects can inherit credentials from parent contexts:
```
~/.claude/credentials/          # Global (all projects)
└── global-github-token

/projects/company/              # Company-wide
└── .claude/credentials/
    └── company-vpn-cert

/projects/company/app1/         # Project-specific
└── .claude/credentials/
    └── app1-api-key
```

Search order: Project → Company → Global

## Implementation Scripts

### Keychain Wrapper Script

See `scripts/keychain/keychain-wrapper.sh` for cross-platform keychain operations:
- Auto-detects platform (macOS, Linux, Windows)
- Provides unified interface: `store()`, `retrieve()`, `delete()`, `list()`
- Handles platform-specific error codes

### Credential Scanner

See `scripts/security/scan-credentials.sh` for pattern-based detection:
- Regex patterns for common credential formats
- Entropy analysis for high-randomness strings
- Context-aware scanning (ignore test fixtures, comments)

### Leak Prevention Hook

See `scripts/security/prevent-leaks.sh` for PreToolUse hook implementation:
- Scans Bash commands before execution
- Checks Write/Edit tool calls for credential patterns
- Provides user warnings with suggested fixes

## Security Best Practices

### DO

✅ **Always use system keychain** - Never plain text files
✅ **Scope credentials to projects** - Prevents cross-project leaks
✅ **Use temporary files with 0600 permissions** - For file-based credentials
✅ **Unset environment variables immediately** - After single-command use
✅ **Implement all three leak prevention layers** - Defense in depth
✅ **Rotate credentials regularly** - Update stored values periodically
✅ **Audit with `/list-credentials`** - Review what's stored

### DON'T

❌ **Never hardcode credentials** - Always use `/store-credential`
❌ **Never commit .env files** - Use .gitignore
❌ **Never log credential values** - Even in debug mode
❌ **Never use global credentials for sensitive projects** - Use project-specific
❌ **Never disable leak prevention** - Keep all three layers active
❌ **Never share credentials across trust boundaries** - Isolate by project
❌ **Never store credentials in plan files** - Plans may be shared

## Credential Lifecycle Management

### Initial Storage
```bash
# Interactive prompt (secure input)
/store-credential --name "api-key" --type "api-key"
# [User types value securely, not echoed]

# From file (for keys)
/store-credential --name "ssh-key" --type "ssh-key" --file ~/.ssh/id_rsa

# From stdin (pipe from secure source)
echo "$SECRET" | /store-credential --name "token" --type "api-key" --stdin
```

### Rotation
```bash
# Update existing credential
/store-credential --name "api-key" --update --value "$NEW_KEY"

# Verify old key is overwritten
/get-credential --name "api-key" --verify-changed
```

### Deletion
```bash
# Remove credential
/store-credential --name "api-key" --delete

# Confirm deletion
/list-credentials  # Should not show "api-key"
```

## Troubleshooting

### Keychain Access Denied

**macOS:**
```bash
# Grant Terminal/Claude Code keychain access
security unlock-keychain ~/Library/Keychains/login.keychain-db
```

**Linux:**
```bash
# Start gnome-keyring daemon
eval $(gnome-keyring-daemon --start)
export $(gnome-keyring-daemon --start)
```

**Windows:**
```powershell
# Run as Administrator if credential manager access fails
Start-Process powershell -Verb RunAs
```

### Credential Not Found

```bash
# List all credentials to verify name
/list-credentials

# Check project scope
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
echo "Current project: $(basename $PROJECT_ROOT)"

# Try global fallback
/get-credential --name "api-key" --global
```

### Leak Prevention False Positives

```bash
# Whitelist test fixtures
# Add to .claude/project-context.local.md:
leak_prevention_ignore:
  - "tests/fixtures/"
  - "examples/"
  - "*_test.py"
```

## Additional Resources

### Reference Files

For detailed implementation patterns:
- **`references/keychain-apis.md`** - Platform-specific API documentation
- **`references/credential-patterns.md`** - Secure usage patterns with code examples
- **`references/leak-detection.md`** - Comprehensive leak detection patterns

### Example Files

Working examples in `examples/`:
- **`keychain-store-retrieve.sh`** - Complete keychain workflow
- **`oauth-refresh.py`** - OAuth token management with refresh
- **`credential-rotation.sh`** - Automated credential rotation

### Utility Scripts

Available in `scripts/`:
- **`keychain/keychain-wrapper.sh`** - Cross-platform keychain interface
- **`security/scan-credentials.sh`** - Pattern-based credential scanner
- **`security/prevent-leaks.sh`** - PreToolUse hook for leak prevention
- **`security/detect-credentials.py`** - Advanced entropy-based detection

## Integration with Other Components

### With Session Management

Credentials are restored on session resume:
```bash
# SessionStart hook loads project credentials
# Available immediately on /resume
```

### With Project Indexing

Index tracks which credentials are needed:
```json
{
  "credentials_required": [
    "github-api",
    "stripe-api-key",
    "aws-access-key"
  ]
}
```

### With Plan Mode

Plans can reference credential names (not values):
```markdown
## Phase 3: API Integration

- [ ] Store Stripe API key: `/store-credential --name "stripe-api"`
- [ ] Configure webhook secret: `/store-credential --name "stripe-webhook"`
```

Always store credentials before starting work phases requiring them.
