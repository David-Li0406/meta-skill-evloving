# Bundle Management Workflow

Guide for creating, signing, sharing, and importing artifact bundles with SkillMeat.

---

## Overview

**Bundle Operations**:
- **Create**: Package artifacts from your collection into shareable `.skillmeat-pack` files
- **Sign**: Add cryptographic signatures for integrity verification
- **Share**: Distribute bundles to colleagues, teams, or public repositories
- **Import**: Install bundles with automatic conflict resolution
- **Inspect**: Examine bundle contents and verify integrity

**Use Cases**:
- Share development setups with team members
- Distribute company standard artifacts
- Create reproducible environments
- Backup and restore collections
- Collaborate on artifact sets

---

## Quick Reference

### Create Bundle

```bash
# Interactive mode (prompts for artifact selection)
skillmeat bundle create my-setup

# Include specific artifacts
skillmeat bundle create my-setup -r pdf -r canvas -r document-editor

# Include all skills
skillmeat bundle create my-setup --type skill

# Include all artifacts
skillmeat bundle create my-setup --all

# With metadata
skillmeat bundle create my-setup \
  -d "My development environment" \
  -a "jane@example.com" \
  --tags "dev,python,web"

# Create and sign
skillmeat bundle create my-setup --sign
```

### Inspect Bundle

```bash
# View bundle metadata
skillmeat bundle inspect bundle.skillmeat-pack

# Verify integrity
skillmeat bundle inspect bundle.skillmeat-pack --verify

# List all files
skillmeat bundle inspect bundle.skillmeat-pack --list-files

# JSON output
skillmeat bundle inspect bundle.skillmeat-pack --json
```

### Import Bundle

```bash
# Interactive import (prompts for conflicts)
skillmeat bundle import colleague-setup.skillmeat-pack

# Preview without changes
skillmeat bundle import colleague-setup.skillmeat-pack --dry-run

# Always merge (overwrite existing)
skillmeat bundle import colleague-setup.skillmeat-pack --strategy=merge

# Fork conflicts (create duplicates)
skillmeat bundle import colleague-setup.skillmeat-pack --strategy=fork

# Skip conflicts (keep existing)
skillmeat bundle import colleague-setup.skillmeat-pack --strategy=skip

# Verify hash
skillmeat bundle import bundle.skillmeat-pack --hash abc123...
```

### Sign and Verify

```bash
# Generate signing key
skillmeat sign generate-key -n "Jane Doe" -e "jane@example.com"

# Create and sign bundle
skillmeat bundle create my-setup --sign

# Verify signature
skillmeat sign verify bundle.skillmeat-pack

# Require signature (fail if unsigned)
skillmeat sign verify bundle.skillmeat-pack --require-signature

# List all keys
skillmeat sign list-keys

# Export public key for sharing
skillmeat sign export-key --key-id abc123

# Import trusted key
skillmeat sign import-key colleague-key.pub
```

---

## Workflow 1: Share Your Development Setup

### Step 1: Generate Signing Key (First Time Only)

```bash
# Create your signing key
skillmeat sign generate-key \
  -n "Jane Doe" \
  -e "jane@example.com"

# Key stored in system keychain
# Output: "Created signing key: abc123def456..."
```

**Output**:
```
✓ Generated Ed25519 key pair
✓ Stored in system keychain
  Key ID: abc123def456
  Name:   Jane Doe
  Email:  jane@example.com

Export your public key to share with others:
  skillmeat sign export-key --key-id abc123def456
```

### Step 2: Create Bundle

```bash
# Create bundle with specific artifacts
skillmeat bundle create dev-setup \
  -r pdf \
  -r canvas \
  -r document-editor \
  -d "My web development environment" \
  -a "jane@example.com" \
  --tags "web,dev,python" \
  --sign
```

**Interactive Mode**:
```
Creating bundle: dev-setup

Select artifacts to include:
  [x] pdf (skill)
  [x] canvas (skill)
  [x] document-editor (skill)
  [ ] old-script (command)

Description: My web development environment
Author: jane@example.com
Tags: web,dev,python
Sign bundle? [Y/n]: y

✓ Packed 3 artifacts
✓ Signed with key abc123def456
✓ Created: dev-setup.skillmeat-pack (2.4 MB)
```

