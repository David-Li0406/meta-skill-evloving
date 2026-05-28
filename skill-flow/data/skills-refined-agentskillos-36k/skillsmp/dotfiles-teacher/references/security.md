# Security Best Practices

## Table of Contents

1. [The .local Pattern](#the-local-pattern)
2. [Gitignore Configuration](#gitignore-configuration)
3. [Template Files](#template-files)
4. [Secret Detection](#secret-detection)

## The .local Pattern

Separate public and private configuration:

```
config/git/
├── config              # Public settings (committed)
├── config.local.template   # Template for private settings (committed)
└── ~/.config/git/config.local  # Actual private settings (NOT committed)
```

### Implementation

**Main config includes local:**
```gitconfig
# config/git/config
[include]
    path = config.local
```

**Template provides structure:**
```gitconfig
# config/git/config.local.template
[user]
    name = Your Name
    email = your@email.com

[github]
    user = your-username
```

**link.sh creates local from template:**
```bash
if [[ ! -f "$XDG_CONFIG_HOME/git/config.local" ]] && \
   [[ -f "$DOTFILES_DIR/config/git/config.local.template" ]]; then
    cp "$DOTFILES_DIR/config/git/config.local.template" \
       "$XDG_CONFIG_HOME/git/config.local"
    warning "Please edit ~/.config/git/config.local with your settings"
fi
```

## Gitignore Configuration

### Repository .gitignore

```gitignore
# Local configuration files (contain secrets)
*.local
*.local.*
!*.local.template

# Environment files
.env
.env.*
!.env.example

# API keys and tokens
**/secrets/
*.pem
*.key
```

### Global .gitignore

Consider adding to `~/.config/git/ignore`:

```gitignore
# OS files
.DS_Store
Thumbs.db

# Editor files
*.swp
*~
.idea/
.vscode/
```

## Template Files

### Naming Convention

| File Type | Example |
|-----------|---------|
| Template | `config.local.template` |
| Actual | `config.local` (created at setup) |
| Example | `.env.example` |

### Template Content Guidelines

1. Include all required keys with placeholder values
2. Add comments explaining each setting
3. Use obvious placeholder values:

```bash
# .zshrc.local.template
# Personal aliases and settings

# API tokens (obtain from provider dashboard)
export GITHUB_TOKEN="your-github-token-here"
export OPENAI_API_KEY="sk-your-key-here"

# Personal preferences
export EDITOR="vim"  # or code, nano, etc.
```

## Secret Detection

### Pre-commit Checks

Add to CI or git hooks:

```bash
# Check for common secret patterns
detect_secrets() {
    local patterns=(
        'api[_-]?key\s*[:=]'
        'secret[_-]?key\s*[:=]'
        'password\s*[:=]'
        'token\s*[:=]'
        'private[_-]?key'
    )

    for pattern in "${patterns[@]}"; do
        if git diff --cached | grep -iE "$pattern" | grep -v 'template\|example\|placeholder'; then
            error "Potential secret detected!"
            return 1
        fi
    done
}
```

### What to Never Commit

- API keys and tokens
- Passwords and credentials
- Private SSH keys
- Personal email addresses
- Internal URLs and endpoints
- Database connection strings
- OAuth client secrets
