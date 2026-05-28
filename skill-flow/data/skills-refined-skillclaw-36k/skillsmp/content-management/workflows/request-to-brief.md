---
name: request-to-brief
description: Workflow automatisé - De la demande client ou analyse au brief éditorial structuré
version: 1.0.0
---

# Workflow : Demande/Analyse → Brief Éditorial

Ce workflow montre comment l'agence IA transforme automatiquement une demande client vague ou une analyse de données en brief éditorial actionnable.

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW REQUEST → BRIEF (< 4h)                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   INPUT              ANALYSE             ENRICHMENT         OUTPUT               │
│                                                                                  │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ DEMANDE  │─────►│  SEO     │──────►│ PERSONA  │──────►│  BRIEF   │         │
│   │ CLIENT   │      │ RESEARCH │       │ MAPPING  │       │ COMPLET  │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│        │                 │                   │                  │               │
│        ▼                 ▼                   ▼                  ▼               │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ ANALYSE  │      │ CONCUR-  │       │ CONTENT  │       │ CALENDAR │         │
│   │ DONNÉES  │      │ RENCE    │       │ STRATEGY │       │ PLANNING │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│                                                                                  │
│   ~30 min            ~1-2h               ~1h                ~30 min             │
│                                                                                  │
│   TOTAL: 2-4h (90% automatisé) + validation humaine                             │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Sources d'Input

```yaml
sources:
  # 1. Demande client directe
  - type: email
    patterns:
      - "besoin de contenu"
      - "articles sur"
      - "stratégie éditoriale"
      - "calendrier de publication"
    output: client_request

  # 2. Analyse SEO automatique
  - type: scheduled
    cron: "0 8 1 * *"  # 1er du mois
    action: monthly_seo_opportunities
    output: seo_analysis

  # 3. Données analytics
  - type: webhook
    source: google_analytics
    events: [content_gap_detected]
    output: analytics_insight

  # 4. Veille concurrentielle
  - type: webhook
    source: semrush
    events: [competitor_content_alert]
    output: competitive_intel

  # 5. Demande interne
  - type: form
    endpoint: /api/content/request-brief
    output: internal_request
```

---

## Scénario A : Demande Client → Brief

### A.1 Réception de la demande (10 min)

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Parser demande | client-intake | reception/email-parser | Email client | Structured request |
| Classifier intent | client-intake | qualification/intent-classifier | Request | Type: CONTENT_STRATEGY |
| Extraire besoins | client-intake | extraction/requirements-extractor | Request | Requirements |

```json
{
  "client_request": {
    "id": "REQ-2025-001234",
    "from": "marketing@acme.fr",
    "type": "CONTENT_STRATEGY",
    "raw_request": "Nous voudrions créer du contenu autour de notre nouvelle offre cloud. Cible: DSI de PME. Budget: 10 articles. Deadline: Q1 2025.",
    "extracted": {
      "topic": "offre cloud",
      "audience": "DSI PME",
      "volume": "10 articles",
      "deadline": "Q1 2025",
      "constraints": [],
      "goals_mentioned": ["visibilité", "leads"]
    }
  }
}
```

### A.2 Qualification approfondie (20 min)

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Analyser secteur | client-intake | qualification/complexity-assessor | Industry context |
| Évaluer concurrence | marketing | strategie/market-analysis | Competitive landscape |
| Identifier gaps | marketing | acquisition/seo/strategie | Content gaps |

```json
{
  "qualification": {
    "sector": {
      "industry": "Cloud Computing / SaaS",
      "market_size": "Large",
      "content_saturation": "High"
    },
    "competitive_landscape": {
      "main_competitors": ["OVH", "Scaleway", "AWS"],
      "content_leaders": ["AWS Blog", "Google Cloud Blog"],
      "differentiation_opportunities": [
        "Focus PME française",
        "Souveraineté données",
        "Support en français"
      ]
    },
    "audience_size": {
      "dsi_pme_france": "~45,000",
      "reachable_online": "~70%"
    }
  }
}
```

