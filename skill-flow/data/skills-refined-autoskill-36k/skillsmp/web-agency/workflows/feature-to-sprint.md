---
name: feature-to-sprint
description: Workflow automatisé - De la demande de feature au sprint planning
version: 1.0.0
---

# Workflow : Feature Request → Sprint Planning

Ce workflow montre comment l'agence IA traite automatiquement une demande de nouvelle fonctionnalité, de la réception jusqu'à son intégration dans un sprint.

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                 WORKFLOW FEATURE REQUEST → SPRINT                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   JOUR 1              JOUR 2              JOUR 3-4            JOUR 5            │
│   INTAKE              ANALYSE             SPECS               PLANNING           │
│                                                                                  │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ REQUEST  │─────►│ FEASIB.  │──────►│ USER     │──────►│ BACKLOG  │         │
│   │ RECEIVED │      │ STUDY    │       │ STORIES  │       │ REFINED  │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│        │                 │                   │                  │               │
│        ▼                 ▼                   ▼                  ▼               │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ QUALIFY  │      │ ESTIMATE │       │ TASKS    │       │ SPRINT   │         │
│   │ & ROUTE  │      │ & SCOPE  │       │ BREAKDOWN│       │ ASSIGNED │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│                                                                                  │
│   Cycle complet: 3-5 jours ouvrés                                               │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Triggers

```yaml
triggers:
  - type: email
    patterns:
      - "nouvelle fonctionnalité"
      - "j'aimerais pouvoir"
      - "serait-il possible"
      - "feature request"
      - "amélioration"

  - type: form
    endpoint: /api/feedback/feature-request

  - type: slack
    channels: [product-feedback, client-requests]
    reactions: [💡, ✨, 🚀]

  - type: intercom
    tags: [feature-request, enhancement]
```

---

## Phase 1 : Intake & Qualification (Jour 1)

### 1.1 Réception

| Source | Skill | Agent | Output |
|--------|-------|-------|--------|
| Email client | client-intake | reception/email-parser | Structured request |
| Formulaire | client-intake | reception/form-handler | Feature data |
| Slack/Intercom | client-intake | reception/chat-handler | Context extracted |

**Exemple: Email client**
```
De: marie.martin@clientxyz.com
Objet: Suggestion - Export des rapports en PDF

Bonjour,

Nous utilisons votre plateforme quotidiennement et aurions besoin
de pouvoir exporter nos rapports mensuels en PDF pour les partager
avec notre direction qui n'a pas accès à l'outil.

Idéalement, on aimerait:
- Choisir la période
- Sélectionner les métriques à inclure
- Avoir le logo de notre entreprise sur le document
- Pouvoir planifier un envoi automatique

C'est quelque chose que vous pourriez envisager?

Merci,
Marie Martin
Responsable Analytics - ClientXYZ
```

### 1.2 Qualification

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Classifier intent | client-intake | qualification/intent-classifier | Intent: FEATURE_REQUEST |
| Évaluer complexité | client-intake | qualification/complexity-assessor | Size: M |
| Détecter urgence | client-intake | qualification/urgency-detector | Priority: P3 |
| Vérifier faisabilité | client-intake | qualification/feasibility-checker | Feasibility: GO |

```json
{
  "qualification": {
    "intent": "FEATURE_REQUEST",
    "category": "REPORTING",
    "complexity": {
      "size": "M",
      "score": 55,
      "effort_estimate": "5-8 jours"
    },
    "urgency": {
      "level": "P3",
      "signals": [],
      "business_value": "HIGH"
    },
    "feasibility": {
      "status": "GO",
      "technical": true,
      "dependencies": ["PDF library", "Scheduler service"],
      "risks": ["Performance génération PDF volumineux"]
    },
    "similar_requests": 3,
    "client_tier": "ENTERPRISE"
  }
}
```

