---
name: julien-cmd-project-info
description: Display information about the current project or a specified path
author: Julien
version: 1.0.0
category: infrastructure
type: command
triggers:
  - project info
  - current project
  - show project
  - info projet
  - projet courant
  - afficher projet
  - project details
---

# Project Information

Affiche les informations du projet courant (ou d'un chemin spécifié).

## Exécution

```bash
# Projet courant
python "$MARKETPLACE_ROOT/scripts/project-registry.py" info

# Chemin spécifique
python "$MARKETPLACE_ROOT/scripts/project-registry.py" info "C:\chemin\vers\projet"
```

## Informations affichées

- **Nom**: Nom du projet (extrait du dossier)
- **Type**: Type détecté (wordpress, hostinger, calibre, etc.)
- **Path**: Chemin complet
- **Skills**: Patterns de skills associés
- **Git**: Remote git si disponible
- **Tags**: Tags du projet
- **Découvert**: Date de première découverte
- **Vu**: Dernière fois vu lors d'un scan

## Si le projet n'est pas enregistré

```
Projet non enregistré: C:\chemin\vers\projet
Utilisez 'discover' pour l'enregistrer.
```

Dans ce cas, utilisez `/project-scan` ou exécutez:
```bash
python "$MARKETPLACE_ROOT/scripts/project-registry.py" discover "C:\chemin\vers\projet"
```
