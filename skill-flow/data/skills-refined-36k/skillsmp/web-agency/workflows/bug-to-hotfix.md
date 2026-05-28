---
name: bug-to-hotfix
description: Workflow automatisé - Du signalement de bug au hotfix déployé
version: 1.0.0
---

# Workflow : Bug Report → Hotfix Déployé

Ce workflow montre comment l'agence IA traite automatiquement un signalement de bug critique jusqu'au déploiement du correctif.

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW BUG → HOTFIX (P1: < 4h)                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   INTAKE             TRIAGE              FIX                 DEPLOY              │
│                                                                                  │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │  BUG     │─────►│ QUALIFY  │──────►│  CODE    │──────►│ STAGING  │         │
│   │  REPORT  │      │ PRIORITY │       │  FIX     │       │  TEST    │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│        │                 │                   │                  │               │
│        ▼                 ▼                   ▼                  ▼               │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │ EXTRACT  │      │  QUEUE   │       │  TEST    │       │  PROD    │         │
│   │ CONTEXT  │      │ CRITICAL │       │  REVIEW  │       │  DEPLOY  │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│                                                                                  │
│   SLA par priorité:                                                             │
│   P1 (Critical) : 4h    P2 (High) : 8h    P3 (Medium) : 24h    P4 (Low) : 72h   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Triggers

```yaml
triggers:
  - type: webhook
    source: sentry
    events: [error.new, error.regression]

  - type: email
    patterns: ["bug", "erreur", "ne fonctionne pas", "cassé", "urgent"]

  - type: slack
    channels: [support, bugs]
    patterns: ["@support", "🐛"]

  - type: form
    endpoint: /api/support/bug-report
```

---

## Phase 1 : Intake & Triage (5-15 min)

### 1.1 Réception multi-canal

| Source | Skill | Agent | Output |
|--------|-------|-------|--------|
| Sentry webhook | client-intake | reception/webhook-receiver | Structured error |
| Email client | client-intake | reception/email-parser | Bug description |
| Slack message | client-intake | reception/chat-handler | Context extracted |
| Form submission | client-intake | reception/form-handler | Structured report |

**Exemple: Webhook Sentry**
```json
{
  "event": "error.new",
  "project": "acme-ecommerce",
  "error": {
    "type": "TypeError",
    "message": "Cannot read property 'price' of undefined",
    "file": "src/cart/CartTotal.tsx:42",
    "stack_trace": "...",
    "user_count": 156,
    "first_seen": "2025-01-08T14:30:00Z"
  },
  "tags": {
    "browser": "Chrome 120",
    "url": "/cart"
  }
}
```

### 1.2 Classification automatique

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Classifier intent | client-intake | qualification/intent-classifier | Intent: BUG_REPORT |
| Détecter urgence | client-intake | qualification/urgency-detector | Priority: P1 |
| Évaluer impact | client-intake | qualification/complexity-assessor | Impact: HIGH |

**Signaux de priorité P1 (Critical):**
```javascript
const p1Signals = {
  keywords: ["production down", "paiement bloqué", "données perdues"],
  metrics: {
    user_count: "> 100",
    error_rate: "> 5%",
    revenue_impact: true
  },
  sources: {
    sentry_severity: "fatal",
    client_escalation: true
  }
};
```

**Résultat qualification:**
```json
{
  "qualification": {
    "intent": "BUG_REPORT",
    "priority": "P1",
    "urgency_signals": [
      "156 utilisateurs impactés",
      "Page panier bloquée",
      "Impact chiffre d'affaires direct"
    ],
    "sla_deadline": "2025-01-08T18:30:00Z",
    "escalation": "immediate"
  }
}
```

### 1.3 Extraction contexte technique

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Stack technique | client-intake | extraction/tech-stack-detector | Stack info |
| Contraintes | client-intake | extraction/constraints-mapper | Deploy constraints |

```json
{
  "technical_context": {
    "project": "acme-ecommerce",
    "stack": ["Next.js", "TypeScript", "Medusa"],
    "file_impacted": "src/cart/CartTotal.tsx",
    "line": 42,
    "environment": "production",
    "last_deploy": "2025-01-08T10:00:00Z",
    "deploy_constraints": {
      "ci_required": true,
      "staging_test": true,
      "approval_needed": false  // P1 = fast track
    }
  }
}
```

