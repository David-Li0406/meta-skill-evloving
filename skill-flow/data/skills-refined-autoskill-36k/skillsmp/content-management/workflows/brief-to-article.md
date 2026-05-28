---
name: brief-to-article
description: Workflow automatisé - Du brief éditorial à l'article publié
version: 1.0.0
---

# Workflow : Brief Éditorial → Article Publié

Ce workflow montre comment l'agence IA transforme automatiquement un brief éditorial en article optimisé et publié.

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW BRIEF → ARTICLE (< 8h)                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   INTAKE             CRÉATION            OPTIMISATION        PUBLICATION         │
│                                                                                  │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │  BRIEF   │─────►│ RÉDACTION│──────►│   SEO    │──────►│ PLANNING │         │
│   │  REÇU    │      │ ARTICLE  │       │ OPTIMIZE │       │ ÉDITORIAL│         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│        │                 │                   │                  │               │
│        ▼                 ▼                   ▼                  ▼               │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ QUALIF   │      │  ASSETS  │       │ RÉVISION │       │ PUBLISH  │         │
│   │ ÉDITORIAL│      │  IMAGES  │       │ WORKFLOW │       │ + SOCIAL │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│                                                                                  │
│   ~30 min            ~2-4h               ~1h                ~30 min             │
│                                                                                  │
│   TOTAL: 4-6h (automatisé) + validation humaine (~1h)                           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Triggers

```yaml
triggers:
  - type: email
    patterns:
      - "brief article"
      - "rédiger un article"
      - "nouveau contenu"
      - "besoin d'un article"
    from: ["*@client.com", "marketing@*"]

  - type: form
    endpoint: /api/content/brief

  - type: webhook
    source: notion
    events: [page.created]
    filters:
      database: "Briefs Éditoriaux"

  - type: slack
    channels: [content-team]
    patterns: ["@content", "nouveau brief"]
```

---

## Phase 1 : Intake & Qualification (30 min)

### 1.1 Réception du brief

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Parser brief | client-intake | reception/email-parser | Email/Form | Structured brief |
| Extraire pièces jointes | client-intake | reception/attachment-processor | Attachments | References, images |

```json
{
  "brief_parsed": {
    "source": "email",
    "from": "marketing@acme.fr",
    "subject": "Brief - Article SEO 2025",
    "body": "...",
    "attachments": [
      { "name": "sources-seo.pdf", "type": "reference" },
      { "name": "logo-acme.png", "type": "asset" }
    ]
  }
}
```

### 1.2 Qualification éditoriale

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Classifier type contenu | client-intake | qualification/intent-classifier | Brief | Type: ARTICLE |
| Évaluer complexité | client-intake | qualification/complexity-assessor | Brief | Effort: M |
| Détecter urgence | client-intake | qualification/urgency-detector | Context | Priority: P3 |

```json
{
  "qualification": {
    "content_type": "ARTICLE",
    "article_type": "how-to",
    "target_length": 2000,
    "complexity": {
      "research_needed": "medium",
      "technical_level": "intermediate",
      "estimated_hours": 4
    },
    "priority": "P3",
    "deadline": "2025-01-15"
  }
}
```

### 1.3 Extraction des requirements

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Extraire sujet | content-management | redaction/orchestrator | Brief | Topic structured |
| Identifier audience | content-management | redaction/article-writer | Brief | Persona |
| Mapper keywords | content-management | redaction/seo-optimizer | Brief | Keywords |

```json
{
  "content_requirements": {
    "topic": "Tendances SEO 2025",
    "angle": "Guide pratique pour PME",
    "audience": {
      "persona": "Marketing Manager PME",
      "level": "Intermédiaire",
      "pain_points": ["Manque de visibilité", "Budget limité"]
    },
    "seo": {
      "primary_keyword": "tendances seo 2025",
      "secondary_keywords": ["seo 2025", "référencement naturel", "google update"],
      "search_intent": "informational"
    },
    "tone": "Professionnel, accessible",
    "cta": "Télécharger checklist SEO"
  }
}
```

