---
name: email-to-devis
description: Workflow automatisé - De l'email client au devis en moins de 24h
version: 1.0.0
---

# Workflow : Email Client → Devis Automatisé

Ce workflow montre comment l'agence IA traite automatiquement un email client pour produire un devis qualifié en moins de 24h.

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW EMAIL → DEVIS (< 24h)                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   NIVEAU 0           NIVEAU 1            NIVEAU 2-3          NIVEAU 4           │
│   INTAKE             ORCHESTRATION       MÉTIER              OUTPUT              │
│                                                                                  │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │  EMAIL   │─────►│  QUEUE   │──────►│ PROJECT  │──────►│  DEVIS   │         │
│   │  REÇU    │      │  TASK    │       │ MGMT     │       │  PDF     │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│        │                 │                   │                  │               │
│        ▼                 ▼                   ▼                  ▼               │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ QUALIF   │      │ DISPATCH │       │ DIRECTION│       │  EMAIL   │         │
│   │ AUTO     │      │ SKILLS   │       │ TECHNIQUE│       │  CLIENT  │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│                                                                                  │
│   ~2 min             ~1 min              ~2-4h               ~5 min             │
│                                                                                  │
│   TOTAL: 2-4h (automatisé) + validation humaine                                 │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Trigger

```yaml
trigger:
  type: email
  patterns:
    - "demande de devis"
    - "nouveau projet"
    - "besoin d'un site"
    - "combien coûte"
  from: "*"  # tout expéditeur
```

## Phase 1 : Intake Automatique (2-5 min)

### 1.1 Réception

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Parsing email | client-intake | reception/email-parser | Raw email | Structured data |
| Pièces jointes | client-intake | reception/attachment-processor | Attachments | Extracted content |

```json
{
  "email_parsed": {
    "from": "jean.dupont@acme.fr",
    "subject": "Demande de devis - Refonte site e-commerce",
    "body_text": "...",
    "attachments": [
      { "name": "cahier-des-charges.pdf", "content_extracted": "..." }
    ]
  }
}
```

### 1.2 Qualification

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Classifier intent | client-intake | qualification/intent-classifier | Parsed email | Intent: NEW_PROJECT |
| Évaluer complexité | client-intake | qualification/complexity-assessor | Email + attachments | Size: M, Score: 65 |
| Détecter urgence | client-intake | qualification/urgency-detector | Full context | Priority: P3 (normal) |
| Estimer budget | client-intake | qualification/budget-estimator | Complexity + intent | Range: 15-30k€ |
| Vérifier faisabilité | client-intake | qualification/feasibility-checker | All data | GO |

```json
{
  "qualification": {
    "intent": "NEW_PROJECT",
    "project_type": "E_COMMERCE",
    "complexity": { "size": "M", "score": 65, "days_estimate": "30-45" },
    "urgency": { "level": "P3", "signals": [] },
    "budget": { "estimated": "15000-30000", "client_mentioned": null },
    "feasibility": { "status": "GO", "blockers": [] }
  }
}
```

### 1.3 Extraction

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Extraire requirements | client-intake | extraction/requirements-extractor | Full context | Requirements list |
| Identifier stakeholders | client-intake | extraction/stakeholder-identifier | Email | Contacts |
| Parser timeline | client-intake | extraction/timeline-parser | Email | Deadlines |
| Détecter stack | client-intake | extraction/tech-stack-detector | CDC + email | Tech preferences |
| Mapper contraintes | client-intake | extraction/constraints-mapper | All | Constraints |

```json
{
  "extraction": {
    "requirements": {
      "functional": ["Catalogue 500 produits", "Panier", "Paiement CB"],
      "non_functional": ["Mobile-first", "RGPD"],
      "technical": ["Migration depuis Prestashop"]
    },
    "stakeholders": {
      "decision_maker": "Jean Dupont (DG)",
      "contacts": ["marketing@acme.fr"]
    },
    "timeline": {
      "deadline_mentioned": "Septembre 2025",
      "flexibility": "MEDIUM"
    },
    "tech_preferences": {
      "current": ["Prestashop"],
      "desired": null,
      "constraints": ["Hébergement OVH existant"]
    }
  }
}
```

### 1.4 Accusé de réception

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Envoyer accusé | client-intake | response/acknowledgment-sender | Email de confirmation |

```
📧 Email envoyé à jean.dupont@acme.fr:

Objet: [Reçu] Votre demande de devis - Refonte site e-commerce

Bonjour Jean,

Nous avons bien reçu votre demande concernant la refonte de votre
site e-commerce.

Notre équipe analyse actuellement votre projet et reviendra vers
vous sous 24h avec une première estimation.

Référence: REQ-2025-001234

Cordialement,
L'équipe [Agence]
```

---

## Phase 2 : Orchestration (1-2 min)

### 2.1 Création de la tâche

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Router vers skills | client-intake | routing/skill-matcher | Qualification | Skills: [project-management, direction-technique] |
| Calculer priorité | client-intake | routing/priority-ranker | All data | Score: 72/100 |
| Créer tâche | task-orchestrator | queue/queue-manager | Routed request | Task ID |

```json
{
  "task": {
    "id": "TASK-2025-001234",
    "type": "DEVIS_REQUEST",
    "priority_score": 72,
    "queue": "high_priority",
    "state": "QUEUED",
    "target_skills": ["project-management", "direction-technique"],
    "sla_deadline": "2025-01-09T10:30:00Z"
  }
}
```

### 2.2 Workflow multi-skills

