---
name: dotfiles-conventions
description: Use when working in Jeff's dotfiles repository to understand structure, naming patterns, branch strategy, and Claude Code integration
---

# Dotfiles Repository Conventions

## Overview

**Repository**: Git-controlled dotfiles at `/Users/jefffarr/src/dotfiles`
**Main focus**: Emacs configuration using org-mode literate programming
**Multi-machine**: Hostname-specific configurations

**Core principle**: Org source files → generated elisp → modular loading → machine overrides

## When to Use

Use this skill when:
- Working in the dotfiles repository
- Understanding file naming patterns
- Need to know directory structure
- Understanding branch strategy
- Setting up Claude Code hooks/skills

## Directory Structure

```
dotfiles/
├── .claude/                    # Claude Code configuration
│   ├── hooks/                 # validate_elisp_syntax.py
│   ├── skills/                # This file and related skills
│   ├── instructions.md        # Main instructions (decomposed to skills)
│   └── settings.local.json    # Claude settings
├── bin/                       # Utility scripts (tangle-org.sh)
├── emacs/                     # Emacs configuration
│   ├── core/                 # Core functionality
│   ├── language-modes/       # Programming language configs
│   ├── major-modes/          # Major mode configs (org-roam, etc)
│   ├── look-and-feel/        # UI and themes
│   ├── local/                # Machine-specific ({hostname}.el)
│   └── init.org              # Main entry point
└── [other dotfiles...]
```

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Module files | `{category}/{name}.org` + `.el` | `core/completion.org` → `core/completion.el` |
| Daily journals | `YYYY-MM-DD.org` | `2025-01-05.org` |
| Knowledge notes | `YYYYMMDDHHMMSS-{slug}.org` | `20250105120000-emacs-config.org` |
| Machine configs | `{hostname}.el` | `Mac.home.el` |

### Module Categories
- **core**: Core functionality
- **language-modes**: Programming languages
- **major-modes**: Major mode configurations
- **look-and-feel**: UI and themes
- **local**: Machine-specific overrides

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `master` | Main development branch |
| `apploi_main` | Work-specific branch (current) |

**Usage**:
- Work-specific configs → work branch
- General improvements → master
- Machine-specific configs work across branches

## Claude Code Integration

### Hook System
- **File**: `.claude/hooks/validate_elisp_syntax.py`
- **Purpose**: Prevents invalid elisp in `.el` files
- **Scope**: Only validates `emacs/` directory

### Skills System
- **Location**: `.claude/skills/`
- **Purpose**: Modular knowledge for specialized assistance
- **Files**: See skills in this directory

## Module File Template

```org
#+title: Module Name
#+author: Jeff Farr
#+property: header-args:emacs-lisp :tangle module-name.el
#+auto_tangle: y

* Introduction
Description of module purpose.

* Configuration
#+begin_src emacs-lisp
;; -*- lexical-binding: t; -*-

;; Module implementation
#+end_src
```

## Package Configuration Template

```elisp
(use-package package-name
  :straight (package-name :type git :host github :repo "user/repo")
  :bind (("C-c k" . package-function))
  :hook (mode . package-mode)
  :config
  (setq package-setting value))
```

## Development Workflow

1. **Edit source**: Always edit `.org` files (see emacs-literate-programming)
2. **Follow structure**: Use established naming/directory conventions
3. **Test incrementally**: Use module reloading (see emacs-modular-config)
4. **Machine-specific**: Use hostname configs when needed (see machine-specific-config)

## Common Mistakes

| Mistake | Why Bad | Fix |
|---------|---------|-----|
| Editing `.el` files | Overwritten on tangle | Edit `.org` files |
| Wrong directory | Module won't load | Follow category structure |
| No commit both files | Repo out of sync | Commit both `.org` and `.el` |
| Secrets in repo | Security risk | Use machine configs, keep keys out |
| Ignoring startup time | Slow Emacs | Monitor, lazy-load packages |

## Best Practices

**File Management**:
- Commit both `.org` and `.el` files
- Never manually edit `.el` files
- Keep modules focused and independent

**Security**:
- No secrets in repository
- Use machine configs for private data
- Assume repo might be public

**Performance**:
- Monitor startup time impact
- Use error handling for resilience
- Consider lazy loading expensive operations

## Cross-References

For detailed information:
- Literate programming: See emacs-literate-programming skill
- Module system: See emacs-modular-config skill
- Org-roam setup: See org-roam-knowledge-mgmt skill
- Machine overrides: See machine-specific-config skill