### 1.4 Planification éditoriale

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Vérifier calendrier | content-management | editorial/calendar-manager | Slot disponible |
| Créer entrée | content-management | editorial/calendar-manager | CAL-2025-001 |

```json
{
  "calendar_entry": {
    "id": "CAL-2025-001",
    "content_id": "CONTENT-2025-001234",
    "dates": {
      "brief_received": "2025-01-10T09:00:00Z",
      "draft_due": "2025-01-10T17:00:00Z",
      "review_due": "2025-01-11T12:00:00Z",
      "publish_date": "2025-01-12T10:00:00Z"
    },
    "status": "in_progress"
  }
}
```

---

## Phase 2 : Création (2-4h)

### 2.1 Recherche & Outline

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Rechercher sources | content-management | redaction/article-writer | Sources list |
| Créer outline | content-management | redaction/article-writer | Article structure |

```markdown
## Outline - Tendances SEO 2025

### Introduction (150 mots)
- Hook: L'évolution constante de Google
- Promesse: 10 tendances à maîtriser

### 1. L'IA et la recherche (300 mots)
- Google SGE
- Content AI-friendly

### 2. Core Web Vitals 2.0 (250 mots)
- INP remplace FID
- Nouveaux seuils

### 3. E-E-A-T renforcé (300 mots)
- Experience ajoutée
- Preuves d'expertise

[... autres sections ...]

### Conclusion (150 mots)
- Récap
- CTA: Checklist

### FAQ (200 mots)
- 3-4 questions fréquentes
```

### 2.2 Rédaction

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Rédiger article | content-management | redaction/article-writer | Draft complet |
| Générer meta | content-management | redaction/seo-optimizer | Title + Meta desc |

```json
{
  "draft": {
    "content_id": "CONTENT-2025-001234",
    "version": "1.0.0",
    "word_count": 2150,
    "reading_time": "9 min",
    "sections": 8,
    "status": "draft",
    "meta": {
      "title": "10 Tendances SEO 2025 : Guide Complet pour PME | ACME",
      "description": "Découvrez les 10 tendances SEO incontournables de 2025. Guide pratique avec conseils actionnables pour améliorer votre référencement.",
      "og_image": "/images/seo-2025-cover.jpg"
    }
  }
}
```

### 2.3 Assets visuels

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Identifier besoins images | content-management | assets/media-manager | Image list |
| Optimiser images | content-management | assets/image-optimizer | Optimized assets |

```json
{
  "assets": {
    "content_id": "CONTENT-2025-001234",
    "images": [
      {
        "id": "IMG-001",
        "type": "hero",
        "alt": "Illustration tendances SEO 2025",
        "sizes": ["400w", "800w", "1200w"],
        "format": "webp",
        "size_kb": 85
      },
      {
        "id": "IMG-002",
        "type": "infographic",
        "alt": "Schéma Core Web Vitals 2025",
        "sizes": ["600w", "1200w"],
        "format": "webp",
        "size_kb": 120
      }
    ],
    "total_size_kb": 205
  }
}
```

---

## Phase 3 : Optimisation & Révision (1h)

### 3.1 Optimisation SEO

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Analyser SEO | content-management | redaction/seo-optimizer | SEO report |
| Optimiser contenu | content-management | redaction/seo-optimizer | Optimized content |

```json
{
  "seo_analysis": {
    "content_id": "CONTENT-2025-001234",
    "score": 87,
    "checks": {
      "keyword_density": { "status": "ok", "value": 1.8 },
      "title_tag": { "status": "ok", "length": 58 },
      "meta_description": { "status": "ok", "length": 152 },
      "headings_structure": { "status": "ok", "h2_count": 10 },
      "internal_links": { "status": "warning", "count": 2, "recommended": 4 },
      "image_alt_texts": { "status": "ok", "coverage": 100 },
      "readability": { "status": "ok", "flesch_score": 65 }
    },
    "suggestions": [
      "Ajouter 2 liens internes supplémentaires",
      "Considérer un FAQ schema markup"
    ]
  }
}
```

### 3.2 Workflow de révision

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Soumettre révision | content-management | editorial/workflow-controller | Status: REVIEW |
| Checklist validation | content-management | editorial/workflow-controller | Checklist |