### Step 3: Share Bundle

**Email**:
- Attach `dev-setup.skillmeat-pack`
- Include SHA-256 hash for verification

**File Sharing**:
```bash
# Upload to shared drive
cp dev-setup.skillmeat-pack /mnt/team-drive/bundles/

# Or use Git LFS
git lfs track "*.skillmeat-pack"
git add dev-setup.skillmeat-pack
git commit -m "Add dev setup bundle"
```

**Public Key Distribution**:
```bash
# Export your public key
skillmeat sign export-key --key-id abc123def456 > jane-public.key

# Share with team (one time)
# Recipients run: skillmeat sign import-key jane-public.key
```

---

## Workflow 2: Import Colleague's Bundle

### Step 1: Receive Bundle

Download or receive bundle file: `colleague-setup.skillmeat-pack`

Optional: Receive SHA-256 hash out-of-band (for verification)

### Step 2: Inspect Bundle

```bash
# View contents
skillmeat bundle inspect colleague-setup.skillmeat-pack

# Verify integrity
skillmeat bundle inspect colleague-setup.skillmeat-pack --verify
```

**Output**:
```
Bundle: colleague-setup
Version: 1.0.0
Author: john@example.com
Created: 2025-12-24T10:30:00Z
Description: Backend development tools

Artifacts (5):
  - pdf (skill) - v1.2.0
  - api-client (skill) - v2.0.1
  - db-migrate (command) - v1.5.0
  - code-review (agent) - v1.0.0
  - testing-suite (skill) - v3.1.0

Signature: ✓ Verified (key: def456abc789)
Total size: 3.2 MB
```

### Step 3: Verify Signature (If Signed)

```bash
# Import colleague's public key (one time)
skillmeat sign import-key john-public.key

# Verify signature
skillmeat sign verify colleague-setup.skillmeat-pack
```

**Output**:
```
✓ Signature valid
  Signed by: john@example.com (def456abc789)
  Signed at: 2025-12-24T10:30:00Z
  Bundle integrity verified
```

### Step 4: Dry Run Import

```bash
# Preview what will happen
skillmeat bundle import colleague-setup.skillmeat-pack --dry-run
```

**Output**:
```
Import Preview: colleague-setup.skillmeat-pack

Would add (3):
  + api-client (skill) - new artifact
  + db-migrate (command) - new artifact
  + testing-suite (skill) - new artifact

Would update (1):
  ~ pdf (skill) - v1.0.0 → v1.2.0

Would skip (1):
  = code-review (agent) - identical to existing

Conflicts (0): none

Strategy: interactive (will prompt for conflicts)
```

### Step 5: Import Bundle

**Interactive (Recommended)**:
```bash
skillmeat bundle import colleague-setup.skillmeat-pack
```

**Prompts**:
```
Artifact 'pdf' already exists:
  Existing: v1.0.0 (source: anthropics/skills/pdf)
  Imported: v1.2.0 (source: anthropics/skills/pdf)

Actions:
  [m] Merge (replace with imported version)
  [f] Fork (keep both, rename imported)
  [s] Skip (keep existing, don't import)
  [d] Diff (compare versions)
  [q] Quit import

Choice [m/f/s/d/q]: m

✓ Replaced pdf with v1.2.0
```

**Non-Interactive**:
```bash
# Always merge (overwrite)
skillmeat bundle import colleague-setup.skillmeat-pack --strategy=merge

# Fork conflicts (create duplicates)
skillmeat bundle import colleague-setup.skillmeat-pack --strategy=fork

# Skip conflicts (keep existing)
skillmeat bundle import colleague-setup.skillmeat-pack --strategy=skip
```

**Final Output**:
```
✓ Import complete

Added (3):
  + api-client (skill)
  + db-migrate (command)
  + testing-suite (skill)

Updated (1):
  ~ pdf (skill) - v1.0.0 → v1.2.0

Skipped (1):
  = code-review (agent)

Total: 4 artifacts imported, 1 skipped
```

---