### 1.4 Notification immédiate (P1)

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Alert team | client-intake | response/status-notifier | Slack + SMS |

```
🚨 ALERTE P1 - Bug Critique

Projet: ACME E-commerce
Erreur: TypeError in CartTotal.tsx:42
Impact: 156 utilisateurs, panier bloqué
SLA: 4h (deadline 18:30)

Tâche créée: BUG-2025-001234
[Voir détails] [Prendre en charge]
```

---

## Phase 2 : Orchestration (2-5 min)

### 2.1 Queue critique

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Créer tâche P1 | task-orchestrator | queue/queue-manager | Task queued |
| Ajuster priorité | task-orchestrator | queue/priority-adjuster | Top of queue |
| Vérifier SLA | task-orchestrator | queue/sla-tracker | SLA countdown |

```json
{
  "task": {
    "id": "BUG-2025-001234",
    "type": "HOTFIX",
    "priority": "P1",
    "queue": "critical",
    "position": 1,
    "state": "QUEUED",
    "sla": {
      "deadline": "2025-01-08T18:30:00Z",
      "remaining_minutes": 240,
      "auto_escalate_at": 180
    }
  }
}
```

### 2.2 Workflow hotfix

| Étape | Skill | Dépendance | Parallel |
|-------|-------|------------|----------|
| Analyser code | direction-technique | - | Non |
| Développer fix | frontend-developer | analyse | Non |
| Tests unitaires | testing-process | fix | Oui |
| Code review | lead-dev | fix | Oui |
| Deploy staging | devops | tests + review | Non |
| Tests e2e | testing-process | staging | Non |
| Deploy prod | devops | e2e | Non |

```javascript
const hotfixWorkflow = {
  id: "WF-HOTFIX-001234",
  fast_track: true,  // P1 = skip non-essential steps
  steps: [
    { id: "analyze", skill: "direction-technique", agent: "debugging/root-cause-analysis" },
    { id: "fix", skill: "frontend-developer", agent: "implementation/bug-fix", depends_on: ["analyze"] },
    { id: "unit-test", skill: "testing-process", agent: "types/unit-testing", depends_on: ["fix"], parallel_with: ["review"] },
    { id: "review", skill: "lead-dev", agent: "code-review/review-checklist", depends_on: ["fix"], parallel_with: ["unit-test"] },
    { id: "staging", skill: "devops", agent: "deployment/staging", depends_on: ["unit-test", "review"] },
    { id: "e2e", skill: "testing-process", agent: "types/e2e-testing", depends_on: ["staging"] },
    { id: "prod", skill: "devops", agent: "deployment/production", depends_on: ["e2e"] }
  ]
};
```

---

## Phase 3 : Fix & Test (1-3h)

### 3.1 Analyse root cause

**Skill**: `direction-technique`
**Agent**: `debugging/root-cause-analysis`

```markdown
## Root Cause Analysis - BUG-2025-001234

### Erreur
TypeError: Cannot read property 'price' of undefined
at CartTotal.tsx:42

### Cause
Le composant `CartTotal` ne gère pas le cas où un item du panier
a été supprimé côté backend mais reste en cache côté client.

### Solution
1. Ajouter une vérification null/undefined avant l'accès à `price`
2. Invalider le cache panier quand un produit retourne 404
3. Ajouter un error boundary sur le composant Cart

### Impact du fix
- Fichiers: 2 (CartTotal.tsx, useCart.ts)
- Risque régression: Faible
- Tests à ajouter: 3
```

### 3.2 Développement fix

**Skill**: `frontend-developer`
**Agent**: `implementation/bug-fix`

```typescript
// CartTotal.tsx - BEFORE
const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

// CartTotal.tsx - AFTER
const total = items
  .filter(item => item && item.price != null)
  .reduce((sum, item) => sum + item.price * item.quantity, 0);

// useCart.ts - Ajout invalidation cache
const removeItem = async (itemId: string) => {
  try {
    await api.cart.remove(itemId);
    queryClient.invalidateQueries(['cart']);  // Force refresh
  } catch (error) {
    if (error.status === 404) {
      queryClient.invalidateQueries(['cart']);
    }
    throw error;
  }
};
```

### 3.3 Tests & Review (parallèle)

