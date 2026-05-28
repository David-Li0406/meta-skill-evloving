**Skill**: [semantic-release](../SKILL.md)

# Troubleshooting

Consolidated troubleshooting guide for all semantic-release issues.

---

## Authentication Issues

### No GitHub Token Specified

**Symptom**: Error "No GitHub token specified" from semantic-release

**Cause**: `GITHUB_TOKEN` not set or gh CLI not authenticated

**Resolution**:

```bash
# 1. Check gh CLI authentication
gh auth status

# 2. If not authenticated, use web browser
gh auth login
# Select: GitHub.com → HTTPS → Login with browser

# 3. Verify token retrieval works
gh auth token
```

**Note**: This error is NOT a recommendation to create manual tokens. gh CLI handles everything via web authentication.

### Permission Denied (publickey)

**Symptom**: SSH fails with "Permission denied (publickey)"

**Resolution**:

```bash
# 1. Test SSH
ssh -T git@github.com

# 2. Check SSH config
cat ~/.ssh/config | grep -A 5 "github.com"

# 3. Verify key exists
ls -la ~/.ssh/id_ed25519*

# 4. Check key is loaded
ssh-add -l

# 5. Add key to ssh-agent if needed
ssh-add ~/.ssh/id_ed25519_yourkey
```

### GitHub Account Mismatch

**Symptom**: Error "GitHub account mismatch" or release publishes under wrong account

**Cause**: gh CLI is authenticated with different account than expected for this repository

**Resolution**:

```bash
# Check current account
gh api user --jq '.login'

# Switch to correct account
gh auth switch --user <expected-username>
```

**Prevention**: Set `GH_ACCOUNT` in your directory's `.mise.toml`:

```toml
[env]
GH_ACCOUNT = "terrylica"  # Expected account for this directory
GH_TOKEN = "{{ read_file(path=env.HOME ~ '/.claude/.secrets/gh-token-terrylica') | trim }}"
```

### GitHub Token Missing 'workflow' Scope

**Symptom**: Error "GitHub token missing 'workflow' scope" or "Failed to create release"

**Cause**: GitHub CLI token lacks `workflow` scope

**Resolution**:

```bash
# Add workflow scope to existing authentication
gh auth refresh -s workflow

# Verify
gh api -i user 2>&1 | grep -i "x-oauth-scopes"
# Should include: workflow
```

---

## SSH ControlMaster Cache

For multi-account GitHub setups, SSH ControlMaster can cache connections with stale authentication.

### Symptoms

- `ssh -T git@github.com` shows correct account
- `gh auth status` shows correct account
- Git operations still fail with "Repository not found"

### Detection

```bash
# Compare these outputs:
ssh -o ControlMaster=no -T git@github.com  # Fresh connection
ssh -T git@github.com                       # Cached connection
# If different → stale cache
```

### Resolution

```bash
# Kill cached connection
ssh -O exit git@github.com 2>/dev/null || pkill -f 'ssh.*github.com'
# Or:
rm -f ~/.ssh/control-git@github.com:22
```

### Prevention

```sshconfig
# ~/.ssh/config - Disable ControlMaster for GitHub
Host github.com
    ControlMaster no
```

---

## Release Workflow Errors

### No Release Created

**Symptom**: Command succeeds but no git tag or release created

**Diagnosis**:

- Check commit messages follow Conventional Commits format
- Verify commits since last release contain `feat:` or `fix:` types
- Confirm branch name matches configuration (default: `main`)

**Check**:

```bash
/usr/bin/env bash << 'GIT_EOF'
git log $(git describe --tags --abbrev=0)..HEAD --oneline
GIT_EOF
```

Only these trigger releases:

| Commit Type                    | Release                        |
| ------------------------------ | ------------------------------ |
| `feat:`                        | minor                          |
| `fix:`                         | patch                          |
| `BREAKING CHANGE:` or `feat!:` | major                          |
| `docs:`, `chore:`, etc.        | no release (unless configured) |

### Repository Not Found (Valid URL)

**Cause**: gh CLI authenticated with wrong account (common in multi-account setups)

**Resolution**:

1. `gh api user --jq '.login'` - check active account
2. `gh auth switch --user <correct-account>` - switch if needed
3. If account not logged in: `gh auth login` for that account

### Permission Denied Errors

**Symptom**: GitHub Actions fails with "Resource not accessible by integration"

**Resolution**: Repository Settings → Actions → General → Workflow permissions → Enable "Read and write permissions"

