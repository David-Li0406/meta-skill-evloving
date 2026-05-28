---
name: julien-notion-github-enricher
description: >
  Enrichit une page Github [DB] avec métadonnées GitHub API, README, vidéos YouTube et articles liés.
  Crée des entrées dans Youtube [DB] et Ressources Web [DB] avec relations bidirectionnelles.
  Gère le tracking de fraîcheur (Last Sync, Sync Status).
version: "3.0.0"
license: Apache-2.0
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - WebFetch
  - WebSearch
  - mcp__notion__notion-fetch
  - mcp__notion__notion-search
  - mcp__notion__notion-update-page
  - mcp__notion__notion-create-pages
triggers:
  - "enrich github"
  - "enrichir github"
  - "github metadata"
  - "sync github"
  - "update github"
  - "github info"
  - "refresh github"
  - "rafraîchir github"
  - "outdated repos"
  - "repos obsolètes"
  - "find videos for repo"
  - "find articles for repo"
metadata:
  author: "Julien"
  category: "notion"
  keywords: ["notion", "github", "api", "enrichment", "sync", "youtube", "articles"]
---

# GitHub Enricher pour Notion (v3)

Enrichissement complet des pages Github [DB] avec :
- Métadonnées GitHub API
- Description réelle depuis README.md
- Images du README
- Vidéos YouTube liées → Youtube [DB]
- Articles liés → Ressources Web [DB]
- Relations bidirectionnelles entre les DBs

## Observability

**First**: At the beginning of execution, display:
```
🔧 Skill "julien-notion-github-enricher" v3.0.0 activated
```

## Databases impliquées

| Database | ID | Data Source | Rôle |
|----------|-----|-------------|------|
| Github [DB] | `2cacdc04-12e3-81cc-a84e-fdbba086ab29` | `collection://2cacdc04-12e3-8182-b4f0-000b3089ad8a` | Page cible |
| Youtube [DB] | `143cdc04-12e3-8030-8fb2-c2fb46f78037` | `collection://8a93155c-0f2e-4254-bbce-547bbbe56fd1` | Vidéos liées |
| Ressources Web [DB] | `afbf024b-2d2c-49eb-b035-99a4d495f19f` | `collection://b85380b8-e636-4aa9-a3dd-6496afd59a47` | Articles liés |

## Données récupérées

### Depuis GitHub API
| Champ Notion | Source GitHub API | Description |
|--------------|-------------------|-------------|
| `Description` | `description` ou README | Description du repo |
| `Language` | `language` | Langage principal |
| `Stars` | `stargazers_count` | Nombre d'étoiles |
| `Topics` | `topics` | Tags/catégories |
| `Last Commit` | `pushed_at` | Date du dernier push |
| `Last Sync` | (calculé) | Date d'exécution |
| `Sync Status` | (calculé) | Fresh/Outdated/Error |

### Depuis README.md
| Donnée | Utilisation |
|--------|-------------|
| Vraie description | Si API description est vide/courte |
| Images | Cover image + gallery dans contenu |

### Depuis Web Search
| Source | Destination | Tag |
|--------|-------------|-----|
| Vidéos YouTube | Youtube [DB] | `Auto-Enrichment` |
| Articles web | Ressources Web [DB] | `Auto-Enrichment` |

## Logique de Sync Status

```
Si Last Commit > Last Sync → "Outdated" (repo modifié depuis dernier sync)
Si Last Commit ≤ Last Sync → "Fresh" (données à jour)
Si erreur API → "Error"
Si jamais sync → "Never Synced"
```

## Execution Steps

### Step 1: Identifier la page

**Input accepté :**
- URL Notion complète
- Page ID (UUID)
- Nom du repo (recherche dans Github [DB])

```
Fetch la page via MCP notion-fetch
Extraire la property "URL" (lien GitHub)
```

### Step 2: Parser l'URL GitHub

```
https://github.com/owner/repo → owner, repo
Ignorer les URLs d'organisation (pas de /repo)
```

### Step 3: Appeler l'API GitHub

**Endpoint :** `https://api.github.com/repos/{owner}/{repo}`

