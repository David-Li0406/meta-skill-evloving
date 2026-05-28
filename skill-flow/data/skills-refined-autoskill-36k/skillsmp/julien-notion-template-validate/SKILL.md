---
name: julien-notion-template-validate
description: >
  Valide la conformité d'une page Notion par rapport à son template.
  Vérifie les properties requises et la structure du contenu.
  Use when checking template compliance or auditing pages.
version: "1.0.0"
license: Apache-2.0
user-invocable: true
allowed-tools:
  - Read
  - mcp__notion__notion-fetch
  - mcp__notion__notion-search
triggers:
  - "validate template"
  - "valider template"
  - "check conformity"
  - "vérifier conformité"
  - "template compliance"
  - "conformité template"
  - "is page valid"
  - "page conforme"
metadata:
  author: "Julien"
  category: "notion"
  keywords: ["notion", "template", "validation", "conformity"]
---

# Validate Notion Template

Vérifie qu'une page Notion est conforme à son template défini dans Templates [DB].

## Observability

**First**: At the beginning of execution, display:
```
🔧 Skill "julien-notion-template-validate" activated
```

## Prerequisites

- Database "Templates [DB]" existe avec le template référencé
- Page cible a une property "Template" ou appartient à une DB avec template par défaut

## Execution Steps

### Step 1: Identifier la page et son template

```
1. Fetch la page Notion
2. Lire la property "Template" ou identifier via la database parente
3. Fetch le template correspondant dans Templates [DB]
```

### Step 2: Valider les properties

**Pour chaque property dans schema.properties.required :**
```
1. Vérifier que la property existe
2. Vérifier que le type correspond
3. Si "format" défini : valider avec regex
4. Si "min" défini : vérifier la valeur minimale
```

**Scoring :**
- Property présente et valide : ✓
- Property présente mais invalide : ⚠
- Property manquante : ✗

### Step 3: Valider la structure du contenu

**Parser le Content Template et vérifier :**
1. Présence des sections H1/H2 attendues
2. Présence du callout description
3. Présence des inline databases
4. Contenu non-vide dans les sections LLM

### Step 4: Générer le rapport

```
┌─────────────────────────────────────────┐
│ Rapport de conformité                   │
│ Page: owner/repo-name                   │
│ Template: github-repo v1.0.0            │
├─────────────────────────────────────────┤
│ Properties                              │
│ ✓ Name: owner/repo-name (format OK)    │
│ ✓ Language: Python                      │
│ ✓ Tags: [ML, AI] (min 1 OK)            │
│ ⚠ Description: (vide)                   │
│ ✗ Template: (manquant)                  │
├─────────────────────────────────────────┤
│ Contenu                                 │
│ ✓ H1 titre présent                      │
│ ✓ Callout description                   │
│ ⚠ Section Résumé: vide                  │
│ ✓ Inline database présente              │
├─────────────────────────────────────────┤
│ Score: 75% (⚠ Partiellement conforme)   │
└─────────────────────────────────────────┘
```

## Expected Output

**Rapport avec :**
- Liste des properties avec statut
- Liste des sections avec statut
- Score global (%)
- Statut : ✓ Conforme (>90%), ⚠ Partiel (50-90%), ✗ Non conforme (<50%)

**Actions suggérées si non conforme :**
```
Suggestions:
1. Ajouter la property "Template" avec valeur "github-repo-v1.0.0"
2. Remplir la description
3. Exécuter /apply-template pour régénérer les sections
```

## Error Handling

| Erreur | Cause | Solution |
|--------|-------|----------|
| Template non identifié | Property "Template" absente | Spécifier le template manuellement |
| Schema invalide | JSON mal formé dans template | Corriger le schema dans Templates [DB] |

## Skill Chaining

### Skills Required Before
- None (peut être appelé indépendamment)

### Input Expected
- **Format**: URL de page Notion
- **Source**: User input

### Output Produced
- **Format**: Rapport de conformité (texte)
- **Side effects**: Aucun (lecture seule)

### Compatible Skills After
- **julien-notion-template-apply**: Si le score est bas, suggérer d'appliquer le template

### Tools Used
- **mcp__notion__notion-fetch**: Lire page et template
- **mcp__notion__notion-search**: Trouver le template

## Configuration

**Templates [DB] ID**: `005ff73e-512d-4a51-9c43-a1a8fb17791d`
