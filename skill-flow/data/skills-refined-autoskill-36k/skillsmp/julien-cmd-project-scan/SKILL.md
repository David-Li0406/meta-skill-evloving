---
name: julien-cmd-project-scan
description: Scan all configured project roots and update the registry
author: Julien
version: 1.0.0
category: infrastructure
type: command
triggers:
  - scan projects
  - update project registry
  - refresh projects
  - scanner les projets
  - mettre à jour le registre
  - rafraîchir les projets
  - discover projects
---

# Scan Project Roots

Scan tous les roots de projets configurés et met à jour le registre.

## Exécution

```bash
python "$MARKETPLACE_ROOT/scripts/project-registry.py" scan
```

Où `$MARKETPLACE_ROOT` est le chemin du marketplace (généralement `~/_Projets de code/2025.11 Claude Code MarketPlace`).

## Ce que fait cette commande

1. Parcourt les 3 roots configurés:
   - `_Projets de code` (pattern YYYY.MM)
   - `_référentiels de code\Hostinger`
   - `Portable Softwares\Autohotkey scripts`

2. Pour chaque sous-dossier:
   - Encode le chemin (style Claude Code)
   - Détecte le type de projet via patterns
   - Enregistre dans le registre

3. Marque les projets manquants (supprimés/déplacés)

4. Affiche les statistiques:
   - Projets scannés
   - Nouveaux projets
   - Projets mis à jour
   - Projets manquants

## Résultat

Le registre `registry/projects-registry.json` est mis à jour avec tous les projets découverts.
