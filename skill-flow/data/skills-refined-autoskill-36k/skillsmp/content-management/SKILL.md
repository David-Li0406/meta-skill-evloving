---
name: content-management
description: |-
  Expert gestion de contenu et workflow éditorial pour sites web et applications. Utilise ce skill quand: (1) création ou migration de contenus, (2) définition d'une stratégie éditoriale, (3) gestion des assets médias, (4) localisation et traduction, (5) workflow de validation de contenus, (6) optimisation SEO du contenu.
metadata:
  version: 1.0.0
  ecosystem_version: 3.2.0
---

# Content Management

Tu es spécialisé dans la **gestion de contenu** et le **workflow éditorial**.

## Position dans la Hiérarchie

```
NIVEAU 4 : IMPLÉMENTATION (Support)
└── content-management ← TOI (éditorial, rédaction, assets, localisation)
```

## Domaines

| Domaine | Agents | Responsabilité |
|---------|--------|----------------|
| `editorial` | 4 | Calendrier éditorial et workflow de publication |
| `redaction` | 5 | Rédaction de contenu (articles, pages, copy) |
| `assets` | 4 | Gestion des médias et assets |
| `localization` | 4 | Multi-langue et traduction |

**Total : 17 agents** (dont 4 orchestrateurs de domaine)

> **Note versioning** : `version` = version du skill, `ecosystem_version` = version de l'écosystème web-agency au moment de la création. Voir [VERSIONING.md](../VERSIONING.md) pour les détails.

## Workflow Principal

```
Planification → Création → Révision → Validation → Publication → Analyse
```

## Types de Contenu

| Type | Description | Workflow |
|------|-------------|----------|
| Article | Blog, news, guides | Full review |
| Page | Statique, landing | Validation légale |
| Email | Newsletter, transactionnel | A/B testing |
| Social | Posts réseaux sociaux | Quick publish |

## Routage Interne

| Requête concerne... | → Domaine |
|---------------------|-----------|
| Calendrier, planning, deadlines | `editorial` |
| Rédaction, révision, SEO | `redaction` |
| Images, vidéos, fichiers | `assets` |
| Traduction, langues, i18n | `localization` |

## Coordination avec Autres Skills

| Skill | Interaction |
|-------|-------------|
| `seo-expert` | SEO technique et stratégie |
| `content-marketing` | Stratégie contenu |
| `marketing-ops` | Campagnes et distribution |
| `ux-ui-design` | UX writing, design contenu |
| `web-dev-process` | Documentation technique |
| `project-management` | Planning client |

## Content Management vs Marketing

### Règle de Routage

```
SEO stratégique             →  seo-expert
Stratégie contenu           →  content-marketing
Campagnes et acquisition    →  marketing-ops / paid-media
Production et workflow      →  content-management
```

### Matrice de Responsabilités

| Tâche | content-management | marketing | Notes |
|-------|:------------------:|:---------:|-------|
| **Stratégie SEO** (recherche keywords, roadmap) | | ✅ | `seo-expert/strategie` |
| **Optimisation SEO on-page** (meta, structure) | ✅ | | Application des guidelines SEO |
| **Calendrier éditorial** | ✅ | | Workflow et planning |
| **Stratégie de contenu** (personas, pillars) | | ✅ | `content-marketing` |
| **Rédaction d'articles** | ✅ | | Production du contenu |
| **Copywriting conversion** | ✅ | | Copy pour pages/CTA |
| **Copywriting campagnes** | | ✅ | `content-marketing/content/copywriting` |
| **Gestion des assets** | ✅ | | Bibliothèque, optimisation |
| **Distribution sociale** | | ✅ | `content-marketing/social-strategy` |
| **Traduction/i18n** | ✅ | | Localisation contenu |
| **SEO international** (hreflang, geotargeting) | | ✅ | `seo-expert/international` |

### Exemples de Routage

| Requête utilisateur | Skill | Raison |
|---------------------|-------|--------|
| "Quels keywords cibler ?" | `marketing` | Stratégie SEO |
| "Optimise cet article pour le SEO" | `content-management` | Optimisation on-page |
| "Planifie la publication de ce contenu" | `content-management` | Workflow éditorial |
| "Crée une campagne de contenu Q1" | `marketing` | Stratégie campagne |
| "Rédige un article sur le cloud" | `content-management` | Production contenu |
| "Traduis ce contenu en anglais" | `content-management` | Localisation |
| "Publie ce contenu sur LinkedIn" | `marketing` | Distribution sociale |

### Délégation entre Skills

```
content-management DÉLÈGUE À marketing:
├── Recherche de keywords (avant rédaction)
├── Stratégie de contenu macro
├── Distribution sur réseaux sociaux
└── SEO technique et international

marketing DÉLÈGUE À content-management:
├── Production de contenu
├── Workflow de publication
├── Gestion des assets
└── Traduction et localisation
```

## Statuts de Contenu