## Workflow 3: Team Standard Distribution

### Scenario
Your team needs a standard set of artifacts for all developers.

### Step 1: Create Team Signing Key

**Key Administrator**:
```bash
# Generate team key
skillmeat sign generate-key \
  -n "Acme Corp Engineering" \
  -e "engineering@acme.com"

# Export public key
skillmeat sign export-key --key-id team123 > acme-eng-public.key

# Distribute public key to all team members
# (via docs, wiki, onboarding repo)
```

**Team Members**:
```bash
# Import team public key (one time)
skillmeat sign import-key acme-eng-public.key
```

### Step 2: Create Standard Bundle

**Key Administrator or Build System**:
```bash
# Create bundle with all required artifacts
skillmeat bundle create acme-standard \
  --type skill \
  --type command \
  -d "Acme Corp standard development environment" \
  -a "engineering@acme.com" \
  -v "2024.12.1" \
  --tags "standard,required,onboarding" \
  --sign \
  --signing-key-id team123
```

### Step 3: Distribute Bundle

**Options**:
1. **Internal Package Registry**: Upload to artifact repository
2. **Git Repository**: Store in onboarding repo with Git LFS
3. **Cloud Storage**: S3, Google Drive, Dropbox with access controls
4. **Wiki/Docs**: Link from onboarding documentation

**Example (Git)**:
```bash
cd company-onboarding-repo
git lfs track "*.skillmeat-pack"
cp acme-standard.skillmeat-pack bundles/
git add bundles/acme-standard.skillmeat-pack
git commit -m "Update standard bundle to v2024.12.1"
git push
```

### Step 4: New Developer Onboarding

**New Team Member**:
```bash
# Clone onboarding repo
git clone https://github.com/acme/onboarding.git
cd onboarding

# Import team public key
skillmeat sign import-key keys/acme-eng-public.key

# Verify and import bundle
skillmeat sign verify bundles/acme-standard.skillmeat-pack
skillmeat bundle import bundles/acme-standard.skillmeat-pack --strategy=merge

# Deploy all artifacts to current project
skillmeat deploy --all
```

**Automation (Shell Script)**:
```bash
#!/bin/bash
# setup-dev-env.sh

echo "Setting up Acme development environment..."

# Import team key
skillmeat sign import-key keys/acme-eng-public.key

# Verify bundle
if ! skillmeat sign verify bundles/acme-standard.skillmeat-pack; then
  echo "Error: Bundle signature verification failed"
  exit 1
fi

# Import bundle (merge strategy)
skillmeat bundle import bundles/acme-standard.skillmeat-pack --strategy=merge

# Deploy to current project
skillmeat deploy --all

echo "✓ Development environment ready"
```

---

## Bundle Format Reference

### Bundle File Structure

`.skillmeat-pack` files are ZIP archives with standardized structure:

```
bundle.skillmeat-pack (ZIP)
├── manifest.toml          # Bundle metadata
├── signature.json         # Ed25519 signature (if signed)
├── artifacts/
│   ├── pdf/
│   │   ├── SKILL.md
│   │   ├── metadata.toml
│   │   └── scripts/
│   ├── canvas/
│   │   ├── SKILL.md
│   │   └── templates/
│   └── ...
└── checksums.sha256       # File integrity hashes
```

### manifest.toml

```toml
[bundle]
name = "my-setup"
version = "1.0.0"
created_at = "2025-12-24T12:00:00Z"
author = "jane@example.com"
description = "My development setup"
license = "MIT"
tags = ["dev", "python", "web"]

# Optional: Bundle dependencies
[dependencies]
skillmeat_version = ">=0.3.0"
python_version = ">=3.9"

# Artifacts included in bundle
[[artifacts]]
name = "pdf"
type = "skill"
source = "anthropics/skills/pdf"
version = "v1.2.0"
resolved_sha = "abc123def456..."
added_at = "2025-12-24T11:00:00Z"

[[artifacts]]
name = "canvas"
type = "skill"
source = "anthropics/skills/canvas-design"
version = "latest"
resolved_sha = "def456abc789..."
added_at = "2025-12-24T11:30:00Z"

[[artifacts]]
name = "api-client"
type = "command"
source = "myorg/commands/api-client"
version = "v2.0.1"
resolved_sha = "789abc123def..."
added_at = "2025-12-24T12:00:00Z"

# Optional: Deployment recommendations
[deployment]
recommended_scope = "user"  # or "local"
auto_deploy = false
```