### Stale Ahead/Behind Indicators

**Symptom**: After release, prompt shows `↑:N` but actually in sync

**Cause**: Local tracking refs not updated after API push

**Resolution**:

```bash
git fetch origin main:refs/remotes/origin/main --no-tags
```

**Prevention**: Always run Phase 4 (Postflight), or use `npm run release` which runs `postrelease` automatically.

---

## Git Push Failures

### Git Push Works But Release Fails

**Cause**: SSH works (git operations) but gh CLI authentication missing

**Resolution**:

```bash
# SSH is working (Priority 1 ✅)
# Need GitHub API auth (Priority 2)

# Authenticate via web browser
gh auth login
# Select: GitHub.com → HTTPS → Login with browser

# Verify authentication
gh auth status
```

---

## Common Pitfalls

### Dirty Working Directory

**Symptom**: After release, `git status` shows version files as modified with OLD versions

**Cause**: Files were staged before release started. semantic-release commits from working copy, but git index cache may show stale state.

**Prevention**: Always clear git cache before checking status:

```bash
# Step 1: Refresh git index (automatic in npm run release)
git update-index --refresh -q || true

# Step 2: Check for uncommitted changes
git status --porcelain
# Should output nothing

# If dirty, either:
git stash           # Stash changes
git commit -m "..."  # Commit changes
git checkout -- .   # Discard changes
```

**Recovery**: If you see stale versions after release:

```bash
git update-index --refresh
git status  # Should now show clean
```

### Pre-Release Checklist

Before running `npm run release`:

1. ✅ All changes committed
2. ✅ No staged files (`git diff --cached` is empty)
3. ✅ No untracked files in version-synced paths
4. ✅ Branch is up-to-date with remote

### Accidental MAJOR Version Bump

**Symptom**: Released X.0.0 when intended MINOR/PATCH

**Cause**: Commit message contained `!` suffix or `BREAKING CHANGE:` footer unintentionally

**Prevention**:

1. Claude Code: Multi-perspective subagents analyze before proceeding
2. Shell: `read -p` confirmation prompt in release function
3. Review: `npm run release:dry` always shows planned version bump

**Recovery** (if already released):

```bash
# Option 1: Release follow-up patch (preferred - preserves history)
git commit --allow-empty -m "fix: correct version sequence after accidental MAJOR"
npm run release

# Option 2: Delete and re-release (destructive - not recommended)
# Only if no consumers have updated yet
gh release delete vX.0.0 --yes
git push --delete origin vX.0.0
git tag -d vX.0.0
# Amend commit to remove BREAKING CHANGE, then re-release
```

---

## macOS Gatekeeper Blocks .node Files

**Symptom**: macOS shows dialog "Apple could not verify .node is free of malware" when running `npx semantic-release`. Multiple dialogs appear for different `.node` files.

**Cause**: macOS Gatekeeper quarantines unsigned native Node.js modules downloaded via npm/npx. Each `npx` invocation re-downloads packages, triggering new quarantine flags.

**Root cause**: Native `.node` modules (compiled C++ addons) are not code-signed by npm package authors. macOS Sequoia and later are stricter about unsigned binaries.

### Solution (Recommended): Install globally

```bash
/usr/bin/env bash << 'SETUP_EOF'
# One-time setup: Install semantic-release globally
npm install -g semantic-release @semantic-release/changelog @semantic-release/git @semantic-release/github @semantic-release/exec

# Clear quarantine from global node_modules (one-time after install or node upgrade)
xattr -r -d com.apple.quarantine ~/.local/share/mise/installs/node/

# Use semantic-release directly (not npx)
/usr/bin/env bash -c 'GITHUB_TOKEN=$(gh auth token) semantic-release --no-ci'
SETUP_EOF
```

**Why this works**: Global install downloads packages once. Clearing quarantine once is sufficient until Node.js is upgraded.

### Alternative: Clear quarantine from npm cache

If you must use `npx`, clear quarantine from npm cache locations:

```bash
xattr -r -d com.apple.quarantine ~/.npm/
xattr -r -d com.apple.quarantine ~/.local/share/mise/installs/node/
```

### For project-local installs

Add postinstall script to `package.json`:

```json
{
  "scripts": {
    "postinstall": "xattr -r -d com.apple.quarantine ./node_modules 2>/dev/null || true"
  }
}
```

---

## Node.js Compatibility

### Node.js Version Mismatch

**Symptom**: Installation fails with "engine node is incompatible"