---

## Scénario B : Analyse SEO → Brief

### B.1 Analyse des opportunités (1h)

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Audit keywords | marketing | acquisition/seo/strategie/opportunites-keywords | Keyword opportunities |
| Analyser SERP | marketing | acquisition/seo/strategie/analyse-concurrentielle | SERP analysis |
| Identifier gaps | marketing | acquisition/seo/strategie/audit-global | Content gaps |

```json
{
  "seo_analysis": {
    "source": "monthly_audit",
    "date": "2025-01-01",
    "opportunities": [
      {
        "keyword": "migration cloud pme",
        "volume": 1200,
        "difficulty": 42,
        "current_position": null,
        "opportunity_score": 85,
        "content_type": "guide",
        "estimated_traffic": 450
      },
      {
        "keyword": "cloud souverain france",
        "volume": 880,
        "difficulty": 38,
        "current_position": 45,
        "opportunity_score": 78,
        "content_type": "comparison",
        "estimated_traffic": 320
      },
      {
        "keyword": "cout hebergement cloud",
        "volume": 2400,
        "difficulty": 55,
        "current_position": null,
        "opportunity_score": 72,
        "content_type": "calculator/tool",
        "estimated_traffic": 600
      }
    ],
    "gaps_vs_competitors": [
      "Pas de contenu sur la migration depuis on-premise",
      "Aucun comparatif avec AWS/Azure",
      "Manque de case studies PME"
    ]
  }
}
```

### B.2 Priorisation (30 min)

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Scorer opportunités | marketing | acquisition/seo/strategie/roadmap-seo | Prioritized list |
| Mapper au funnel | marketing | strategie/objectifs-marketing | Funnel mapping |

```json
{
  "prioritization": {
    "scoring_criteria": {
      "search_volume": 0.25,
      "difficulty_inverse": 0.20,
      "business_relevance": 0.30,
      "competition_gap": 0.25
    },
    "prioritized_topics": [
      {
        "rank": 1,
        "topic": "Guide migration cloud PME",
        "score": 92,
        "funnel_stage": "TOFU",
        "format": "guide longform",
        "urgency": "high"
      },
      {
        "rank": 2,
        "topic": "Cloud souverain: comparatif solutions françaises",
        "score": 87,
        "funnel_stage": "MOFU",
        "format": "comparison",
        "urgency": "high"
      },
      {
        "rank": 3,
        "topic": "Calculateur coût cloud",
        "score": 82,
        "funnel_stage": "MOFU",
        "format": "interactive tool",
        "urgency": "medium"
      }
    ]
  }
}
```

---

## Phase 2 : Enrichissement (1-2h)

### 2.1 Recherche approfondie

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Rechercher sources | content-management | redaction/article-writer | Sources list |
| Analyser tendances | marketing | strategie/market-analysis | Trends |
| Collecter data | marketing | analytics/kpi-tracking | Supporting data |

```json
{
  "research": {
    "topic": "migration cloud pme",
    "sources": {
      "industry_reports": [
        "Gartner Cloud Adoption Report 2024",
        "Markess PME Cloud Study"
      ],
      "competitor_content": [
        { "url": "ovh.com/guide-migration", "word_count": 3500, "backlinks": 45 },
        { "url": "scaleway.com/cloud-pme", "word_count": 2200, "backlinks": 28 }
      ],
      "expert_quotes": [
        { "source": "LinkedIn", "expert": "Jean Dupont, CTO @TechPME" }
      ]
    },
    "trends": {
      "rising": ["FinOps", "cloud hybride", "edge computing"],
      "stable": ["sécurité", "RGPD", "sauvegarde"],
      "declining": ["cloud privé on-premise"]
    },
    "data_points": [
      "72% des PME prévoient d'augmenter leur budget cloud en 2025",
      "Coût moyen migration: 15-50k€ pour PME 50-200 salariés",
      "Délai moyen: 3-6 mois"
    ]
  }
}
```