| Étape | Skill | Agent | Dépendance |
|-------|-------|-------|------------|
| Formaliser brief | project-management | avant-projet/formalisation-brief | - |
| Étude faisabilité tech | direction-technique | avant-projet/etude-faisabilite | brief |
| Chiffrage commercial | project-management | avant-projet/chiffrage | faisabilité |
| Estimation technique | direction-technique | estimation/estimation-macro | faisabilité |
| Rédaction proposition | project-management | avant-projet/redaction-proposition | chiffrage + estimation |

```javascript
const workflow = {
  id: "WF-DEVIS-001234",
  steps: [
    { id: "brief", skill: "project-management", agent: "formalisation-brief", parallel: false },
    { id: "feasibility", skill: "direction-technique", agent: "etude-faisabilite", depends_on: ["brief"] },
    { id: "commercial", skill: "project-management", agent: "chiffrage", depends_on: ["feasibility"] },
    { id: "technical", skill: "direction-technique", agent: "estimation-macro", depends_on: ["feasibility"] },
    { id: "proposal", skill: "project-management", agent: "redaction-proposition", depends_on: ["commercial", "technical"] }
  ]
};
```

---

## Phase 3 : Exécution Métier (2-4h)

### 3.1 Brief formalisé

**Skill**: `project-management`
**Agent**: `avant-projet/formalisation-brief`

```markdown
# Brief Projet - ACME E-commerce

## Client
- Entreprise: ACME Corp
- Contact: Jean Dupont (DG)
- Email: jean.dupont@acme.fr

## Contexte
Migration e-commerce Prestashop → nouvelle plateforme

## Objectifs
1. Moderniser l'expérience utilisateur (mobile-first)
2. Améliorer les performances
3. Faciliter la gestion du catalogue (500 produits)

## Périmètre
- Catalogue produits avec filtres avancés
- Tunnel d'achat optimisé
- Paiement CB (Stripe)
- Espace client
- Conformité RGPD

## Contraintes
- Hébergement OVH (existant)
- Deadline: Septembre 2025
- Migration données existantes

## Hors périmètre
- Application mobile native
- Marketplace multi-vendeurs
```

### 3.2 Estimation technique

**Skill**: `direction-technique`
**Agent**: `estimation/estimation-macro`

```json
{
  "estimation": {
    "stack_recommandee": "Next.js + Medusa",
    "lots": [
      { "name": "Setup & Architecture", "jours": 5 },
      { "name": "Catalogue & Filtres", "jours": 8 },
      { "name": "Tunnel d'achat", "jours": 10 },
      { "name": "Espace client", "jours": 5 },
      { "name": "Migration données", "jours": 4 },
      { "name": "Intégration paiement", "jours": 3 },
      { "name": "Tests & Recette", "jours": 5 }
    ],
    "total_jours": 40,
    "fourchette": { "min": 35, "max": 50 },
    "risques": ["Complexité migration Prestashop", "Intégration OVH"]
  }
}
```

### 3.3 Proposition commerciale

**Skill**: `project-management`
**Agent**: `avant-projet/redaction-proposition`

Génère un PDF avec:
- Récapitulatif du besoin
- Solution proposée
- Planning prévisionnel
- Chiffrage détaillé
- Conditions générales

---

## Phase 4 : Livraison (5 min)

### 4.1 Validation humaine

```
🔔 NOTIFICATION → Slack #sales

Nouveau devis prêt pour validation:
- Client: ACME Corp (Jean Dupont)
- Projet: Refonte e-commerce
- Montant: 24 000 € HT
- Délai: 10 semaines

[Voir le devis] [Approuver] [Modifier]
```

### 4.2 Envoi au client

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Notifier statut | client-intake | response/status-notifier | Email + devis PDF |

```
📧 Email envoyé à jean.dupont@acme.fr:

Objet: Votre devis - Refonte site e-commerce ACME

Bonjour Jean,

Suite à votre demande, veuillez trouver ci-joint notre
proposition pour la refonte de votre site e-commerce.

Points clés:
- Solution: Next.js + Medusa (headless commerce)
- Délai: 10 semaines
- Budget: 24 000 € HT

Je reste disponible pour en discuter.

[Proposition-ACME-2025.pdf]

Cordialement,
L'équipe [Agence]
```

### 4.3 Tracking

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Logger audit | task-orchestrator | tracking/audit-logger | Audit trail |
| Collecter métriques | task-orchestrator | tracking/metrics-collector | KPIs |
| Clôturer tâche | task-orchestrator | state-machine/state-controller | State: COMPLETED |

```json
{
  "task_completed": {
    "id": "TASK-2025-001234",
    "state": "COMPLETED",
    "duration_total": "3h 42min",
    "duration_breakdown": {
      "intake": "4min",
      "orchestration": "2min",
      "execution": "3h 30min",
      "delivery": "6min"
    },
    "sla_met": true,
    "human_interventions": 1
  }
}
```

---

## Métriques du Workflow

| Métrique | Cible | Mesuré |
|----------|-------|--------|
| Temps total | < 24h | ~4h |
| Temps humain | < 30min | ~15min (validation) |
| Taux d'automatisation | > 80% | 94% |
| Précision qualification | > 90% | À mesurer |

## Points d'Escalade Humaine

| Condition | Action |
|-----------|--------|
| Budget estimé > 50k€ | Validation direction |
| Complexité XXL | Review technique |
| Client existant (upsell) | Notification commercial |
| Faisabilité = BLOCKED | Analyse manuelle |

## Références

- [client-intake/SKILL.md](../../client-intake/SKILL.md)
- [task-orchestrator/SKILL.md](../../task-orchestrator/SKILL.md)
- [project-management/SKILL.md](../../project-management/SKILL.md)
