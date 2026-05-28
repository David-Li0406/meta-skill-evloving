---
name: content-to-multilang
description: Workflow automatisé - Du contenu source à la publication multilingue
version: 1.0.0
---

# Workflow : Contenu FR → Publication Multilingue

Ce workflow montre comment l'agence IA transforme automatiquement un contenu français en versions localisées pour plusieurs marchés.

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW CONTENU → MULTILANG (< 48h)                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   TRIGGER            TRADUCTION          ADAPTATION         PUBLICATION          │
│                                                                                  │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ CONTENU  │─────►│ TRANSLATE│──────►│  ADAPT   │──────►│ VALIDATE │         │
│   │ PUBLIÉ   │      │ PAR LANG │       │  LOCALE  │       │   i18n   │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│        │                 │                   │                  │               │
│        ▼                 ▼                   ▼                  ▼               │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ DETECT   │      │ QUALITY  │       │ CULTURAL │       │ PUBLISH  │         │
│   │ LANGUES  │      │  CHECK   │       │  CHECK   │       │ MULTI    │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│                                                                                  │
│   ~5 min             ~2-4h/lang          ~1h/lang           ~30 min             │
│                                                                                  │
│   TOTAL: 24-48h selon nombre de langues                                         │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Triggers

```yaml
triggers:
  - type: content_published
    source: cms
    conditions:
      - locale: "fr-FR"
      - status: "published"
      - multilang_enabled: true

  - type: manual
    endpoint: /api/content/translate
    params:
      - content_id: required
      - target_locales: required

  - type: scheduled
    cron: "0 6 * * 1"  # Chaque lundi 6h
    action: sync_pending_translations
```

---

## Phase 1 : Détection & Configuration (5 min)

### 1.1 Trigger automatique

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Détecter publication | content-management | editorial/publication-scheduler | Webhook CMS | Content published |
| Vérifier config i18n | content-management | localization/i18n-validator | Content | Locales config |

```json
{
  "trigger": {
    "event": "content.published",
    "content_id": "CONTENT-2025-001234",
    "source_locale": "fr-FR",
    "title": "10 Tendances SEO 2025",
    "type": "article",
    "multilang_config": {
      "enabled": true,
      "auto_translate": true,
      "target_locales": ["en-US", "de-DE", "es-ES"],
      "priority": ["en-US", "de-DE", "es-ES"]
    }
  }
}
```

### 1.2 Analyse du contenu source

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Extraire segments | content-management | localization/translation-manager | Segments list |
| Vérifier mémoire | content-management | localization/translation-manager | TM matches |

```json
{
  "source_analysis": {
    "content_id": "CONTENT-2025-001234",
    "segments": {
      "total": 145,
      "translatable": 138,
      "locked": 7
    },
    "translation_memory": {
      "100_match": 23,
      "fuzzy_match": 45,
      "new": 70
    },
    "estimated_effort": {
      "en-US": "2.5h",
      "de-DE": "3h",
      "es-ES": "3h"
    },
    "special_content": {
      "code_blocks": 3,
      "urls": 12,
      "brand_terms": 5
    }
  }
}
```

### 1.3 Création des tâches

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Créer tâches par langue | task-orchestrator | queue/queue-manager | Translation tasks |
| Définir priorités | task-orchestrator | queue/priority-adjuster | Ordered queue |

```json
{
  "translation_tasks": [
    {
      "task_id": "TRANS-2025-001-EN",
      "content_id": "CONTENT-2025-001234",
      "source": "fr-FR",
      "target": "en-US",
      "priority": 1,
      "status": "queued",
      "sla_deadline": "2025-01-11T18:00:00Z"
    },
    {
      "task_id": "TRANS-2025-001-DE",
      "content_id": "CONTENT-2025-001234",
      "source": "fr-FR",
      "target": "de-DE",
      "priority": 2,
      "status": "queued",
      "sla_deadline": "2025-01-12T12:00:00Z"
    },
    {
      "task_id": "TRANS-2025-001-ES",
      "content_id": "CONTENT-2025-001234",
      "source": "fr-FR",
      "target": "es-ES",
      "priority": 3,
      "status": "queued",
      "sla_deadline": "2025-01-12T18:00:00Z"
    }
  ]
}
```