**Headers :**
```
Accept: application/vnd.github.v3+json
Authorization: token {GITHUB_TOKEN}  # optionnel, augmente rate limit
```

**Données extraites :**
```json
{
  "description": "...",
  "language": "Python",
  "stargazers_count": 1234,
  "topics": ["ai", "automation"],
  "pushed_at": "2026-01-10T15:30:00Z"
}
```

### Step 4: Fetch README.md (NOUVEAU v3)

**URL :** `https://raw.githubusercontent.com/{owner}/{repo}/main/README.md`
- Fallback: `master`, `HEAD`

**Extraction :**
```
1. Si API description vide/courte (<50 chars):
   - Extraire les 500 premiers caractères après badges
   - Résumer avec Claude si trop long

2. Extraire images:
   - Regex: !\[.*?\]\((.*?)\)
   - Filtrer: badges, shields.io, github stats
   - Garder: screenshots, diagrammes, démos
```

### Step 5: Rechercher vidéos YouTube (NOUVEAU v3)

**Via WebSearch :**
```
Query: "{repo_name} tutorial" OR "{repo_name} demo" site:youtube.com
Limiter à 3-5 résultats pertinents
```

**Pour chaque vidéo trouvée :**
1. Vérifier si déjà dans Youtube [DB] (via URL)
2. Si non, créer page dans Youtube [DB]:
   ```
   Nom: Titre de la vidéo
   Créateur: Nom de la chaîne
   URL: URL YouTube
   Étiquettes: ["Auto-Enrichment", "{Language}"]
   Related Repo: [page Github courante]
   ```

### Step 6: Rechercher articles (NOUVEAU v3)

**Via WebSearch :**
```
Query: "{repo_name} tutorial" OR "{repo_name} guide" OR "{repo_name} article"
Sources: dev.to, medium.com, hackernews, blogs tech
Limiter à 3-5 résultats pertinents
```

**Pour chaque article trouvé :**
1. Vérifier si déjà dans Ressources Web [DB] (via URL)
2. Si non et MCP fonctionne, créer page:
   ```
   Titre: Titre de l'article
   URL: URL de l'article
   Source/Étiquettes: "Auto-Enrichment"
   Related Repo: [page Github courante]
   ```

### Step 7: Mettre à jour la page Github [DB]

```
Via MCP notion-update-page :
- Description (de README si API vide)
- Language (mappé aux options existantes ou "Other")
- Stars
- Topics (multi-select)
- Last Commit (date de pushed_at)
- Last Sync (date actuelle)
- Sync Status (Fresh si succès)
- Related Videos (relation vers vidéos créées)
- Related Articles (relation vers articles créés) - si disponible
```

### Step 8: Ajouter la cover image

```
Priorité:
1. Première image pertinente du README
2. OpenGraph: https://opengraph.githubassets.com/1/{owner}/{repo}

Note: Notion MCP ne supporte pas la modification de cover directement
      → Informer l'utilisateur de l'URL pour ajout manuel
```

### Step 9: Optionnel - Appliquer le template

Si demandé, chaîner avec `julien-notion-template-apply` pour générer le contenu LLM.

## Commandes

### Enrichir une page

```bash
# Via URL Notion
"Enrich https://www.notion.so/2e2cdc0412e3817aa6e1ed43902bdc40"

# Via nom de repo
"Enrich leonvanzyl/autocoder"
```

### Enrichir toutes les pages Never Synced

```bash
"Enrich all never synced github repos"
```

### Lister les pages Outdated

```bash
"Show outdated github repos"
```

## Rate Limits GitHub

| Authentification | Limite |
|------------------|--------|
| Sans token | 60 req/heure |
| Avec `GITHUB_TOKEN` | 5000 req/heure |

**Configurer le token :**
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

## Mapping des langages

| GitHub | Notion Option |
|--------|---------------|
| Python | Python |
| JavaScript | JavaScript |
| TypeScript | TypeScript |
| Go | Go |
| Rust | Rust |
| Autres | Other |

## Error Handling