```json
{
  "review": {
    "content_id": "CONTENT-2025-001234",
    "status": "review",
    "checklist": {
      "spelling_grammar": true,
      "facts_verified": true,
      "links_working": true,
      "images_optimized": true,
      "seo_score_above_80": true,
      "cta_present": true,
      "mobile_preview": true
    },
    "reviewer": "editor-001",
    "comments": "Excellent article, quelques ajustements mineurs sur la section 3"
  }
}
```

### 3.3 Validation humaine

```
🔔 NOTIFICATION → Slack #content-review

Nouvel article prêt pour validation:
- Titre: 10 Tendances SEO 2025 : Guide Complet pour PME
- Longueur: 2150 mots (9 min lecture)
- Score SEO: 87/100
- Auteur: content-bot
- Reviewer: @editor

[Prévisualiser] [Approuver] [Demander modifications]
```

---

## Phase 4 : Publication (30 min)

### 4.1 Planification publication

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Scheduler publication | content-management | editorial/publication-scheduler | Scheduled |
| Préparer distribution | marketing | content/social-media-content | Social posts |

```json
{
  "publication": {
    "content_id": "CONTENT-2025-001234",
    "schedule": {
      "publish_at": "2025-01-12T10:00:00+01:00",
      "timezone": "Europe/Paris",
      "channels": ["website", "newsletter", "linkedin", "twitter"]
    },
    "social_posts": {
      "linkedin": {
        "text": "🚀 Les 10 tendances SEO qui vont marquer 2025...",
        "scheduled": "2025-01-12T10:30:00+01:00"
      },
      "twitter": {
        "text": "Le SEO évolue en 2025 ! Découvrez les 10 tendances clés 🧵",
        "scheduled": "2025-01-12T11:00:00+01:00"
      }
    }
  }
}
```

### 4.2 Mise en ligne

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Publier | content-management | editorial/publication-scheduler | PUBLISHED |
| Notifier sitemap | marketing | acquisition/seo/technique | Sitemap updated |
| Distribuer social | marketing | content/social-media-content | Posts published |

```json
{
  "published": {
    "content_id": "CONTENT-2025-001234",
    "url": "https://acme.fr/blog/tendances-seo-2025",
    "published_at": "2025-01-12T10:00:00+01:00",
    "notifications": {
      "sitemap": "updated",
      "search_console": "submitted",
      "newsletter": "scheduled_next_batch",
      "social": {
        "linkedin": "published",
        "twitter": "published"
      }
    }
  }
}
```

### 4.3 Confirmation

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Notifier demandeur | client-intake | response/status-notifier | Email confirmation |
| Logger audit | task-orchestrator | tracking/audit-logger | Audit trail |

```
📧 Email envoyé à marketing@acme.fr:

Objet: ✅ Article publié - 10 Tendances SEO 2025

Bonjour,

Votre article "10 Tendances SEO 2025 : Guide Complet pour PME"
a été publié avec succès.

📊 Résumé:
- URL: https://acme.fr/blog/tendances-seo-2025
- Longueur: 2150 mots
- Score SEO: 87/100
- Distribution: Blog, LinkedIn, Twitter

📈 Suivi disponible dans votre dashboard.

Cordialement,
L'équipe Content
```

---

## Métriques du Workflow

| Métrique | Cible | Mesuré |
|----------|-------|--------|
| Temps total | < 8h | ~5h |
| Temps humain | < 1h | ~45min (révision) |
| Taux d'automatisation | > 80% | 85% |
| Score SEO moyen | > 80 | 87 |
| Taux de publication | > 95% | 98% |

## Points d'Escalade Humaine

| Condition | Action |
|-----------|--------|
| Sujet technique complexe | Review expert |
| Contenu légal/médical | Validation juridique |
| Brief incomplet | Demande clarification |
| Score SEO < 70 | Optimisation manuelle |
| Deadline < 4h | Fast-track + alert |

## Références

- [content-management/SKILL.md](../SKILL.md)
- [client-intake/SKILL.md](../../client-intake/SKILL.md)
- [marketing/SKILL.md](../../marketing/SKILL.md)
