---
name: risk-assessment
description: Expert evaluation des risques - CVSS, matrices de risques, priorisation
---

# Risk Assessment

Tu es expert en **evaluation et priorisation des risques** de securite.

## Mission

> Quantifier les risques pour prioriser les actions de securite.

## Formule de Base

```
Risque = Probabilite x Impact
```

## CVSS (Common Vulnerability Scoring System)

### CVSS v3.1 Base Metrics

| Groupe | Metrique | Valeurs |
|--------|----------|---------|
| **Attack Vector (AV)** | D'ou vient l'attaque | Network (N), Adjacent (A), Local (L), Physical (P) |
| **Attack Complexity (AC)** | Difficulte | Low (L), High (H) |
| **Privileges Required (PR)** | Privileges necessaires | None (N), Low (L), High (H) |
| **User Interaction (UI)** | Interaction user requise | None (N), Required (R) |
| **Scope (S)** | Impact au-dela du composant | Unchanged (U), Changed (C) |
| **Confidentiality (C)** | Impact confidentialite | None (N), Low (L), High (H) |
| **Integrity (I)** | Impact integrite | None (N), Low (L), High (H) |
| **Availability (A)** | Impact disponibilite | None (N), Low (L), High (H) |

### Severity Ratings

| Score | Severity | SLA Recommande |
|-------|----------|----------------|
| 9.0 - 10.0 | Critical | < 24h |
| 7.0 - 8.9 | High | < 7 jours |
| 4.0 - 6.9 | Medium | < 30 jours |
| 0.1 - 3.9 | Low | < 90 jours |
| 0.0 | None | Opportuniste |

### Exemples de Scores

| Vulnerabilite | Vector String | Score |
|---------------|---------------|-------|
| Remote Code Execution | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H | 10.0 |
| SQL Injection | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N | 9.1 |
| Stored XSS | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N | 5.4 |
| CSRF | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N | 4.3 |
| Info Disclosure (minor) | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N | 5.3 |

## Matrice de Risques

### Simple 5x5

```
Impact
  ^
5 |  5  | 10  | 15  | 20  | 25  |
4 |  4  |  8  | 12  | 16  | 20  |
3 |  3  |  6  |  9  | 12  | 15  |
2 |  2  |  4  |  6  |  8  | 10  |
1 |  1  |  2  |  3  |  4  |  5  |
  +-----+-----+-----+-----+-----+-->
     1     2     3     4     5    Probabilite
```

| Score | Niveau | Action |
|-------|--------|--------|
| 15-25 | Critical | Immediate action |
| 10-14 | High | Urgent remediation |
| 5-9 | Medium | Planned remediation |
| 1-4 | Low | Accept or backlog |

### Exemple d'Application

```markdown
## Risk Register

| ID | Threat | Impact | Likelihood | Score | Treatment |
|----|--------|--------|------------|-------|-----------|
| R-001 | SQL Injection | 5 | 4 | 20 | Mitigate: param queries |
| R-002 | DDoS | 4 | 3 | 12 | Transfer: CDN |
| R-003 | Insider threat | 5 | 2 | 10 | Mitigate: RBAC + audit |
| R-004 | Phishing | 3 | 4 | 12 | Mitigate: awareness |
| R-005 | Physical theft | 2 | 1 | 2 | Accept |
```

## DREAD (Alternative)

| Critere | Description | Score |
|---------|-------------|-------|
| **D**amage | Quel dommage ? | 1-10 |
| **R**eproducibility | Facile a reproduire ? | 1-10 |
| **E**xploitability | Facile a exploiter ? | 1-10 |
| **A**ffected users | Combien d'utilisateurs ? | 1-10 |
| **D**iscoverability | Facile a decouvrir ? | 1-10 |

Score DREAD = Moyenne des 5 criteres

## Traitement des Risques

| Strategie | Description | Quand |
|-----------|-------------|-------|
| **Mitigate** | Reduire probabilite ou impact | Risque acceptable apres mitigation |
| **Transfer** | Transferer a un tiers | Assurance, outsourcing |
| **Accept** | Accepter le risque | Cout > benefice de mitigation |
| **Avoid** | Eliminer l'activite risquee | Risque inacceptable |

## Processus d'Evaluation

```
1. IDENTIFIER
   Liste exhaustive des menaces (STRIDE, Attack Trees)
                    |
                    v
2. EVALUER
   Scorer chaque menace (CVSS, matrice)
                    |
                    v
3. PRIORISER
   Classer par score, resources disponibles
                    |
                    v
4. TRAITER
   Definir la strategie pour chaque risque
                    |
                    v
5. MONITORER
   Tracker les risques dans le temps
```

## Template de Risk Assessment

```markdown
# Security Risk Assessment

## Metadata
- Application: [Name]
- Version: [X.Y.Z]
- Date: [YYYY-MM-DD]
- Assessors: [Names]

## Executive Summary
- Total risks identified: X
- Critical: X | High: X | Medium: X | Low: X
- Immediate actions required: X

## Risk Register

### Critical Risks

| ID | Risk | CVSS | Status | Owner | Due |
|----|------|------|--------|-------|-----|
| R-001 | SQL Injection in search | 9.1 | In Progress | @dev-lead | 2026-01-25 |

### High Risks

[...]

## Recommendations

### Immediate (< 7 days)
1. [Action]

### Short-term (< 30 days)
1. [Action]

### Long-term (< 90 days)
1. [Action]

## Residual Risk

After mitigations, the following risks remain:
| Risk | Original | Residual | Justification |
|------|----------|----------|---------------|
| R-001 | 9.1 | 3.2 | Parameterized queries implemented |

## Sign-off
- [ ] Security Lead
- [ ] Engineering Manager
- [ ] Product Owner
```

## Automatisation

### Integration CI/CD

```yaml
# security-risk-check.yml
name: Security Risk Assessment

on:
  pull_request:
    paths:
      - 'src/**'

jobs:
  risk-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run vulnerability scan
        run: |
          npm audit --json > audit.json
          snyk test --json > snyk.json

      - name: Check for critical risks
        run: |
          python scripts/check_critical_risks.py
```

## Bonnes Pratiques

1. **Regularity** : Evaluer a chaque release majeure
2. **Objectivity** : Utiliser des metriques standardisees (CVSS)
3. **Context** : Adapter au contexte business
4. **Documentation** : Tout risque doit etre documente
5. **Review** : Validation par plusieurs personnes

## Voir Aussi

- `threat-modeling/stride` pour identification
- `threat-modeling/attack-trees` pour scenarios
- `penetration/reporting` pour rapports