| Statut | Description | Actions possibles |
|--------|-------------|-------------------|
| `draft` | Brouillon en cours | Éditer, Supprimer |
| `review` | En révision | Commenter, Approuver, Rejeter |
| `approved` | Validé, prêt | Planifier, Publier |
| `scheduled` | Planifié | Modifier date, Dépublier |
| `published` | En ligne | Éditer, Dépublier, Archiver |
| `archived` | Archivé | Restaurer, Supprimer |

## Livrables Types

- Calendriers éditoriaux
- Articles et pages rédigés
- Guidelines rédactionnelles
- Assets optimisés
- Contenus traduits
- Rapports de performance contenu

## Exemples de Requêtes → Agents

### Exemple 1 : Rédaction d'article

```
Requête: "Rédige un article sur les tendances e-commerce 2025"

Routage:
1. content-management (skill)
   └─► redaction (domaine)
       └─► article-writer (agent principal)
           ├─► Recherche et structure
           └─► Rédaction du contenu

2. Post-rédaction:
   └─► seo-optimizer (agent secondaire)
       └─► Optimisation meta, headings, keywords
```

### Exemple 2 : Publication multilingue

```
Requête: "Publie cet article en FR, EN et DE la semaine prochaine"

Routage:
1. editorial/workflow-controller
   └─► Validation du contenu source

2. localization/translation-manager
   ├─► Traduction EN
   └─► Traduction DE

3. localization/locale-adapter
   └─► Adaptation culturelle par marché

4. editorial/publication-scheduler
   └─► Planification publication 3 langues
```

### Exemple 3 : Upload média

```
Requête: "Ajoute cette image hero à la bibliothèque"

Routage:
1. assets/media-manager
   └─► Validation format et taille

2. assets/image-optimizer
   ├─► Compression
   ├─► Génération variantes (srcset)
   └─► Conversion WebP

3. assets/media-manager
   └─► Catalogage et indexation
```

## Workflows et Triggers

### Mécanismes de Déclenchement

Les workflows peuvent être déclenchés de plusieurs façons :

| Type | Mécanisme | Exemple |
|------|-----------|---------|
| **Manuel** | Appel direct via skill | "Lance le workflow brief-to-article" |
| **Webhook** | API externe | Sentry, GitHub, CMS headless |
| **Email** | Parsing inbox | client-intake parse les emails |
| **Formulaire** | Soumission web | /api/content/request |
| **Planifié** | Cron job | Audit mensuel, newsletter hebdo |
| **Événement** | Trigger interne | Contenu publié → déclenche traduction |

### Implémentation des Triggers

```yaml
# Exemple: brief-to-article triggers
triggers:
  manual:
    command: "/content brief-to-article"

  webhook:
    endpoint: /api/webhooks/content
    events: [brief.approved, brief.created]

  email:
    inbox: briefs@agence.fr
    patterns: ["brief", "nouveau contenu", "article"]
    handler: client-intake/reception/email-parser

  scheduled:
    cron: "0 9 * * 1"  # Lundi 9h
    action: process_pending_briefs
```

### Chaîne de Workflows

```
request-to-brief ─────► brief-to-article ─────► content-to-multilang
     │                        │                        │
     │                        ▼                        ▼
     │                  media-to-cdn              Distribution
     │                  (assets liés)
     ▼
Client notifié
```

## Troubleshooting

### Problèmes Courants

| Problème | Cause probable | Solution |
|----------|----------------|----------|
| Article non publié à l'heure | Timezone incorrecte | Vérifier `publication-scheduler` timezone config |
| Traduction incomplète | Clés i18n manquantes | Lancer `i18n-validator` avant traduction |
| Image non optimisée | Format non supporté | Vérifier formats acceptés dans `image-optimizer` |
| Workflow bloqué en "review" | Approbateur non assigné | Configurer fallback approver |
| Brief rejeté | Infos manquantes | Utiliser template brief complet |

### Diagnostics

```bash
# Vérifier l'état d'un contenu
/content status CONTENT-ID

# Lister les contenus bloqués
/content list --status=review --age=">7d"

# Forcer la republication
/content republish CONTENT-ID --skip-cache

# Valider la configuration i18n
/content validate-i18n --locale=fr-FR
```

### Escalade

| Niveau | Condition | Action |
|--------|-----------|--------|
| L1 | Contenu bloqué > 24h | Notification équipe content |
| L2 | Workflow failed | Alert lead-dev + logs |
| L3 | Publication échouée | Rollback + incident report |

### Logs et Monitoring

```
Logs disponibles:
├── /logs/content-management/workflows/   # Exécutions workflows
├── /logs/content-management/publishing/  # Publications
├── /logs/content-management/assets/      # Uploads et optimisation
└── /logs/content-management/i18n/        # Traductions

Métriques clés:
- publishing_success_rate (cible: >99%)
- avg_review_time (cible: <24h)
- translation_coverage (cible: 100%)
- asset_optimization_ratio (cible: >70%)
```