### 1.3 Extraction des requirements

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Extraire requirements | client-intake | extraction/requirements-extractor | Requirements |
| Parser timeline | client-intake | extraction/timeline-parser | Expectations |
| Mapper contraintes | client-intake | extraction/constraints-mapper | Constraints |

```json
{
  "requirements": {
    "functional": [
      "Sélection de période (date range)",
      "Choix des métriques à inclure",
      "Personnalisation logo/branding",
      "Export PDF téléchargeable",
      "Planification d'envoi automatique"
    ],
    "non_functional": [
      "Génération < 30 secondes",
      "Support rapports > 100 pages",
      "Responsive email template"
    ],
    "out_of_scope_detected": [
      "Export Excel (non mentionné)",
      "API publique (non mentionné)"
    ]
  },
  "client_expectations": {
    "timeline_mentioned": null,
    "budget_mentioned": null,
    "priority_expressed": "nice-to-have"
  }
}
```

### 1.4 Accusé de réception

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Envoyer accusé | client-intake | response/acknowledgment-sender | Email |
| Demander clarif | client-intake | response/clarification-requester | Questions (si besoin) |

```
📧 Email envoyé à marie.martin@clientxyz.com:

Objet: [Reçu] Votre suggestion - Export PDF des rapports

Bonjour Marie,

Merci pour votre suggestion concernant l'export PDF des rapports!

Nous avons bien noté votre besoin:
✓ Sélection de période personnalisée
✓ Choix des métriques
✓ Personnalisation avec logo entreprise
✓ Planification d'envoi automatique

Votre demande a été ajoutée à notre backlog produit et sera
évaluée par notre équipe. Nous reviendrons vers vous sous
quelques jours avec une estimation.

Référence: FEAT-2025-000456

Cordialement,
L'équipe Produit
```

---

## Phase 2 : Orchestration & Analyse (Jour 1-2)

### 2.1 Création tâche produit

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Router | client-intake | routing/skill-matcher | Skills: [direction-technique, project-management] |
| Prioriser | client-intake | routing/priority-ranker | Score: 68/100 |
| Résoudre dépendances | client-intake | routing/dependency-resolver | Dependencies mapped |
| Créer tâche | task-orchestrator | queue/queue-manager | Task queued |

```json
{
  "task": {
    "id": "FEAT-2025-000456",
    "type": "FEATURE_REQUEST",
    "priority_score": 68,
    "queue": "normal",
    "state": "QUEUED",
    "routing": {
      "primary_skill": "direction-technique",
      "secondary_skills": ["project-management", "frontend-developer", "backend-developer"],
      "workflow": "feature-to-sprint"
    },
    "metadata": {
      "client": "ClientXYZ",
      "client_tier": "ENTERPRISE",
      "similar_requests_count": 3,
      "business_value": "HIGH"
    }
  }
}
```

### 2.2 Workflow d'analyse

```javascript
const featureWorkflow = {
  id: "WF-FEAT-000456",
  stages: [
    {
      name: "analysis",
      steps: [
        { id: "feasibility", skill: "direction-technique", agent: "avant-projet/etude-faisabilite" },
        { id: "estimation", skill: "direction-technique", agent: "estimation/estimation-macro" },
        { id: "scope", skill: "project-management", agent: "avant-projet/analyse-perimetre" }
      ]
    },
    {
      name: "specification",
      steps: [
        { id: "specs", skill: "direction-technique", agent: "specification/specification-technique" },
        { id: "stories", skill: "project-management", agent: "pilotage/user-stories" },
        { id: "tasks", skill: "lead-dev", agent: "technical-decisions/task-breakdown" }
      ]
    },
    {
      name: "planning",
      steps: [
        { id: "refinement", skill: "project-management", agent: "pilotage/backlog-refinement" },
        { id: "sprint", skill: "lead-dev", agent: "delivery/sprint-planning" }
      ]
    }
  ]
};
```

---

## Phase 3 : Étude & Estimation (Jour 2)

### 3.1 Étude de faisabilité technique

**Skill**: `direction-technique`
**Agent**: `avant-projet/etude-faisabilite`

