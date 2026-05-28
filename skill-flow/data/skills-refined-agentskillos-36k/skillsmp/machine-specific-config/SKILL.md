---
name: machine-specific-config
description: Use when setting up dotfiles on new machines or creating hostname-based configuration overrides for work/home/different environments
---

# Machine-Specific Configuration Management

## Overview

**Multi-Machine Support**: Same dotfiles repo works across multiple machines using hostname detection and automatic config overrides.

**Core principle**: Detect hostname → auto-load `local/{hostname}.el` → apply machine-specific overrides

## When to Use

Use this skill when:
- Setting up dotfiles on a new machine
- Creating machine-specific settings
- Debugging why config differs between machines
- Understanding which hostname config is active
- Separating work/home/personal configurations

## Quick Reference

| Task | How | Details |
|------|-----|---------|
| Check hostname | `(system-name)` in Emacs | Returns current hostname |
| Machine variable | `jf/machine-name` | Stores detected hostname |
| Config file | `emacs/local/{hostname}.el` | Auto-loaded during init |
| Create override | Create file, add setq/config | Restart Emacs to load |

## Configuration Pattern

### Setup New Machine

1. Check hostname: Eval `(system-name)` in Emacs
2. Create file: `emacs/local/{hostname}.el`
3. Add overrides (see examples below)
4. Restart Emacs (changes load automatically)

### Override Examples

```elisp
;; emacs/local/Mac.home.el

;; Machine-specific org-roam dailies
(setq org-roam-dailies-directory "dailies/Mac.home/")

;; Local paths
(setq my-documents-path "/Users/jefffarr/Documents/")

;; Machine-specific keybindings
(global-set-key (kbd "C-c h") 'home-function)

;; Package config override
(use-package some-package
  :config
  (setq package-setting 'home-value))
```

## Common Machine-Specific Settings

| Category | Examples |
|----------|----------|
| **Org-roam** | `org-roam-dailies-directory`, org directories, capture templates |
| **File Paths** | Document roots, project workspaces, backup directories |
| **Packages** | Different configs for work/home, integrations, dev tools |
| **Display** | Monitor settings, font sizes, themes, window rules |

## Multi-Environment Strategy

### Environment Types
- **Work machines**: Work org-roam, work packages
- **Personal machines**: Home directories, personal tools
- **Cross-platform**: Platform-specific paths/packages

### Load Order
1. Core modules (from `jf/enabled-modules`)
2. All standard modules
3. Machine config (automatic from `local/{hostname}.el`)

## Debugging

**Check current machine**:
- Variable: `C-h v jf/machine-name`
- Returns: Current hostname

**File not loading**:
- Verify filename matches hostname exactly
- Check file exists in `emacs/local/` directory
- Restart Emacs after creating file

**Override not working**:
- Machine configs load last (correct)
- Verify variable name is correct
- Check for typos in hostname

## Common Mistakes

| Mistake | Why Bad | Fix |
|---------|---------|-----|
| Wrong hostname | File won't load | Use exact output of `(system-name)` |
| Too many overrides | Hard to maintain | Only override what's different |
| No documentation | Forget why override exists | Comment purpose of overrides |
| Secrets in file | Security risk | Keep credentials out of repo |
| Duplicating base config | Maintenance burden | Override minimally |

## Best Practices

- **Minimal overrides**: Only change what's actually different
- **Document purpose**: Comment why settings are machine-specific
- **No secrets**: Keep API keys and credentials out
- **Logical grouping**: Keep related overrides together
- **Test isolation**: Verify base config still works without overrides
