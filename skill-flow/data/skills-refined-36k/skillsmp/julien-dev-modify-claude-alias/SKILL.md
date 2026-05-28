---
name: julien-dev-modify-claude-alias
description: |
  Modifie l'alias PowerShell `claude` en préservant toutes les fonctionnalités existantes.
  Gère les bypass permissions, MCP auto-détection, titre d'onglet et recherche d'exécutable.
triggers:
  - "modifier l'alias claude"
  - "changer la fonction claude"
  - "update claude alias"
  - "modifier le comportement de claude"
  - "powershell claude function"
---

# modify-claude-alias

## Description
Modifie l'alias PowerShell `claude` en préservant toutes les fonctionnalités existantes.

## Triggers
- "modifier l'alias claude"
- "changer la fonction claude"
- "update claude alias"
- "modifier le comportement de claude"

## Instructions
Tu es un expert en modification sécurisée de l'alias `claude` dans le profil PowerShell.

### Fonctionnalités à TOUJOURS préserver
1. `--permission-mode bypassPermissions` (ligne 403)
2. MCP auto-détection via `.mcp.json` (lignes 405-409)
3. Gestion du titre d'onglet (lignes 420-422, 445-446)
4. `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` (ligne 425)
5. Recherche intelligente de l'exécutable claude.ps1/claude.cmd (lignes 427-440)
6. Pass-through correct des arguments (ligne 443)
7. Restauration du titre après exit (ligne 445-446)

### Processus de modification
1. Lire le fichier `reference/claude-function-spec.md` pour comprendre la structure
2. Lire la fonction actuelle dans `profile/Microsoft.PowerShell_profile.ps1`
3. Vérifier que TOUTES les fonctionnalités ci-dessus sont présentes
4. Appliquer la modification demandée
5. Vérifier à nouveau que toutes les fonctionnalités sont préservées
6. Expliquer les changements effectués

### Fichiers concernés
- `profile/Microsoft.PowerShell_profile.ps1` (lignes 401-447)

### Règles de sécurité
- ❌ JAMAIS supprimer une fonctionnalité existante sans confirmation explicite
- ❌ JAMAIS modifier les lignes de gestion du titre d'onglet
- ❌ JAMAIS modifier la recherche d'exécutable
- ✅ TOUJOURS vérifier que `$cmdArgs` et `$passArgs` sont correctement construits
- ✅ TOUJOURS tester mentalement les cas d'usage courants

### Cas d'usage à valider

Après toute modification, vérifier mentalement ces cas :
- `claude` → Doit reprendre ou démarrer selon la logique
- `claude --help` → Doit fonctionner
- `claude -m "prompt"` → Doit passer le prompt
- `claude` avec .mcp.json → Doit charger MCP
- Titre d'onglet → Doit afficher le nom du dossier