### 2.2 Mapping persona

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Définir persona | direction-marketing | positionnement/persona-builder | Detailed persona |
| Mapper pain points | direction-marketing | positionnement/persona-builder | Pain points |
| Identifier triggers | direction-marketing | positionnement/persona-builder | Decision triggers |

```json
{
  "persona": {
    "name": "Pierre, DSI de PME",
    "demographics": {
      "role": "DSI / Responsable IT",
      "company_size": "50-200 salariés",
      "industry": "Services, Industrie, Commerce",
      "age_range": "35-50"
    },
    "pain_points": [
      "Infrastructure vieillissante coûteuse",
      "Difficulté à recruter des talents IT",
      "Pression pour réduire les coûts",
      "Inquiétude sécurité/RGPD"
    ],
    "goals": [
      "Moderniser le SI sans risque",
      "Réduire les coûts opérationnels",
      "Améliorer l'agilité de l'entreprise"
    ],
    "decision_triggers": [
      "Incident majeur sur infra actuelle",
      "Fin de support d'un système",
      "Croissance rapide de l'entreprise",
      "Pression de la direction générale"
    ],
    "content_preferences": {
      "formats": ["guides pratiques", "cas clients", "comparatifs"],
      "tone": "expert mais accessible",
      "length": "2000-4000 mots",
      "proof_points": ["ROI chiffré", "témoignages pairs", "certifications"]
    }
  }
}
```

### 2.3 Stratégie de contenu

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Définir angles | content-management | redaction/orchestrator | Content angles |
| Mapper au parcours | marketing | strategie/objectifs-marketing | Funnel content |
| Définir KPIs | marketing | analytics/kpi-tracking | Success metrics |

```json
{
  "content_strategy": {
    "theme": "Migration Cloud pour PME",
    "positioning": "Le partenaire cloud souverain des PME françaises",
    "content_pillars": [
      {
        "pillar": "Éducation",
        "goal": "Awareness",
        "topics": ["Qu'est-ce que le cloud?", "Bénéfices cloud PME", "Mythes cloud"]
      },
      {
        "pillar": "Évaluation",
        "goal": "Consideration",
        "topics": ["Guide migration", "Comparatifs", "Calculateur coûts"]
      },
      {
        "pillar": "Validation",
        "goal": "Decision",
        "topics": ["Case studies", "ROI prouvé", "Sécurité garanties"]
      }
    ],
    "kpis": {
      "traffic": "+50% organic traffic sur /cloud",
      "leads": "20 MQL/mois depuis contenu",
      "rankings": "Top 10 sur 5 keywords cibles"
    }
  }
}
```

---

## Phase 3 : Génération du Brief (30 min)

### 3.1 Compilation brief structuré

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Générer brief | content-management | redaction/article-writer | Complete brief |
| Valider structure | content-management | editorial/workflow-controller | Validated |

