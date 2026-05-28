---
name: init-project
description: Interactive wizard for configuring ticket resolution workflow. Creates .claude/ticket-config.json with source, branch, and complexity settings.
---

# Init Project Skill

Interactive configuration wizard that creates `.claude/ticket-config.json` to configure the ticket resolution workflow for a project.

## When to Use

- First time running `/resolve` in a project
- Reconfiguring project settings
- Called via `/resolve --init`

## Wizard Flow

### 1. Welcome

```markdown
# Configuration du projet pour /resolve

Ce wizard va creer le fichier `.claude/ticket-config.json` pour configurer
le workflow de resolution de tickets dans ce projet.
```

### 2. Source Configuration

```
AskUserQuestion:
  question: "Quelle source de tickets utilisez-vous principalement ?"
  header: "Source"
  options:
    - label: "YouTrack"
      description: "Tickets YouTrack via MCP"
    - label: "GitHub Issues"
      description: "Issues et PRs GitHub via gh CLI"
    - label: "Les deux"
      description: "Detection automatique selon le format"
```

**If YouTrack selected or "Les deux"**:
```
AskUserQuestion:
  question: "Quel est le prefixe de votre projet YouTrack ?"
  header: "YouTrack"
  options:
    - label: "Entrer le prefixe"
      description: "Ex: PROJ, MYAPP, BACK..."
```
User enters prefix (e.g., "PROJ")

**If GitHub selected or "Les deux"**:
```
AskUserQuestion:
  question: "Quel est le repository GitHub ?"
  header: "GitHub"
  options:
    - label: "Detecter automatiquement"
      description: "Utiliser 'git remote get-url origin'"
    - label: "Entrer manuellement"
      description: "Format: owner/repo"
```
- If auto-detect: run `git remote get-url origin` and extract owner/repo
- If manual: user enters "owner/repo"

### 3. Branch Configuration

```
AskUserQuestion:
  question: "Quelle est votre branche principale ?"
  header: "Base branch"
  options:
    - label: "main"
      description: "Convention moderne"
    - label: "master"
      description: "Convention classique"
    - label: "develop"
      description: "Gitflow - branche de dev"
```

```
AskUserQuestion:
  question: "Comment nommer les branches de feature ?"
  header: "Prefixes"
  options:
    - label: "Standard (Recommended)"
      description: "feat/, fix/, refactor/, docs/"
    - label: "Simple"
      description: "feature/, bugfix/"
    - label: "Avec ticket"
      description: "PROJ-123/description"
```

### 4. Complexity Defaults

```
AskUserQuestion:
  question: "Comportement par defaut pour la complexite ?"
  header: "Complexite"
  options:
    - label: "Detection automatique (Recommended)"
      description: "Analyser le contenu du ticket"
    - label: "Toujours simple"
      description: "Workflow rapide sans exploration"
    - label: "Toujours complet"
      description: "AEP + Architect systematique"
```

### 5. Generate Configuration

Build config object based on answers:

```json
{
  "default_source": "auto|youtrack|github",
  "youtrack": {
    "project_prefix": "PROJ"
  },
  "github": {
    "repo": "owner/repo"
  },
  "branches": {
    "default_base": "main|master|develop",
    "prefix_mapping": {
      "bug": "fix",
      "feature": "feat",
      "task": "feat",
      "refactoring": "refactor",
      "documentation": "docs"
    }
  },
  "complexity": {
    "auto_detect": true|false,
    "default_level": "simple|medium|complex"
  },
  "simplify": {
    "enabled": true,
    "agent": "auto",
    "scope": "modified",
    "auto_apply": false
  },
  "review": {
    "enabled": true,
    "auto_fix": false,
    "severity_threshold": "important",
    "block_on_critical": true
  },
  "pr": {
    "draft_by_default": true,
    "default_target": null,
    "include_ticket_link": true,
    "title_format": "{type}: {title} ({ticket_id})"
  }
}
```

### 6. Save Configuration

```bash
mkdir -p .claude
```

Write to `.claude/ticket-config.json`.

### 7. Confirmation

```markdown
# Configuration sauvegardee

Fichier cree: `.claude/ticket-config.json`

```json
{content of generated config}
```

## Utilisation

```bash
# Resoudre un ticket
/resolve PROJ-123

# Mode automatique
/resolve PROJ-123 --auto

# Modifier la config
/resolve --init
```

Le projet est pret pour utiliser /resolve !
```

## Output

After completion, the skill creates:
- `.claude/ticket-config.json` - Project configuration file

**IMPORTANT**: After this skill completes, the workflow STOPS. Do not continue to ticket resolution.