```markdown
## Étude de Faisabilité - FEAT-2025-000456
### Export PDF des Rapports

#### Faisabilité Technique: ✅ GO

**Architecture proposée:**
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────►│   API       │────►│  PDF        │
│   (React)   │     │  /reports   │     │  Generator  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  Scheduler  │────►│   Email     │
                    │  (Bull)     │     │   Service   │
                    └─────────────┘     └─────────────┘
```

**Composants nécessaires:**
1. React PDF (@react-pdf/renderer) - Génération PDF côté serveur
2. Bull Queue - Planification des tâches
3. SendGrid - Envoi emails programmés

**Risques identifiés:**
| Risque | Impact | Mitigation |
|--------|--------|------------|
| Performance grands rapports | Medium | Pagination, génération async |
| Timeout génération | Low | Worker dédié, progress tracking |
| Complexité templating | Low | Design system tokens réutilisés |

**Conclusion:** Projet réalisable avec stack existante
```

### 3.2 Estimation technique

**Skill**: `direction-technique`
**Agent**: `estimation/estimation-macro`

```json
{
  "estimation": {
    "feature": "Export PDF des Rapports",
    "breakdown": [
      {
        "lot": "Backend - API & Génération",
        "tasks": [
          "Endpoint POST /api/reports/export",
          "Service génération PDF",
          "Templates PDF (3 layouts)"
        ],
        "estimate_days": 3,
        "skills": ["backend-developer"]
      },
      {
        "lot": "Backend - Scheduler",
        "tasks": [
          "Configuration Bull Queue",
          "Job scheduled-report",
          "Gestion erreurs/retries"
        ],
        "estimate_days": 1.5,
        "skills": ["backend-developer"]
      },
      {
        "lot": "Frontend - UI",
        "tasks": [
          "Modal export configuration",
          "Composant date range picker",
          "Sélecteur métriques",
          "Page gestion schedules"
        ],
        "estimate_days": 2.5,
        "skills": ["frontend-developer"]
      },
      {
        "lot": "Tests & Documentation",
        "tasks": [
          "Tests unitaires (API + Frontend)",
          "Tests e2e workflow complet",
          "Documentation utilisateur"
        ],
        "estimate_days": 1.5,
        "skills": ["testing-process"]
      }
    ],
    "total_days": 8.5,
    "buffer": 1.5,
    "total_with_buffer": 10,
    "confidence": "HIGH",
    "team_required": ["1 backend", "1 frontend"]
  }
}
```

### 3.3 Analyse périmètre

**Skill**: `project-management`
**Agent**: `avant-projet/analyse-perimetre`

```markdown
## Analyse Périmètre - Export PDF

### Dans le périmètre (MVP)
- ✅ Export PDF manuel (bouton)
- ✅ Sélection période
- ✅ Sélection métriques
- ✅ Logo client (upload)

### Phase 2 (post-MVP)
- 📅 Planification envoi automatique
- 📅 Templates multiples
- 📅 Export batch (plusieurs rapports)

### Hors périmètre
- ❌ Export Excel
- ❌ API publique
- ❌ Génération temps réel (> 100 pages)

### Décision
MVP en 6 jours, Scheduler en +4 jours = 10 jours total
Recommandation: Livrer MVP d'abord, itérer ensuite
```

---

## Phase 4 : Spécification (Jour 3-4)

### 4.1 User Stories

**Skill**: `project-management`
**Agent**: `pilotage/user-stories`

```markdown
## Epic: Export PDF des Rapports

### US-001: Export PDF manuel
**En tant que** utilisateur analytics
**Je veux** exporter un rapport en PDF
**Afin de** le partager avec ma direction

**Critères d'acceptation:**
- [ ] Bouton "Exporter PDF" visible sur page rapport
- [ ] Modal permet de choisir la période
- [ ] Modal permet de sélectionner les métriques
- [ ] PDF téléchargé contient les données sélectionnées
- [ ] Temps de génération < 30s pour rapports standards

