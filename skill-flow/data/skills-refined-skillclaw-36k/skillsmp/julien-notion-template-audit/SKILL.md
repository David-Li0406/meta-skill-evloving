---
name: julien-notion-template-audit
description: >
  Audit de conformité d'une database Notion entière.
  Calcule le % de pages conformes, identifie les pages orphelines.
  Use when auditing databases or planning template migrations.
version: "1.0.0"
license: Apache-2.0
user-invocable: true
allowed-tools:
  - Read
  - mcp__notion__notion-fetch
  - mcp__notion__notion-search
triggers:
  - "audit database"
  - "audit base"
  - "template audit"
  - "audit templates"
  - "conformity report"
  - "rapport conformité"
  - "database health"
  - "santé base"
  - "orphan pages"
  - "pages orphelines"
metadata:
  author: "Julien"
  category: "notion"
  keywords: ["notion", "template", "audit", "database", "conformity"]
---

# Audit Notion Templates

Audit complet d'une database Notion pour évaluer la conformité des pages par rapport aux templates.

## Observability

**First**: At the beginning of execution, display:
```
🔧 Skill "julien-notion-template-audit" activated
```

## Prerequisites

- Database Notion cible accessible
- Templates [DB] configurée avec templates pour cette database

## Execution Steps

### Step 1: Identifier la database et les templates applicables

```
1. Fetch la database cible
2. Rechercher dans Templates [DB] les templates où Target DBs contient cette database
3. Ou identifier via la property "Template" des pages existantes
```

### Step 2: Analyser chaque page

**Pour chaque page de la database :**
```
1. Identifier le template applicable (via property "Template" ou défaut)
2. Valider les properties requises
3. Vérifier la structure du contenu
4. Calculer le score de conformité
5. Catégoriser : Conforme / Partiel / Non conforme / Orphelin
```

**Catégories :**
- **Conforme** (✓): Score > 90%
- **Partiel** (⚠): Score 50-90%
- **Non conforme** (✗): Score < 50%
- **Orphelin** (?): Pas de template identifiable

### Step 3: Agréger les statistiques

```
- Total pages analysées
- Par catégorie : nombre et %
- Par template : distribution
- Properties les plus souvent manquantes
- Sections les plus souvent vides
```

### Step 4: Générer le rapport d'audit

```
╔═════════════════════════════════════════════════════════╗
║          AUDIT: Github [DB]                             ║
║          Date: 2026-01-15                               ║
╠═════════════════════════════════════════════════════════╣
║ RÉSUMÉ                                                  ║
║ ───────────────────────────────────────────────────     ║
║ Total pages: 156                                        ║
║                                                         ║
║ ✓ Conformes:     89 (57%)  ████████████░░░░░░░░        ║
║ ⚠ Partielles:    42 (27%)  ██████░░░░░░░░░░░░░░        ║
║ ✗ Non conformes: 18 (12%)  ███░░░░░░░░░░░░░░░░░        ║
║ ? Orphelines:     7 (4%)   █░░░░░░░░░░░░░░░░░░░        ║
╠═════════════════════════════════════════════════════════╣
║ PAR TEMPLATE                                            ║
║ ───────────────────────────────────────────────────     ║
║ github-repo v1.0.0:  142 pages                          ║
║   - Conformes: 85 (60%)                                 ║
║   - Partielles: 40 (28%)                                ║
║   - Non conformes: 17 (12%)                             ║
║                                                         ║
║ (sans template): 14 pages                               ║
╠═════════════════════════════════════════════════════════╣
║ PROBLÈMES FRÉQUENTS                                     ║
║ ───────────────────────────────────────────────────     ║
║ Properties manquantes:                                  ║
║   1. Description (45 pages)                             ║
║   2. Template (32 pages)                                ║
║   3. Tags (12 pages)                                    ║
║                                                         ║
║ Sections vides:                                         ║
║   1. Résumé (38 pages)                                  ║
║   2. Cas d'usage (25 pages)                             ║
╠═════════════════════════════════════════════════════════╣
║ RECOMMANDATIONS                                         ║
║ ───────────────────────────────────────────────────     ║
║ 1. Exécuter /apply-template sur 45 pages sans contenu   ║
║ 2. Ajouter property "Template" aux 32 pages manquantes  ║
║ 3. Investiguer les 7 pages orphelines                   ║
╚═════════════════════════════════════════════════════════╝
```

## Expected Output

**Rapport complet avec :**
- Statistiques globales
- Distribution par template
- Problèmes fréquents classés
- Recommandations actionnables

**Export optionnel :**
- Liste des pages non conformes (URLs)
- CSV avec scores par page

## Error Handling

| Erreur | Cause | Solution |
|--------|-------|----------|
| Database trop grande | Plus de 100 pages | Limiter l'audit ou paginer |
| Timeout | Trop de requêtes | Augmenter les délais entre requêtes |

## Skill Chaining

### Skills Required Before
- None (entry point pour audits)

### Input Expected
- **Format**: URL ou ID de database Notion
- **Source**: User input

### Output Produced
- **Format**: Rapport d'audit (texte formaté)
- **Side effects**: Aucun (lecture seule)

### Compatible Skills After
- **julien-notion-template-apply**: Appliquer templates sur pages non conformes
- **julien-notion-template-validate**: Validation détaillée page par page

### Tools Used
- **mcp__notion__notion-fetch**: Lire database et pages
- **mcp__notion__notion-search**: Parcourir les pages

## Configuration

**Templates [DB] ID**: `005ff73e-512d-4a51-9c43-a1a8fb17791d`