### signature.json

```json
{
  "algorithm": "Ed25519",
  "key_id": "abc123def456",
  "signer": {
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "signed_at": "2025-12-24T12:00:00Z",
  "signature": "base64-encoded-signature-here...",
  "manifest_hash": "sha256-of-manifest-toml"
}
```

### checksums.sha256

```
abc123...  artifacts/pdf/SKILL.md
def456...  artifacts/pdf/scripts/process.js
789abc...  artifacts/canvas/SKILL.md
...
```

---

## Conflict Resolution Strategies

### Strategy: Interactive (Default)

**Behavior**: Prompt for each conflict

**When to Use**:
- First time importing from new source
- Reviewing colleague's changes
- Uncertain about impact

**Example**:
```bash
skillmeat bundle import bundle.skillmeat-pack
# or
skillmeat bundle import bundle.skillmeat-pack --strategy=interactive
```

**Prompts**:
```
Conflict: artifact 'pdf' already exists

Existing:
  Version: v1.0.0
  Source:  anthropics/skills/pdf
  SHA:     abc123...

Imported:
  Version: v1.2.0
  Source:  anthropics/skills/pdf
  SHA:     def456...

Actions:
  [m] Merge - Replace with imported version
  [f] Fork  - Keep both (rename imported to 'pdf-imported')
  [s] Skip  - Keep existing, don't import
  [d] Diff  - Show differences
  [q] Quit  - Cancel import

Choice [m/f/s/d/q]:
```

### Strategy: Merge

**Behavior**: Always overwrite existing artifacts with imported versions

**When to Use**:
- Importing trusted updates
- Team standard bundles
- Known-good configurations

**Example**:
```bash
skillmeat bundle import bundle.skillmeat-pack --strategy=merge
```

**Output**:
```
Importing with merge strategy (overwrite existing)...

✓ Replaced pdf (v1.0.0 → v1.2.0)
✓ Replaced canvas (v2.0.0 → v2.1.0)
+ Added api-client (v1.0.0)

Total: 2 updated, 1 added
```

### Strategy: Fork

**Behavior**: Keep existing artifacts, create duplicates with suffix

**When to Use**:
- Trying experimental versions
- Comparing two versions side-by-side
- Testing without losing current setup

**Example**:
```bash
skillmeat bundle import bundle.skillmeat-pack --strategy=fork
```

**Output**:
```
Importing with fork strategy (create duplicates)...

= Kept pdf (existing)
+ Added pdf-imported (v1.2.0)
= Kept canvas (existing)
+ Added canvas-imported (v2.1.0)
+ Added api-client (v1.0.0)

Total: 2 forked, 1 added
```

**Result**:
```bash
skillmeat list
# Output:
# pdf (skill) - v1.0.0
# pdf-imported (skill) - v1.2.0
# canvas (skill) - v2.0.0
# canvas-imported (skill) - v2.1.0
# api-client (command) - v1.0.0
```

### Strategy: Skip

**Behavior**: Keep existing artifacts, don't import conflicts

**When to Use**:
- Selectively importing new artifacts only
- Preserving local modifications
- Conservative updates

**Example**:
```bash
skillmeat bundle import bundle.skillmeat-pack --strategy=skip
```

**Output**:
```
Importing with skip strategy (keep existing)...

= Skipped pdf (keeping existing v1.0.0)
= Skipped canvas (keeping existing v2.0.0)
+ Added api-client (v1.0.0)

Total: 2 skipped, 1 added
```

---

## Security Best Practices

### 1. Always Verify Signatures

**Before Importing**:
```bash
# Inspect bundle
skillmeat bundle inspect bundle.skillmeat-pack

# Verify signature
skillmeat sign verify bundle.skillmeat-pack

# Import only if verified
if skillmeat sign verify bundle.skillmeat-pack; then
  skillmeat bundle import bundle.skillmeat-pack
else
  echo "Error: Signature verification failed"
  exit 1
fi
```