**Cause**: Node.js version below 24.10.0

**Resolution**:

```bash
# Install Node.js 24 LTS (using mise)
mise install node@24
mise use node@24
```

Update `.github/workflows/release.yml`:

```yaml
- uses: actions/setup-node@v6
  with:
    node-version: "24"
    cache: "npm"
```

---

## @semantic-release/exec Lodash Template Conflicts

The `@semantic-release/exec` plugin uses [Lodash templates](https://lodash.com/docs/#template) to interpolate variables. **This conflicts with bash variable syntax** because both use `${...}` delimiters.

### Symptom

```
SyntaxError: Unexpected token ':'
    at Function (<anonymous>)
    at lodash.js:14942:16
```

Or: `undefined reference` errors for bash variables that look like template variables.

### Cause

Lodash interprets ALL `${...}` patterns, including bash constructs:

| Pattern                      | Intended For       | Lodash Sees                            |
| ---------------------------- | ------------------ | -------------------------------------- |
| `${nextRelease.version}`     | Lodash template    | ✅ Correct                             |
| `${QUARTO_PUB_AUTH_TOKEN:-}` | Bash default value | ❌ Tries to parse `:-` as JS           |
| `${VAR}`                     | Bash variable      | ❌ Looks for `VAR` in template context |

The colon in bash default syntax (`${VAR:-default}`) causes "Unexpected token ':'" because Lodash tries to parse it as JavaScript.

### Solution 1: Use ERB-Style for Lodash Variables

Use `<%= %>` syntax instead of `${}` for semantic-release variables:

```yaml
# WRONG - conflicts with bash
- - "@semantic-release/exec"
  - successCmd: "echo 'Released ${nextRelease.version}'"

# CORRECT - ERB-style for lodash, $ for bash
- - "@semantic-release/exec"
  - successCmd: "echo 'Released <%= nextRelease.version %>'"
```

### Solution 2: Remove Bash Default Syntax

If you have bash variables with defaults, simplify them:

```yaml
# WRONG - :- causes lodash parse error
successCmd: |
  if [ -z "${TOKEN:-}" ]; then
    echo "No token"
  fi

# CORRECT - remove default syntax
successCmd: |
  if [ -z "$TOKEN" ]; then
    echo "No token"
  fi
```

### Solution 3: Wrap in External Script

For complex bash, move logic to a script file:

```yaml
# .releaserc.yml
- - "@semantic-release/exec"
  - successCmd: "./scripts/post-release.sh <%= nextRelease.version %>"
```

```bash
# scripts/post-release.sh
#!/usr/bin/env bash
set -euo pipefail
VERSION="$1"
# Now you can use any bash syntax freely
if [ -z "${TOKEN:-}" ]; then
  echo "Warning: No token set"
fi
echo "Released $VERSION"
```

### Available Lodash Template Variables

| Variable                     | Description                 |
| ---------------------------- | --------------------------- |
| `<%= nextRelease.version %>` | New version (e.g., `X.Y.Z`) |
| `<%= nextRelease.gitTag %>`  | Git tag (e.g., `vX.Y.Z`)    |
| `<%= nextRelease.notes %>`   | Release notes               |
| `<%= lastRelease.version %>` | Previous version            |
| `<%= lastRelease.gitTag %>`  | Previous git tag            |
| `<%= branch.name %>`         | Current branch              |

### Quick Reference

| Context                   | Use This                     |
| ------------------------- | ---------------------------- |
| semantic-release variable | `<%= nextRelease.version %>` |
| Bash variable             | `$VAR` or `"$VAR"`           |
| Bash with default         | Move to external script      |
| Bash subshell             | `$(command)` is safe         |

---

## Migration Issues (v24 → v25)

Projects initialized before v7.10 lack automatic push. Add manually:

### Add successCmd to `.releaserc.yml`

After @semantic-release/git entry:

```yaml
- - "@semantic-release/exec"
  - successCmd: "/usr/bin/env bash -c 'git push --follow-tags origin main'"
```

### Add postrelease to `package.json`

```bash
npm pkg set scripts.postrelease="git fetch origin main:refs/remotes/origin/main --no-tags || true"
```

---

## References

- [Der Flounder - Clearing quarantine attribute](https://derflounder.wordpress.com/2012/11/20/clearing-the-quarantine-extended-attribute-from-downloaded-applications/)
- [Homebrew/brew#17979 - xattr quarantine on Apple Silicon](https://github.com/Homebrew/brew/issues/17979)