---

## Phase 2 : Traduction (2-4h par langue)

### 2.1 Traduction assistée

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Appliquer TM | content-management | localization/translation-manager | TM applied |
| Traduire nouveaux | content-management | localization/translation-manager | Draft translation |
| Quality check | content-management | localization/translation-manager | QA report |

```json
{
  "translation": {
    "task_id": "TRANS-2025-001-EN",
    "target": "en-US",
    "progress": {
      "segments_done": 138,
      "segments_total": 138
    },
    "sources": {
      "translation_memory": 68,
      "machine_translation": 52,
      "human_review_needed": 18
    },
    "quality": {
      "score": 92,
      "issues": [
        { "type": "terminology", "segment": 45, "suggestion": "Use 'SEO trends' not 'SEO tendencies'" },
        { "type": "style", "segment": 78, "suggestion": "More natural phrasing needed" }
      ]
    }
  }
}
```

### 2.2 Traitement du glossaire

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Appliquer glossaire | content-management | localization/translation-manager | Terms applied |
| Vérifier cohérence | content-management | localization/translation-manager | Consistency check |

```json
{
  "glossary_application": {
    "terms_found": 15,
    "terms_applied": [
      { "source": "référencement naturel", "target": "organic search", "count": 8 },
      { "source": "taux de rebond", "target": "bounce rate", "count": 3 },
      { "source": "balise titre", "target": "title tag", "count": 4 }
    ],
    "new_terms_suggested": [
      { "source": "SGE", "suggested": "SGE (Search Generative Experience)", "context": "Google's AI search" }
    ]
  }
}
```

---

## Phase 3 : Adaptation Locale (1h par langue)

### 3.1 Adaptation culturelle

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Adapter formats | content-management | localization/locale-adapter | Formats adapted |
| Vérifier références | content-management | localization/locale-adapter | References check |

```json
{
  "locale_adaptation": {
    "task_id": "TRANS-2025-001-EN",
    "target": "en-US",
    "adaptations": [
      {
        "type": "date_format",
        "original": "10 janvier 2025",
        "adapted": "January 10, 2025",
        "count": 5
      },
      {
        "type": "currency",
        "original": "1 500 €",
        "adapted": "$1,650",
        "note": "Conversion applied"
      },
      {
        "type": "cultural_reference",
        "original": "comme la Ligue 1",
        "adapted": "like the Premier League",
        "note": "Sports reference localized"
      },
      {
        "type": "legal",
        "original": "RGPD",
        "adapted": "GDPR",
        "note": "Regulation name"
      }
    ]
  }
}
```

### 3.2 Adaptation SEO locale

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Rechercher keywords locaux | marketing | acquisition/seo/strategie | Local keywords |
| Adapter meta | content-management | redaction/seo-optimizer | Localized meta |

```json
{
  "seo_localization": {
    "target": "en-US",
    "keywords": {
      "primary": {
        "source": "tendances seo 2025",
        "localized": "seo trends 2025",
        "search_volume": 12400
      },
      "secondary": [
        { "localized": "google algorithm update 2025", "volume": 8100 },
        { "localized": "seo best practices 2025", "volume": 6500 }
      ]
    },
    "meta": {
      "title": "10 SEO Trends for 2025: Complete Guide for SMBs | ACME",
      "description": "Discover the 10 essential SEO trends for 2025. Practical guide with actionable tips to improve your search rankings."
    },
    "url_slug": "/blog/seo-trends-2025"
  }
}
```

---

## Phase 4 : Validation i18n (30 min par langue)

### 4.1 Validation technique

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Valider structure | content-management | localization/i18n-validator | Structure OK |
| Vérifier encoding | content-management | localization/i18n-validator | UTF-8 OK |
| Tester liens | content-management | localization/i18n-validator | Links OK |

```json
{
  "i18n_validation": {
    "task_id": "TRANS-2025-001-EN",
    "target": "en-US",
    "checks": {
      "encoding": { "status": "passed", "charset": "UTF-8" },
      "structure": { "status": "passed", "segments_match": true },
      "placeholders": { "status": "passed", "count": 12, "preserved": 12 },
      "links": { "status": "passed", "total": 15, "localized": 8, "external": 7 },
      "images": { "status": "passed", "alt_texts_translated": true },
      "special_chars": { "status": "passed", "issues": 0 }
    },
    "overall": "PASSED",
    "ready_for_review": true
  }
}
```