**Story Points:** 5

---

### US-002: Personnalisation branding
**En tant qu'** administrateur
**Je veux** configurer le logo de mon entreprise
**Afin que** les exports PDF soient brandés

**Critères d'acceptation:**
- [ ] Upload logo dans settings
- [ ] Logo apparaît en header du PDF
- [ ] Formats supportés: PNG, JPG, SVG
- [ ] Taille max: 2MB

**Story Points:** 2

---

### US-003: Planification export automatique
**En tant que** utilisateur analytics
**Je veux** programmer un envoi automatique hebdomadaire
**Afin de** recevoir mes rapports sans action manuelle

**Critères d'acceptation:**
- [ ] Interface création schedule
- [ ] Choix fréquence (quotidien/hebdo/mensuel)
- [ ] Choix destinataires email
- [ ] Email reçu avec PDF en PJ
- [ ] Historique des envois consultable

**Story Points:** 8

---

**Total Epic:** 15 points
**Vélocité équipe:** 20 points/sprint
**Estimation:** 1 sprint (75% capacité)
```

### 4.2 Découpage technique

**Skill**: `lead-dev`
**Agent**: `technical-decisions/task-breakdown`

```markdown
## Tasks Techniques - FEAT-2025-000456

### Sprint 1 - Export PDF (10 jours)

#### Backend
- [ ] TASK-001: Créer endpoint POST /api/reports/export (0.5j)
- [ ] TASK-002: Implémenter ReportPdfService (1j)
- [ ] TASK-003: Créer templates PDF React-PDF (1.5j)
- [ ] TASK-004: Configurer Bull Queue pour async generation (0.5j)
- [ ] TASK-005: Implémenter job scheduled-report (1j)
- [ ] TASK-006: Intégration SendGrid pour envoi (0.5j)

#### Frontend
- [ ] TASK-007: Composant ExportModal (1j)
- [ ] TASK-008: Composant DateRangePicker (0.5j)
- [ ] TASK-009: Composant MetricsSelector (0.5j)
- [ ] TASK-010: Page ScheduleManagement (1j)
- [ ] TASK-011: Integration API export (0.5j)

#### QA
- [ ] TASK-012: Tests unitaires services (0.5j)
- [ ] TASK-013: Tests e2e export workflow (0.5j)
- [ ] TASK-014: Tests e2e scheduler (0.5j)

#### Documentation
- [ ] TASK-015: Guide utilisateur export PDF (0.25j)
- [ ] TASK-016: Documentation technique API (0.25j)
```

---

## Phase 5 : Sprint Planning (Jour 5)

### 5.1 Backlog Refinement

**Skill**: `project-management`
**Agent**: `pilotage/backlog-refinement`

```json
{
  "backlog_item": {
    "id": "FEAT-2025-000456",
    "title": "Export PDF des Rapports",
    "epic": "Reporting",
    "status": "REFINED",
    "priority": "HIGH",
    "business_value": 8,
    "effort": 10,
    "roi_score": 0.8,
    "dependencies": [],
    "ready_for_sprint": true,
    "definition_of_ready": {
      "user_stories_written": true,
      "acceptance_criteria_defined": true,
      "technical_tasks_created": true,
      "estimation_complete": true,
      "dependencies_resolved": true,
      "designs_available": true
    }
  }
}
```

### 5.2 Assignation Sprint

**Skill**: `lead-dev`
**Agent**: `delivery/sprint-planning`

```json
{
  "sprint": {
    "id": "SPRINT-2025-03",
    "name": "Sprint 3 - Export & Analytics",
    "start_date": "2025-01-13",
    "end_date": "2025-01-24",
    "capacity_points": 20,
    "committed_points": 18,
    "items": [
      {
        "id": "FEAT-2025-000456",
        "title": "Export PDF des Rapports",
        "points": 15,
        "assignees": ["dev-backend-1", "dev-frontend-1"],
        "status": "PLANNED"
      },
      {
        "id": "BUG-2025-000123",
        "title": "Fix timezone reports",
        "points": 3,
        "assignees": ["dev-backend-1"],
        "status": "PLANNED"
      }
    ],
    "goals": [
      "Livrer MVP export PDF",
      "Corriger bugs critiques reporting"
    ]
  }
}
```

### 5.3 Communication client

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Notifier statut | client-intake | response/status-notifier | Email client |

```
📧 Email envoyé à marie.martin@clientxyz.com:

