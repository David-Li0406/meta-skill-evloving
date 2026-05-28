---
name: update-claude-code
description: Use when updating the claude-code nix package to a new version in this dotfiles repo
---

# Update Claude Code

Update `packages/claude-code/package.nix` to a new version.

## Process

### 1. Get Source Hash

```bash
nix-prefetch-url --unpack "https://registry.npmjs.org/@anthropic-ai/claude-code/-/claude-code-${VERSION}.tgz"
```

Convert to SRI format:
```bash
nix hash convert --hash-algo sha256 --to sri <HASH_FROM_ABOVE>
```

### 2. Generate package-lock.json

The npm tarball doesn't include package-lock.json. Generate it:

```bash
cd /tmp && rm -rf claude-code-update && mkdir claude-code-update && cd claude-code-update
curl -sL "https://registry.npmjs.org/@anthropic-ai/claude-code/-/claude-code-${VERSION}.tgz" | tar -xzf - --strip-components=1
AUTHORIZED=1 npm install --package-lock-only
```

Copy to repo:
```bash
cp /tmp/claude-code-update/package-lock.json ~/dotfiles/packages/claude-code/package-lock.json
```

### 3. Update package.nix

Edit `packages/claude-code/package.nix`:
- `version` → new version
- `src.hash` → SRI hash from step 1
- `npmDepsHash` → placeholder: `sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=`

### 4. Get npmDepsHash

User must build the flake. Build will fail with correct hash in error message.

Update `npmDepsHash` with the hash from the error, rebuild.

## Key Gotchas

- `AUTHORIZED=1` required for npm scripts (prepare hook checks this)
- Cannot build flake remotely - user must run build locally
- Three hashes to update: version, src.hash, npmDepsHash
