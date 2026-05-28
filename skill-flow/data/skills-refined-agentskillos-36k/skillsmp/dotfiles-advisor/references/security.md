# Dotfiles Security

Best practices for keeping sensitive data out of dotfiles repositories.

## Table of Contents

1. [Core Principles](#core-principles)
2. [The .local Pattern](#the-local-pattern)
3. [Git Security](#git-security)
4. [Secret Management](#secret-management)
5. [Checklist](#checklist)

---

## Core Principles

### Never Commit

- API keys and tokens
- Passwords and credentials
- Private SSH keys
- Personal email addresses
- Work-specific paths or domains
- Machine-specific hardware IDs

### Always Separate

- Public config (repository) vs private config (local)
- Work settings vs personal settings
- Machine-specific vs universal settings

---

## The .local Pattern

### Shell Configuration

```bash
# .zshrc - committed to repo
export EDITOR="nvim"
export LANG="en_US.UTF-8"

# Load local overrides (not committed)
[[ -f ~/.zshrc.local ]] && source ~/.zshrc.local
```

```bash
# ~/.zshrc.local - NOT in repo, created manually
export OPENAI_API_KEY="sk-..."
export GITHUB_TOKEN="ghp_..."
export WORK_EMAIL="name@company.com"
```

### Git Configuration

```gitconfig
# ~/.config/git/config - committed
[user]
    name = Your Name
    email = public@example.com

[include]
    path = ~/.config/git/config.local
```

```gitconfig
# ~/.config/git/config.local - NOT in repo
[user]
    email = private@example.com
    signingkey = ~/.ssh/id_ed25519.pub

[credential "https://github.com"]
    helper = store
```

### SSH Configuration

```ssh-config
# ~/.ssh/config - committed (public parts only)
Host github.com
    IdentityFile ~/.ssh/id_ed25519
    AddKeysToAgent yes

Include ~/.ssh/config.local
```

```ssh-config
# ~/.ssh/config.local - NOT in repo
Host work-server
    HostName internal.company.com
    User myusername
    IdentityFile ~/.ssh/work_key
```

---

## Git Security

### .gitignore Essentials

```gitignore
# Credentials
*.local
*.secret
.env
.env.*
!.env.example

# SSH
*.pem
*.key
id_*
!id_*.pub

# GPG
*.gpg
secring.*

# Editor
.idea/
.vscode/settings.json

# OS
.DS_Store
Thumbs.db
```

### Pre-commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for potential secrets
if git diff --cached --name-only | xargs grep -l -E "(api_key|password|secret|token)" 2>/dev/null; then
    echo "ERROR: Potential secret detected in staged files"
    exit 1
fi

# Check for .local files
if git diff --cached --name-only | grep -E "\.local$"; then
    echo "ERROR: .local files should not be committed"
    exit 1
fi
```

### Git-secrets Tool

```bash
# Install
brew install git-secrets

# Initialize in repo
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'PRIVATE_KEY'
git secrets --add --allowed 'PRIVATE_KEY_EXAMPLE'
```

---

## Secret Management

### Environment Variables

```bash
# Use direnv for project-specific secrets
# .envrc (gitignored)
export DATABASE_URL="postgres://..."
export API_KEY="..."

# .envrc.example (committed)
export DATABASE_URL="postgres://user:pass@localhost/db"
export API_KEY="your-api-key-here"
```

### Password Managers Integration

#### 1Password CLI

```bash
# .zshrc.local
export GITHUB_TOKEN=$(op read "op://Personal/GitHub/token")
```

#### Bitwarden CLI

```bash
# .zshrc.local
export API_KEY=$(bw get password "API Key")
```

### chezmoi with Secrets

```toml
# .chezmoi.toml.tmpl
[data]
    email = "{{ promptString "email" }}"

{{ if eq .chezmoi.os "darwin" -}}
[onePassword]
    prompt = false
{{- end }}
```

```bash
# Template using 1Password
{{ onepasswordRead "op://vault/item/field" }}
```

---

## Checklist

### Before First Commit

- [ ] `.gitignore` includes `*.local`, `.env*`, credentials patterns
- [ ] No hardcoded API keys, tokens, or passwords
- [ ] Email addresses are generic or use `.local` override
- [ ] SSH config excludes private host information
- [ ] Work-specific paths use environment variables

### Before Each Commit

- [ ] Run `git diff --cached` to review changes
- [ ] Search for sensitive patterns: `api`, `key`, `token`, `password`, `secret`
- [ ] Verify no `.local` files are staged
- [ ] Check no private paths are exposed

### Setup Automation

```makefile
# makefile
.PHONY: secrets-check

secrets-check:
	@echo "Checking for potential secrets..."
	@git secrets --scan 2>/dev/null || echo "git-secrets not installed"
	@! grep -r -E "(sk-|ghp_|AKIA)" --include="*.sh" --include="*.zsh" .
```

### Recovery Steps

If secrets were accidentally committed:

```bash
# Remove from history (DANGEROUS - rewrites history)
git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch path/to/secret" \
    --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner
bfg --delete-files "*.local"
bfg --replace-text passwords.txt

# Force push (coordinate with team)
git push origin --force --all

# Rotate compromised credentials immediately
```

---

## Quick Reference

| File Type | Pattern | Location |
|-----------|---------|----------|
| Shell secrets | `.zshrc.local` | `~/.zshrc.local` or `$ZDOTDIR/.zshrc.local` |
| Git config | `config.local` | `~/.config/git/config.local` |
| SSH config | `config.local` | `~/.ssh/config.local` |
| Environment | `.envrc` | Project root (gitignored) |
| Editor | `settings.local.json` | Editor config directory |
