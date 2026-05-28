# Skill: modify-claude-alias

Cette skill permet de modifier l'alias PowerShell `claude` en toute sécurité, en préservant toutes les fonctionnalités existantes.

## Usage

Simplement demander à Claude de modifier le comportement de l'alias :

```
> claude
User: "Je veux que claude démarre toujours en mode verbose"
Claude: [Utilise automatiquement cette skill]
        [Lit la spécification de la fonction]
        [Modifie en préservant toutes les features]
        [Valide que tout fonctionne]
```

## Triggers

La skill se déclenche automatiquement quand vous utilisez ces phrases :

- "modifier l'alias claude"
- "changer la fonction claude"
- "update claude alias"
- "modifier le comportement de claude"

## Fonctionnalités préservées

La skill garantit que ces features ne seront JAMAIS supprimées :

1. ✅ Permission bypass (`--permission-mode bypassPermissions`)
2. ✅ MCP auto-détection (`.mcp.json`)
3. ✅ Gestion du titre d'onglet (nom du dossier)
4. ✅ `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` (empêche Claude de modifier le titre)
5. ✅ Recherche intelligente de claude.ps1/claude.cmd
6. ✅ Pass-through correct des arguments
7. ✅ Restauration du titre après exit

## Structure de la skill

```
.claude/skills/modify-claude-alias/
├── SKILL.md                      # Définition et instructions
├── README.md                     # Ce fichier
└── reference/
    └── claude-function-spec.md   # Spécification complète de la fonction
```

## Documentation

### reference/claude-function-spec.md

Contient la spécification complète de la fonction `claude` :
- Architecture section par section
- Rôle de chaque bloc de code
- Ce qui est modifiable vs ce qui ne l'est pas
- Historique des versions
- Cas d'usage à valider

**Toujours lire ce fichier avant de modifier l'alias !**

## Exemples de modifications

### Ajouter un flag par défaut

```
User: "Je veux que claude lance toujours avec --verbose"
Claude: [Lit la spec]
        [Modifie la ligne 403 pour ajouter --verbose]
        [Vérifie que toutes les features sont préservées]
```

### Changer la logique de resume

```
User: "Je veux que claude resume seulement si la dernière session a moins de 1h"
Claude: [Lit la spec]
        [Modifie la section 3 (logique de resume)]
        [Ajoute un check de temps]
        [Vérifie que toutes les features sont préservées]
```

### Ajouter une condition MCP

```
User: "Je veux que claude affiche un warning si pas de .mcp.json"
Claude: [Lit la spec]
        [Modifie la section 2 (MCP)]
        [Ajoute un Write-Host avec warning]
        [Vérifie que toutes les features sont préservées]
```

## Règles de sécurité

La skill respecte ces règles strictes :

- ❌ JAMAIS supprimer une fonctionnalité existante sans confirmation
- ❌ JAMAIS modifier la gestion du titre d'onglet
- ❌ JAMAIS modifier la recherche d'exécutable
- ✅ TOUJOURS vérifier `$cmdArgs` et `$passArgs`
- ✅ TOUJOURS tester mentalement les cas d'usage

## Validation automatique

Après chaque modification, la skill valide mentalement :

- `claude` → Fonctionne comme attendu
- `claude --help` → Affiche l'aide correctement
- `claude -m "prompt"` → Passe le prompt
- `claude` avec .mcp.json → Charge MCP
- Titre d'onglet → Affiche le nom du dossier

## Historique

### Version 2.1 (Actuelle)
- Resume automatique par défaut
- `claude .` / `claude new` pour forcer nouveau
- Suppression du check filesystem

### Version 2.0
- Resume si session existe
- `claude -` / `claude --new` pour forcer nouveau

### Version 1.0
- Pas de resume automatique
- MCP auto-détection
- Titre d'onglet

## Fichier modifié

`profile/Microsoft.PowerShell_profile.ps1` (fonction `claude`, lignes ~401-447)

## Déploiement

Après modification, le profil doit être copié vers `Documents\PowerShell\` :

```powershell
Copy-Item "profile/Microsoft.PowerShell_profile.ps1" -Destination "$HOME\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1" -Force
```

Puis recharger avec `rup` ou ouvrir un nouveau terminal.