### 2. Use Dry Run First

**Preview Before Committing**:
```bash
# See what would happen
skillmeat bundle import bundle.skillmeat-pack --dry-run

# Review output carefully

# Import if satisfied
skillmeat bundle import bundle.skillmeat-pack --strategy=merge
```

### 3. Verify Bundle Hash

**Out-of-Band Hash Verification**:
```bash
# Sender provides hash
sha256sum my-bundle.skillmeat-pack
# Output: abc123def456...

# Recipient verifies
skillmeat bundle import bundle.skillmeat-pack --hash abc123def456...
```

### 4. Trust Key Management

**Import Trusted Keys**:
```bash
# Only import keys from trusted sources
skillmeat sign import-key colleague-public.key

# List trusted keys
skillmeat sign list-keys

# Revoke compromised keys
skillmeat sign revoke --key-id abc123
```

### 5. Review Bundle Contents

**Inspect Before Import**:
```bash
# View artifacts
skillmeat bundle inspect bundle.skillmeat-pack

# List all files
skillmeat bundle inspect bundle.skillmeat-pack --list-files

# Check for suspicious sources
# - Unknown GitHub orgs
# - Unusual file paths
# - Excessive file sizes
```

### 6. Use Require-Signature Flag

**Enforce Signature Requirement**:
```bash
# Fail if bundle is unsigned
skillmeat sign verify bundle.skillmeat-pack --require-signature

# In automated scripts
if ! skillmeat sign verify bundle.skillmeat-pack --require-signature; then
  echo "Error: Bundle must be signed"
  exit 1
fi
```

---

## Advanced Patterns

### Pattern 1: Multi-Environment Bundles

**Scenario**: Different bundles for dev, staging, production

```bash
# Create environment-specific bundles
skillmeat bundle create dev-env \
  --type skill \
  -d "Development environment" \
  --tags "dev,local" \
  --sign

skillmeat bundle create prod-env \
  -r pdf \
  -r api-client \
  -d "Production environment" \
  --tags "prod,minimal" \
  --sign
```

**Import Based on Environment**:
```bash
# In development
skillmeat bundle import dev-env.skillmeat-pack --strategy=merge

# In production
skillmeat bundle import prod-env.skillmeat-pack --strategy=merge
```

### Pattern 2: Incremental Updates

**Scenario**: Regular updates to team standard

```bash
# Create versioned bundles
skillmeat bundle create acme-standard \
  --all \
  -v "2024.12.1" \
  --sign

# Next month
skillmeat bundle create acme-standard \
  --all \
  -v "2025.01.1" \
  --sign

# Team members import latest
skillmeat bundle import acme-standard-2025.01.1.skillmeat-pack --strategy=merge
```

### Pattern 3: Backup and Restore

**Backup**:
```bash
# Create full collection backup
skillmeat bundle create backup-$(date +%Y%m%d) \
  --all \
  -d "Full collection backup" \
  -a "$(git config user.email)" \
  --sign

# Store securely (encrypted drive, cloud backup)
```

**Restore**:
```bash
# On new machine or after data loss
skillmeat init
skillmeat bundle import backup-20251224.skillmeat-pack --strategy=merge
skillmeat deploy --all
```

### Pattern 4: Artifact Curation

**Scenario**: Share curated collections

```bash
# Python development bundle
skillmeat bundle create python-dev \
  -r pytest-helpers \
  -r lint-config \
  -r type-checker \
  -d "Python development tools" \
  --tags "python,dev" \
  --sign

# Web development bundle
skillmeat bundle create web-dev \
  -r react-snippets \
  -r api-client \
  -r browser-tools \
  -d "Web development tools" \
  --tags "web,frontend" \
  --sign
```

### Pattern 5: CI/CD Integration

