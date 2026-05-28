---
name: julien-skill-router
description: "Index of available skills with triggers. Use FIRST when starting any task to check which skill might help."
license: Apache-2.0
allowed-tools: [Skill]
metadata:
  author: "Julien"
  version: "1.0.0"
  category: "workflow"
  keywords: ["router", "skills", "index", "triggers", "auto-activation"]
triggers:
  - "which skill"
  - "find skill"
  - "skill for"
  - "right skill"
  - "quelle skill"
  - "trouver skill"
  - "skill pour"
  - "bonne skill"
  - "what skill should I use"
  - "recommend a skill"
---

# Skill Router - Index des Skills Disponibles

Consulte cette skill au début de chaque tâche pour identifier si une skill existante peut t'aider.

## Development Tools

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-skill-router" activated
```

| Skill | Triggers | Description |
|-------|----------|-------------|
| `julien-dev-tools-claude-md-documenter` | CLAUDE.md, document project, project instructions | Créer/améliorer CLAUDE.md |
| `julien-dev-tools-skill-creator` | create skill, new skill, SKILL.md, skill template | Créer/modifier une skill |
| `julien-dev-tools-skill-reviewer` | review skill, check skill, improve skill, skill quality | Évaluer qualité d'une skill |
| `julien-dev-tools-hook-creator` | create hook, new hook, hook template | Créer un hook Claude Code |

## Workflow

| Skill | Triggers | Description |
|-------|----------|-------------|
| `julien-workflow-check-loaded-skills` | loaded skills, check skills, list skills | Vérifier les skills chargées |
| `julien-workflow-sync-personal-skills` | sync skills, synchronize | Synchroniser skills au marketplace |

## Anthropic Office (Documents)

| Skill | Triggers | Description |
|-------|----------|-------------|
| `anthropic-office-pdf` | PDF, form, document | Manipuler fichiers PDF |
| `anthropic-office-xlsx` | Excel, spreadsheet, xlsx | Manipuler fichiers Excel |
| `anthropic-office-docx` | Word, document, docx | Manipuler fichiers Word |
| `anthropic-office-pptx` | PowerPoint, presentation, pptx | Manipuler présentations |

## Anthropic Web/Design

| Skill | Triggers | Description |
|-------|----------|-------------|
| `anthropic-web-frontend-design` | frontend, UI, web design, React | Créer interfaces web |
| `anthropic-design-canvas` | poster, art, visual, infographic | Créer visuels/posters |
| `anthropic-web-artifacts-builder` | prototype, demo, artifact | Créer prototypes web |
| `anthropic-web-testing` | test, playwright, webapp | Tester applications web |
| `anthropic-dev-tools-mcp-builder` | MCP, server, integration | Créer serveurs MCP |

## Infrastructure Hostinger

| Skill | Triggers | Description |
|-------|----------|-------------|
| `julien-infra-hostinger-ssh` | SSH, server, connect | Connexion SSH au VPS |
| `julien-infra-hostinger-docker` | Docker, container | Gérer containers Docker |
| `julien-infra-hostinger-nginx` | Nginx, proxy, SSL | Configurer Nginx |
| `julien-infra-hostinger-database` | database, PostgreSQL, Redis | Gérer bases de données |
| `julien-infra-hostinger-deployment` | deploy, production | Déployer sur VPS |

## Comment Utiliser

1. **Au début d'une tâche**: Consulte ce tableau pour voir si une skill existe
2. **Si match trouvé**: `Skill("nom-de-la-skill")`
3. **Si pas de match**: Procède normalement

## Pattern d'Activation

```
User: "crée moi un CLAUDE.md"
→ Match: "CLAUDE.md" → Skill("julien-dev-tools-claude-md-documenter")

User: "je veux créer une nouvelle skill"
→ Match: "create skill" → Skill("julien-dev-tools-skill-creator")

User: "déploie sur le serveur"
→ Match: "deploy" → Skill("julien-infra-hostinger-deployment")
```