| Erreur | Cause | Action |
|--------|-------|--------|
| `REPO_NOT_FOUND` | Repo supprimé ou privé | Sync Status → Error |
| `RATE_LIMITED` | Limite API atteinte | Attendre ou configurer token |
| `NOT_GITHUB_URL` | URL invalide | Skip, signaler |
| `NO_URL` | Property URL vide | Skip, signaler |

## Skill Chaining

### Skills Required Before
- None (entry point)

### Input Expected
- URL/ID de page Notion, ou nom de repo GitHub

### Output Produced
- Page Notion mise à jour avec métadonnées
- Sync Status et Last Sync trackés

### Compatible Skills After
- **julien-notion-template-apply** : Générer le contenu LLM
- **julien-notion-template-validate** : Vérifier conformité

### Visual Workflow

```
Page Notion (Github [DB])
    ↓
[1] Extraire URL GitHub
    ↓
[2] API GitHub → metadata (stars, language, topics, pushed_at)
    ↓
[3] Fetch README.md → vraie description + images
    ↓
[4] WebSearch YouTube → vidéos pertinentes
    │
    └──► Créer pages dans Youtube [DB]
         avec tag "Auto-Enrichment" et relation
    ↓
[5] WebSearch articles → tutoriels, guides
    │
    └──► Créer pages dans Ressources Web [DB]
         avec tag "Auto-Enrichment" et relation
    ↓
[6] Update page Github [DB]
    ├─► Description (README si API vide)
    ├─► Language, Stars, Topics
    ├─► Last Commit, Last Sync, Sync Status
    └─► Related Videos, Related Articles (relations)
    ↓
[7] Optionnel: Apply template
    ↓
Page enrichie avec vidéos et articles liés
```

## Configuration

**Github [DB]**
- ID: `2cacdc04-12e3-81cc-a84e-fdbba086ab29`
- Data Source: `collection://2cacdc04-12e3-8182-b4f0-000b3089ad8a`

**Youtube [DB]**
- ID: `143cdc04-12e3-8030-8fb2-c2fb46f78037`
- Data Source: `collection://8a93155c-0f2e-4254-bbce-547bbbe56fd1`

**Ressources Web [DB]**
- ID: `afbf024b-2d2c-49eb-b035-99a4d495f19f`
- Data Source: `collection://b85380b8-e636-4aa9-a3dd-6496afd59a47`

**Templates [DB] ID**: `005ff73e-512d-4a51-9c43-a1a8fb17791d`

## Exemple d'exécution

```
🔧 Skill "julien-notion-github-enricher" v3.0.0 activated

Processing: leonvanzyl/autocoder
URL: https://github.com/leonvanzyl/autocoder
Repo: leonvanzyl/autocoder

[1] GitHub API Response:
    Description: (empty)
    Language: Python
    Stars: 1131
    Topics: [claude, ai, automation, coding-agent]
    Last Commit: 2026-01-15T10:30:00Z

[2] README.md fetched:
    Description extracted: "AutoCoder is a long-running autonomous coding agent that can complete complex tasks..."
    Images found: 2 (1 screenshot, 1 diagram)

[3] YouTube Search: "autocoder tutorial"
    Found 3 videos:
    ✓ Created: "AutoCoder Setup Guide" by TechChannel
    ✓ Created: "Build AI Agents with AutoCoder" by DevTutorials
    ✓ Skipped: Already exists in Youtube [DB]

[4] Article Search: "autocoder guide"
    Found 2 articles:
    ✓ Created: "Getting Started with AutoCoder" (dev.to)
    ⚠ Skipped: Ressources Web [DB] MCP unavailable

[5] Updating Notion page...
    ✓ Description (from README)
    ✓ Language → Python
    ✓ Stars → 1131
    ✓ Topics → [claude, ai, automation, coding-agent]
    ✓ Last Commit → 2026-01-15
    ✓ Last Sync → 2026-01-15
    ✓ Sync Status → Fresh
    ✓ Related Videos → 2 videos linked

Cover image URL (manual add):
    https://opengraph.githubassets.com/1/leonvanzyl/autocoder

SUCCESS: Entry enriched with 2 videos and 1 article!
```