**Automated Bundle Creation**:
```yaml
# .github/workflows/create-bundle.yml
name: Create Bundle
on:
  release:
    types: [published]

jobs:
  bundle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install SkillMeat
        run: pip install skillmeat
      - name: Create Bundle
        run: |
          skillmeat bundle create team-standard \
            --all \
            -v "${{ github.event.release.tag_name }}" \
            --sign \
            --signing-key-id "${{ secrets.SIGNING_KEY_ID }}"
      - name: Upload Bundle
        uses: actions/upload-release-asset@v1
        with:
          asset_path: team-standard.skillmeat-pack
          asset_name: team-standard-${{ github.event.release.tag_name }}.skillmeat-pack
```

**Automated Import**:
```bash
#!/bin/bash
# download-latest-bundle.sh

BUNDLE_URL="https://github.com/acme/bundles/releases/latest/download/team-standard.skillmeat-pack"

curl -L -o team-standard.skillmeat-pack "$BUNDLE_URL"
skillmeat sign verify team-standard.skillmeat-pack --require-signature
skillmeat bundle import team-standard.skillmeat-pack --strategy=merge
```

---

## Troubleshooting

### Bundle Creation Fails

**Error**: "No artifacts found in collection"
```bash
# Check collection
skillmeat list

# Add artifacts first
skillmeat add anthropics/skills/pdf
```

**Error**: "Signing key not found"
```bash
# Generate key
skillmeat sign generate-key -n "Your Name" -e "you@example.com"

# Or specify key ID
skillmeat bundle create my-bundle --sign --signing-key-id abc123
```

### Bundle Import Fails

**Error**: "Hash verification failed"
```bash
# Re-download bundle
# Check for corruption

# Verify manually
sha256sum bundle.skillmeat-pack

# Compare with expected hash
```

**Error**: "Signature verification failed"
```bash
# Import signer's public key
skillmeat sign import-key colleague-public.key

# Try verification again
skillmeat sign verify bundle.skillmeat-pack
```

**Error**: "Bundle is corrupt or invalid"
```bash
# Check bundle integrity
skillmeat bundle inspect bundle.skillmeat-pack --verify

# Try re-downloading
```

### Key Management Issues

**Error**: "Signing key not accessible"
```bash
# Check system keychain permissions
# macOS: Keychain Access app
# Linux: Check secret service
# Windows: Credential Manager

# Regenerate key if needed
skillmeat sign generate-key -n "Your Name" -e "you@example.com"
```

**Error**: "Key ID not found"
```bash
# List available keys
skillmeat sign list-keys

# Use correct key ID
skillmeat bundle create my-bundle --sign --signing-key-id <correct-id>
```

---

## Reference

### Bundle Commands

```bash
# Create
skillmeat bundle create <name> [options]

# Inspect
skillmeat bundle inspect <file> [--verify] [--list-files] [--json]

# Import
skillmeat bundle import <file> [--strategy=<strategy>] [--dry-run] [--hash=<hash>]
```

### Sign Commands

```bash
# Generate key
skillmeat sign generate-key -n <name> -e <email>

# Verify
skillmeat sign verify <bundle> [--require-signature]

# List keys
skillmeat sign list-keys

# Export key
skillmeat sign export-key --key-id <id>

# Import key
skillmeat sign import-key <file>

# Revoke key
skillmeat sign revoke --key-id <id>
```

### Conflict Strategies

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `interactive` | Prompt for each conflict | First import, review needed |
| `merge` | Overwrite existing | Trusted updates, team standard |
| `fork` | Keep both, rename imported | Experimental, comparison |
| `skip` | Keep existing, don't import | Selective import, conservative |

### File Extensions

| Extension | Description |
|-----------|-------------|
| `.skillmeat-pack` | Bundle archive (ZIP) |
| `.pub` | Public key (PEM format) |
| `.key` | Private key (PEM, encrypted) |

---

## Best Practices Summary

1. **Always sign bundles** for team distribution
2. **Verify signatures** before importing
3. **Use dry run** to preview imports
4. **Document bundle contents** in description
5. **Version bundles** semantically (YYYY.MM.patch)
6. **Tag bundles** for discoverability
7. **Distribute public keys** securely (docs, wiki)
8. **Review bundle contents** before importing
9. **Use merge strategy** for trusted sources only
10. **Backup collections** regularly with bundles
