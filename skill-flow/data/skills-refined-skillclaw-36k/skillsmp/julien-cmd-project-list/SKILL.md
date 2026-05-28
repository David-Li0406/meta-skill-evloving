---
name: julien-cmd-project-list
description: List all registered projects from the registry
author: Julien
version: 1.0.0
category: infrastructure
type: command
triggers:
  - list projects
  - show projects
  - all projects
  - lister les projets
  - afficher les projets
  - projets enregistrés
  - registered projects
---

# List Registered Projects

Liste tous les projets enregistrés dans le registre.

## Exécution

```bash
python "$MARKETPLACE_ROOT/scripts/project-registry.py" list
```

## Affichage

Pour chaque projet:
- Status: `[OK]` (actif) ou `[??]` (manquant)
- Nom du projet (extrait du dossier)
- Type détecté (wordpress, hostinger, calibre, etc.)
- Chemin complet
- Skills associés

## Exemple de sortie

```
Projets enregistrés (25):

[OK] Claude Code MarketPlace
    Type: marketplace
    Path: C:\Users\julien\...\2025.11 Claude Code MarketPlace
    Skills: *

[OK] Site Clem
    Type: wordpress-hostinger
    Path: C:\Users\julien\...\2025.10 Site internet Clem
    Skills: julien-wordpress-*, julien-infra-hostinger-*

[??] Ancien Projet
    Type: nodejs
    Path: C:\Users\julien\...\2024.01 Ancien Projet
    Skills: (aucun)
```

## Commandes associées

- `/project-scan` - Rafraîchir le registre
- `/project-info` - Détails du projet courant
