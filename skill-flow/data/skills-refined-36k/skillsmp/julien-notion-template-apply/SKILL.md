---
name: julien-notion-template-apply
description: >
  Applique un template Notion sur une page, générant le contenu dynamique via LLM.
  Parse les blocs {{ llm_generate }} et {{ inline_database }}.
  Use when creating pages from templates or regenerating template content.
version: "1.0.0"
license: Apache-2.0
user-invocable: true
allowed-tools:
  - Read
  - mcp__notion__notion-fetch
  - mcp__notion__notion-search
  - mcp__notion__notion-update-page
triggers:
  - "apply template"
  - "appliquer template"
  - "générer contenu"
  - "generate content"
  - "use template"
  - "utiliser template"
  - "create from template"
  - "créer depuis template"
metadata:
  author: "Julien"
  category: "notion"
  keywords: ["notion", "template", "llm", "generation"]
---

# Apply Notion Template

Applique un template stocké dans Templates [DB] sur une page Notion cible, en générant le contenu dynamique.

## Observability

**First**: At the beginning of execution, display:
```
🔧 Skill "julien-notion-template-apply" activated
```

## Prerequisites

- Database "Templates [DB]" existe avec au moins un template
- Page cible existe dans Notion
- Accès MCP Notion configuré

## Execution Steps

### Step 1: Identifier la page cible et le template

**Demander à l'utilisateur ou détecter :**
- URL ou ID de la page cible
- Nom du template à appliquer (ou détecter via property "Template")

### Step 2: Fetch le template depuis Templates [DB]

```
1. Rechercher dans "Templates [DB]" le template avec Status = "Active"
2. Parser le champ "Schema" (JSON)
3. Parser le champ "Content Template" (Markdown avec blocs)
```

### Step 3: Fetch la page cible

```
1. Récupérer les properties de la page
2. Valider que les properties requises sont présentes
3. Extraire les valeurs pour substitution
```

### Step 4: Parser et exécuter les blocs dynamiques

**Types de blocs :**

| Bloc | Action |
|------|--------|
| `{{ property }}` | Substitution directe par la valeur |
| `{{ llm_generate: "prompt" }}` | Générer le texte via Claude |
| `{{ inline_database ... }}` | Interpréter le filtre et créer le bloc |
| `{{ if condition }}` | Évaluer et inclure conditionnellement |

**Pour les blocs `llm_generate` :**
1. Substituer les variables dans le prompt
2. Générer le contenu (3-5 lignes concises)
3. Insérer dans le template

**Pour les blocs `inline_database` :**
1. Identifier la database source
2. Interpréter `filter_description` en filtre Notion
3. Créer le bloc linked database avec le filtre

### Step 5: Mettre à jour la page

```
1. Remplacer le contenu de la page avec le template rempli
2. Mettre à jour la property "Template" si elle existe
3. Confirmer la mise à jour
```

## Expected Output

**Page mise à jour avec :**
- Titre au format H1
- Callout avec description
- Sections générées par LLM
- Inline database filtrée

**Exemple de sortie :**
```
✓ Template "github-repo" appliqué sur "owner/repo-name"
  - 2 blocs LLM générés
  - 1 inline database créée
  - Property "Template" → "github-repo-v1.0.0"
```

## Error Handling

| Erreur | Cause | Solution |
|--------|-------|----------|
| Template non trouvé | Nom incorrect ou Status != Active | Vérifier le nom dans Templates [DB] |
| Property manquante | Property requise absente | Ajouter la property à la page d'abord |
| Page non accessible | Permissions Notion | Partager la page avec l'intégration |

## Skill Chaining

### Skills Required Before
- None (entry point skill)

### Input Expected
- **Format**: URL de page Notion + nom de template (optionnel)
- **Source**: User input ou property "Template" de la page

### Output Produced
- **Format**: Page Notion mise à jour
- **Side effects**: Contenu de page modifié

### Compatible Skills After
- **julien-notion-template-validate**: Vérifier la conformité après application

### Tools Used
- **mcp__notion__notion-fetch**: Lire template et page
- **mcp__notion__notion-search**: Trouver le template
- **mcp__notion__notion-update-page**: Appliquer le contenu

## Configuration

**Templates [DB] ID**: `005ff73e-512d-4a51-9c43-a1a8fb17791d`
**Database URL**: https://www.notion.so/2597cca0239b4ec58cee3b509d8cb860