```markdown
# Brief Éditorial - Guide Migration Cloud PME

## Informations Générales

| Champ | Valeur |
|-------|--------|
| ID Brief | BRIEF-2025-001234 |
| Date création | 2025-01-10 |
| Demandeur | marketing@acme.fr |
| Priorité | Haute |
| Deadline contenu | 2025-01-25 |

## Contexte & Objectifs

### Contexte
ACME lance une nouvelle offre cloud ciblant les PME françaises (50-200 salariés).
Le marché est concurrentiel mais il existe des opportunités sur le segment
"cloud souverain" et "migration accompagnée".

### Objectifs business
1. Générer 20 MQL/mois via contenu organique
2. Positionner ACME comme expert cloud PME
3. Supporter le lancement offre Q1 2025

### Objectifs SEO
- Keyword principal: "migration cloud pme" (1200 vol, KD 42)
- Keywords secondaires: "cloud souverain france", "cout hebergement cloud"
- Objectif: Top 10 en 3 mois

## Audience Cible

### Persona principal
**Pierre, 42 ans, DSI PME industrielle (120 salariés)**

**Pain points:**
- Infrastructure vieillissante coûteuse à maintenir
- Difficulté à recruter des profils IT qualifiés
- Pression DG pour réduire les coûts IT de 20%
- Inquiétudes sur la sécurité et le RGPD

**Objectifs:**
- Moderniser le SI sans prendre de risques
- Réduire les coûts opérationnels
- Libérer du temps pour les projets stratégiques

**Déclencheurs de décision:**
- Incident majeur sur l'infra actuelle
- Fin de support Windows Server
- Croissance rapide de l'entreprise

### Préférences contenu
- Format: Guide pratique, actionnable
- Longueur: 3000-4000 mots
- Ton: Expert mais accessible (pas de jargon excessif)
- Preuves: ROI chiffrés, témoignages de pairs, certifications

## Spécifications Contenu

### Type de contenu
Guide pratique longform (pillar content)

### Titre de travail
"Migration Cloud pour PME : Le Guide Complet 2025"

### Angle éditorial
Accompagner pas à pas un DSI de PME dans sa réflexion et son projet
de migration cloud, de l'évaluation à la mise en production.

### Structure proposée

1. **Introduction** (300 mots)
   - Hook: Coût moyen d'une panne serveur pour une PME
   - Promesse: Guide étape par étape
   - Pour qui: DSI/Responsables IT PME 50-200

2. **Pourquoi migrer vers le cloud en 2025** (500 mots)
   - Stats marché
   - Bénéfices clés (coûts, agilité, sécurité)
   - Signaux qu'il est temps de migrer

3. **Les différentes options cloud** (600 mots)
   - IaaS vs PaaS vs SaaS
   - Cloud public vs privé vs hybride
   - Focus: Cloud souverain français

4. **Évaluer son existant** (500 mots)
   - Audit infrastructure actuelle
   - Identifier les quick wins
   - Checklist pré-migration

5. **Planifier sa migration** (700 mots)
   - Méthodologie en 5 étapes
   - Timeline type (PME 100 salariés)
   - Budget prévisionnel

6. **Choisir son prestataire** (500 mots)
   - Critères de sélection
   - Questions à poser
   - Red flags

7. **Réussir la migration** (600 mots)
   - Best practices
   - Erreurs courantes
   - Change management

8. **Conclusion & prochaines étapes** (200 mots)
   - Récap
   - CTA: Audit gratuit

9. **FAQ** (300 mots)
   - 5 questions fréquentes

### Assets requis
- Infographie: "Les 5 étapes de la migration cloud"
- Tableau comparatif: Cloud public vs privé vs hybride
- Calculateur: Estimation coût migration (interactif si possible)
- Template: Checklist pré-migration (PDF téléchargeable)

### SEO Requirements

| Élément | Spécification |
|---------|---------------|
| Keyword principal | migration cloud pme (densité 1-2%) |
| Keywords secondaires | cloud souverain, cout cloud, migration IT |
| Meta title | Migration Cloud PME : Guide Complet 2025 [Étapes + Coûts] |
| Meta description | Découvrez comment migrer votre PME vers le cloud en 2025. Guide pratique avec étapes, coûts et checklist. Téléchargez notre template gratuit. |
| URL | /guides/migration-cloud-pme |
| Liens internes | 5 minimum (offre cloud, cas clients, contact) |
| Liens externes | 3-5 sources autoritaires (Gartner, CNIL, ANSSI) |

### CTA & Conversion
- CTA principal: "Demander un audit cloud gratuit"
- CTA secondaire: "Télécharger la checklist migration"
- Lead magnet: Checklist PDF + Calculateur Excel

## Planning

| Étape | Deadline | Responsable |
|-------|----------|-------------|
| Validation brief | 2025-01-11 | @marketing |
| Rédaction V1 | 2025-01-18 | @content-team |
| Création assets | 2025-01-20 | @design-team |
| Review SEO | 2025-01-21 | @seo-team |
| Validation finale | 2025-01-23 | @marketing |
| Publication | 2025-01-25 | @content-team |

## Références & Sources

### Études de marché
- Gartner Cloud Adoption Report 2024
- Markess "PME et Cloud" 2024
- INSEE "Équipement numérique des entreprises"

### Contenus concurrents
- OVH: guide-migration-cloud (3500 mots, 45 backlinks)
- Scaleway: cloud-pme-guide (2200 mots, 28 backlinks)

### Données internes
- 72% des leads cloud viennent de recherche organique
- Top performing content: "Comparatif cloud français" (5k visits/mois)

---

*Brief généré automatiquement le 2025-01-10*
*Workflow: request-to-brief v1.0.0*
```

