---
name: dotfiles-teacher
description: Dotfiles management best practices for XDG-compliant, cross-platform, and maintainable configurations. Use when adding new config files to dotfiles, refactoring existing configurations, improving setup scripts, or ensuring security with sensitive data separation. Covers automation (Makefile, CI/CD), maintainability (modularity, documentation), and security (.local pattern).
---

# Dotfiles Teacher

Provide guidance on dotfiles best practices with focus on:
- **Maintainability**: Modular structure, clear naming, XDG compliance
- **Security**: Sensitive data separation via `.local` pattern
- **Automation**: Makefile orchestration, CI/CD testing

## Quick Reference

### Adding New Config

1. Place config in `config/<tool-name>/`
2. Update `link.sh` to create symlink
3. Add `.local.template` for sensitive values
4. Test with `make link && make verify`

### Script Standards

```bash
#!/bin/bash
set -eu
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

info "Starting task"
# Use helper functions: isRunningOnMac, safeDownload, etc.
success "Task complete"
```

### Security Pattern

```
config/tool/config          # Public (committed)
config/tool/config.local.template  # Template (committed)
~/.config/tool/config.local # Private (not committed)
```

## Detailed References

- **[structure.md](references/structure.md)**: Directory layout, XDG Base Directory, naming conventions
- **[scripts.md](references/scripts.md)**: Shell script patterns, error handling, helper functions
- **[security.md](references/security.md)**: Sensitive data separation, .local pattern, gitignore
- **[automation.md](references/automation.md)**: Makefile targets, CI/CD, testing strategies