Objet: Votre suggestion acceptée - Export PDF des rapports

Bonjour Marie,

Bonne nouvelle! Votre suggestion d'export PDF a été retenue
et planifiée.

📅 Planning:
- Développement: Sprint 3 (13-24 janvier)
- Livraison estimée: Fin janvier 2025

📋 Fonctionnalités incluses (MVP):
✓ Export PDF avec sélection de période
✓ Choix des métriques à inclure
✓ Logo de votre entreprise sur les documents
✓ Planification d'envoi automatique

Nous vous tiendrons informée de l'avancement.

Référence: FEAT-2025-000456

Cordialement,
L'équipe Produit
```

---

## Phase 6 : Clôture & Tracking

### 6.1 Métriques

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Logger audit | task-orchestrator | tracking/audit-logger | Audit trail |
| Collecter KPIs | task-orchestrator | tracking/metrics-collector | Metrics |
| Générer rapport | task-orchestrator | tracking/report-generator | Report |

```json
{
  "feature_lifecycle": {
    "id": "FEAT-2025-000456",
    "final_state": "SPRINT_PLANNED",
    "timeline": {
      "submitted": "2025-01-08T09:00:00Z",
      "qualified": "2025-01-08T09:15:00Z",
      "analyzed": "2025-01-09T14:00:00Z",
      "specified": "2025-01-10T16:00:00Z",
      "planned": "2025-01-10T17:00:00Z",
      "total_days": 3
    },
    "metrics": {
      "time_to_qualify": "15 min",
      "time_to_estimate": "1 jour",
      "time_to_sprint": "3 jours",
      "automation_rate": "85%",
      "human_touchpoints": 2
    },
    "next_milestone": {
      "event": "development_start",
      "date": "2025-01-13"
    }
  }
}
```

---

## Priorisation des Feature Requests

### Matrice de scoring

```javascript
const priorityScore = (feature) => {
  const weights = {
    business_value: 0.30,    // Impact business (1-10)
    client_tier: 0.20,       // Enterprise=10, SMB=5, Free=2
    request_count: 0.15,     // Nombre de demandes similaires
    effort_inverse: 0.15,    // 10 - effort_days (inversé)
    strategic_fit: 0.10,     // Alignement roadmap
    urgency: 0.10            // Signaux urgence
  };

  return Object.entries(weights).reduce((score, [key, weight]) => {
    return score + (feature[key] * weight);
  }, 0);
};

// Exemple FEAT-2025-000456:
// business_value: 8, client_tier: 10, request_count: 3,
// effort_inverse: 2, strategic_fit: 7, urgency: 3
// Score = 8*0.3 + 10*0.2 + 3*0.15 + 2*0.15 + 7*0.1 + 3*0.1
// Score = 2.4 + 2.0 + 0.45 + 0.30 + 0.7 + 0.3 = 6.15/10
```

### Seuils de décision

| Score | Décision | Action |
|-------|----------|--------|
| > 7 | Priority High | Sprint suivant |
| 5-7 | Priority Medium | Backlog priorisé |
| 3-5 | Priority Low | Backlog |
| < 3 | Won't Do | Archive + feedback |

## Références

- [client-intake/SKILL.md](../../client-intake/SKILL.md)
- [task-orchestrator/SKILL.md](../../task-orchestrator/SKILL.md)
- [project-management/SKILL.md](../../project-management/SKILL.md)
- [direction-technique/SKILL.md](../../direction-technique/SKILL.md)