### 4.2 Review humain (si configuré)

```
🔔 NOTIFICATION → Slack #translations

Traduction prête pour review:
- Contenu: 10 Tendances SEO 2025
- Langue: 🇺🇸 Anglais (en-US)
- Score qualité: 92/100
- Segments à vérifier: 18/138

[Prévisualiser] [Approuver] [Demander corrections]
```

---

## Phase 5 : Publication Multi-locale (30 min)

### 5.1 Publication synchronisée

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Scheduler publications | content-management | editorial/publication-scheduler | Scheduled |
| Configurer hreflang | marketing | acquisition/seo/international | Hreflang tags |
| Publier | content-management | editorial/publication-scheduler | Published |

```json
{
  "multilang_publication": {
    "content_id": "CONTENT-2025-001234",
    "publications": [
      {
        "locale": "fr-FR",
        "url": "https://acme.fr/blog/tendances-seo-2025",
        "status": "published",
        "published_at": "2025-01-12T10:00:00+01:00"
      },
      {
        "locale": "en-US",
        "url": "https://acme.com/blog/seo-trends-2025",
        "status": "published",
        "published_at": "2025-01-12T15:00:00+01:00"
      },
      {
        "locale": "de-DE",
        "url": "https://acme.de/blog/seo-trends-2025",
        "status": "published",
        "published_at": "2025-01-12T16:00:00+01:00"
      },
      {
        "locale": "es-ES",
        "url": "https://acme.es/blog/tendencias-seo-2025",
        "status": "published",
        "published_at": "2025-01-12T17:00:00+01:00"
      }
    ],
    "hreflang": {
      "configured": true,
      "tags_count": 4,
      "x_default": "en-US"
    }
  }
}
```

### 5.2 Synchronisation Search Console

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Update sitemaps | marketing | acquisition/seo/technique | Sitemaps updated |
| Notify Search Console | marketing | acquisition/seo/technique | Indexed |

```json
{
  "search_console_sync": {
    "sitemaps_updated": [
      "https://acme.fr/sitemap.xml",
      "https://acme.com/sitemap.xml",
      "https://acme.de/sitemap.xml",
      "https://acme.es/sitemap.xml"
    ],
    "urls_submitted": 4,
    "hreflang_validated": true
  }
}
```

### 5.3 Rapport final

```
📧 Rapport de publication multilingue

Contenu: 10 Tendances SEO 2025
Langues publiées: 4/4 ✅

| Langue | URL | Statut |
|--------|-----|--------|
| 🇫🇷 FR | acme.fr/blog/tendances-seo-2025 | ✅ Published |
| 🇺🇸 EN | acme.com/blog/seo-trends-2025 | ✅ Published |
| 🇩🇪 DE | acme.de/blog/seo-trends-2025 | ✅ Published |
| 🇪🇸 ES | acme.es/blog/tendencias-seo-2025 | ✅ Published |

Hreflang: ✅ Configuré
Sitemaps: ✅ Mis à jour
Search Console: ✅ Notifié

Temps total: 28h
Segments traduits: 414 (138 × 3 langues)
Réutilisation TM: 49%
```

---

## Métriques du Workflow

| Métrique | Cible | Mesuré |
|----------|-------|--------|
| Temps par langue | < 8h | ~6h |
| Temps humain | < 30min/lang | ~20min |
| Taux réutilisation TM | > 40% | 49% |
| Score qualité | > 90 | 92 |
| Erreurs i18n | 0 | 0 |

## Points d'Escalade Humaine

| Condition | Action |
|-----------|--------|
| Contenu légal/médical | Traduction certifiée |
| Nouvelle langue | Setup initial requis |
| Score qualité < 85 | Review obligatoire |
| Termes non glossarisés | Validation terminologique |
| Marché sensible | Validation culturelle |

## Références

- [content-management/SKILL.md](../SKILL.md)
- [marketing/acquisition/seo/international](../../marketing/agents/acquisition/seo/international/)