### 3.2 Planning éditorial

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Créer entrées calendrier | content-management | editorial/calendar-manager | Calendar entries |
| Notifier équipe | content-management | editorial/workflow-controller | Notifications |

```json
{
  "calendar_entries": [
    {
      "id": "CAL-2025-001",
      "brief_id": "BRIEF-2025-001234",
      "title": "Guide Migration Cloud PME",
      "type": "pillar_content",
      "dates": {
        "brief_approved": "2025-01-11",
        "draft_due": "2025-01-18",
        "assets_due": "2025-01-20",
        "review_due": "2025-01-23",
        "publish_date": "2025-01-25"
      },
      "assignees": {
        "writer": "content-team",
        "designer": "design-team",
        "reviewer": "seo-team",
        "approver": "marketing"
      },
      "status": "brief_ready"
    }
  ]
}
```

---

## Phase 4 : Livraison (10 min)

### 4.1 Notification & validation

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Envoyer brief | client-intake | response/status-notifier | Email + PDF |
| Logger | task-orchestrator | tracking/audit-logger | Audit trail |

```
📧 Email envoyé à marketing@acme.fr:

Objet: ✅ Brief éditorial prêt - Guide Migration Cloud PME

Bonjour,

Suite à votre demande, voici le brief éditorial pour votre contenu
"Guide Migration Cloud PME".

📋 Résumé:
- Type: Guide pratique longform (3500+ mots)
- Keyword cible: "migration cloud pme" (1200 recherches/mois)
- Deadline publication: 25 janvier 2025
- Assets inclus: 4 (infographie, comparatif, calculateur, checklist)

📎 Documents joints:
- BRIEF-2025-001234.pdf (brief complet)
- BRIEF-2025-001234-outline.md (structure détaillée)

⏰ Prochaine étape:
Merci de valider ce brief avant le 11 janvier pour respecter le planning.

[Approuver le brief] [Demander des modifications]

Cordialement,
L'équipe Content
```

---

## Métriques du Workflow

| Métrique | Cible | Mesuré |
|----------|-------|--------|
| Temps total | < 4h | ~3h |
| Temps humain | < 30min | ~15min (validation) |
| Taux d'automatisation | > 85% | 90% |
| Briefs approuvés 1er jet | > 80% | 85% |
| Qualité SEO research | Score > 80 | 88 |

## Points d'Escalade Humaine

| Condition | Action |
|-----------|--------|
| Demande vague/incomplète | Demande clarification |
| Secteur inconnu | Research manuelle |
| Volume > 20 contenus | Validation stratégie |
| Deadline < 1 semaine | Alert + fast-track |
| Budget non défini | Clarification scope |

## Références

- [content-management/SKILL.md](../SKILL.md)
- [marketing/SKILL.md](../../marketing/SKILL.md)
- [client-intake/SKILL.md](../../client-intake/SKILL.md)