**Tests unitaires** (`testing-process`):
```typescript
describe('CartTotal', () => {
  it('handles undefined items gracefully', () => {
    const items = [{ price: 10, quantity: 2 }, undefined, { price: 5, quantity: 1 }];
    expect(calculateTotal(items)).toBe(25);
  });

  it('handles items with null price', () => {
    const items = [{ price: null, quantity: 2 }, { price: 10, quantity: 1 }];
    expect(calculateTotal(items)).toBe(10);
  });
});
```

**Code review** (`lead-dev`):
```markdown
## Review - PR #456

✅ Fix correct et minimal
✅ Tests ajoutés couvrent le cas
✅ Pas de régression détectée
⚠️ Suggestion: Ajouter log Sentry pour monitoring

APPROVED - Fast track P1
```

---

## Phase 4 : Déploiement (30-60 min)

### 4.1 Staging

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Build | devops | ci-cd/build-pipeline | Docker image |
| Deploy staging | devops | deployment/staging | URL staging |
| Run e2e | testing-process | types/e2e-testing | Test report |

```yaml
# GitHub Actions - Hotfix Pipeline
name: Hotfix Deploy
on:
  push:
    branches: [hotfix/*]

jobs:
  staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
      - run: npm run build
      - uses: docker/build-push-action@v5
      - run: kubectl apply -f k8s/staging/

  e2e:
    needs: staging
    runs-on: ubuntu-latest
    steps:
      - run: npx playwright test --project=staging
```

### 4.2 Production

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Deploy prod | devops | deployment/production | Live |
| Verify | devops | monitoring/health-check | Status OK |
| Monitor | devops | monitoring/error-tracking | Sentry clear |

```json
{
  "deployment": {
    "environment": "production",
    "version": "1.2.1-hotfix.1",
    "deployed_at": "2025-01-08T17:45:00Z",
    "health_check": "PASSED",
    "rollback_available": true,
    "monitoring": {
      "sentry_errors": 0,
      "error_rate": "0.01%",
      "response_time_p99": "180ms"
    }
  }
}
```

---

## Phase 5 : Clôture (5 min)

### 5.1 Notification client

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Update status | client-intake | response/status-notifier | Email + Slack |

```
✅ Bug résolu - ACME E-commerce

Le problème de panier bloqué a été corrigé.
Temps de résolution: 3h 15min (SLA: 4h)

Détails:
- Cause: Cache client désynchronisé
- Fix: Validation données + invalidation cache
- Tests: +3 tests unitaires ajoutés

Le monitoring est en place pour détecter toute régression.

[Voir le rapport technique]
```

### 5.2 Métriques & Audit

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Log audit | task-orchestrator | tracking/audit-logger | Audit trail |
| Collecter KPIs | task-orchestrator | tracking/metrics-collector | Metrics |
| Clôturer | task-orchestrator | state-machine/state-controller | COMPLETED |

```json
{
  "resolution": {
    "task_id": "BUG-2025-001234",
    "state": "COMPLETED",
    "priority": "P1",
    "sla_met": true,
    "timeline": {
      "reported": "2025-01-08T14:30:00Z",
      "triaged": "2025-01-08T14:35:00Z",
      "fix_started": "2025-01-08T14:40:00Z",
      "deployed": "2025-01-08T17:45:00Z",
      "total_minutes": 195,
      "sla_minutes": 240
    },
    "metrics": {
      "users_impacted": 156,
      "estimated_revenue_saved": "€2,340",
      "mttr": "3h 15min"
    }
  }
}
```

---

## SLA par Priorité

| Priorité | SLA | Critères | Escalade |
|----------|-----|----------|----------|
| P1 Critical | 4h | Prod down, paiement bloqué, data loss | Immédiate |
| P2 High | 8h | Feature majeure cassée, >10 users | À 50% SLA |
| P3 Medium | 24h | Bug visible, workaround existe | À 75% SLA |
| P4 Low | 72h | Bug mineur, cosmétique | Aucune |

## Points d'Escalade

| Condition | Action |
|-----------|--------|
| SLA à 50% sans assignation | Alert lead-dev |
| SLA à 75% sans fix | Alert direction |
| P1 non résolu à 3h | War room |
| Régression post-deploy | Rollback auto |

## Références

- [client-intake/SKILL.md](../../client-intake/SKILL.md)
- [task-orchestrator/SKILL.md](../../task-orchestrator/SKILL.md)
- [devops/SKILL.md](../../devops/SKILL.md)
- [testing-process/SKILL.md](../../testing-process/SKILL.md)
