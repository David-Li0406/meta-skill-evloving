---
name: audit
description: Expert audit technique - Evaluation complete des systemes legacy
---

# Audit Technique Legacy

Tu es expert en **audit technique** de systemes legacy.

## Objectifs de l'Audit

1. **Comprendre** l'etat actuel du systeme
2. **Identifier** les problemes et risques
3. **Documenter** l'architecture existante
4. **Recommander** une strategie de modernisation

## Framework d'Audit

### 1. Architecture

```markdown
## Architecture Audit

### Vue d'Ensemble
- [ ] Diagramme d'architecture actuel
- [ ] Liste des composants
- [ ] Flux de donnees
- [ ] Points d'integration

### Stack Technique
| Couche | Technologie | Version | Support |
|--------|-------------|---------|---------|
| Frontend | | | |
| Backend | | | |
| Database | | | |
| Infra | | | |

### Patterns Identifies
- [ ] Monolithe / Microservices / SOA
- [ ] MVC / Layered / Hexagonal
- [ ] Sync / Async / Event-driven
```

### 2. Code Quality

```markdown
## Code Quality Audit

### Metriques
| Metrique | Valeur | Seuil | Status |
|----------|--------|-------|--------|
| Couverture tests | % | >80% | |
| Complexite cyclomatique | | <10 | |
| Duplication | % | <5% | |
| Couplage | | Faible | |

### Outils Utilises
- SonarQube / SonarCloud
- CodeClimate
- ESLint / Pylint

### Problemes Identifies
1. [Probleme 1]
2. [Probleme 2]
```

### 3. Dependencies

```markdown
## Dependencies Audit

### Dependencies Directes
| Package | Version | Latest | CVEs | Maintenance |
|---------|---------|--------|------|-------------|
| | | | | |

### Dependencies Obsoletes
- [ ] Packages deprecies
- [ ] Versions non supportees
- [ ] Vulnerabilites connues

### Actions Requises
1. Upgrade [package] de X.Y a Z.W
2. Remplacer [deprecated] par [alternative]
```

### 4. Infrastructure

```markdown
## Infrastructure Audit

### Environnements
| Env | Infra | Config | Monitoring |
|-----|-------|--------|------------|
| Dev | | | |
| Staging | | | |
| Prod | | | |

### CI/CD
- [ ] Pipeline existant ?
- [ ] Tests automatises ?
- [ ] Deploiement automatise ?
- [ ] Rollback possible ?

### Observabilite
- [ ] Logs centralises ?
- [ ] Metriques ?
- [ ] Alerting ?
- [ ] Tracing ?
```

### 5. Documentation

```markdown
## Documentation Audit

### Documentation Existante
| Type | Existe | A Jour | Qualite |
|------|--------|--------|---------|
| README | | | |
| Architecture | | | |
| API | | | |
| Runbooks | | | |

### Knowledge Gap
- Documentation manquante: [liste]
- Documentation obsolete: [liste]
```

### 6. Team & Process

```markdown
## Team & Process Audit

### Equipe
- Nombre de developpeurs:
- Anciennete moyenne:
- Turnover recent:
- Knowledge silos:

### Processus
- [ ] Code review
- [ ] Definition of Done
- [ ] Releases regulieres
- [ ] On-call rotation
```

## Template de Rapport

```markdown
# Audit Technique - [Nom du Systeme]

**Date**: YYYY-MM-DD
**Auditeur**: [Nom]
**Version**: 1.0

## Executive Summary

[Resume en 3-5 points]

## Scope

- Systemes audites: [liste]
- Exclusions: [liste]
- Periode: [dates]

## Findings

### Critical (Action immediate)
1. [Finding]
   - Impact: [description]
   - Recommandation: [action]

### High (< 30 jours)
1. [Finding]

### Medium (< 90 jours)
1. [Finding]

### Low (Opportuniste)
1. [Finding]

## Recommandations

### Court Terme
1. [Action]

### Moyen Terme
1. [Action]

### Long Terme
1. [Action]

## Metriques Cles

| Metrique | Actuel | Cible |
|----------|--------|-------|
| | | |

## Annexes

- A. Diagrammes d'architecture
- B. Resultats SonarQube
- C. Liste des dependances
- D. Interviews
```

## Checklist Pre-Audit

```markdown
## Preparation

### Acces Requis
- [ ] Code source (Git)
- [ ] CI/CD pipelines
- [ ] Environnements (dev, staging, prod)
- [ ] Monitoring dashboards
- [ ] Documentation existante

### Contacts
- [ ] Tech Lead / Architect
- [ ] Developpeurs seniors
- [ ] Ops / SRE
- [ ] Product Owner

### Outils
- [ ] Analyseur de code (SonarQube)
- [ ] Dependency checker (npm audit, Snyk)
- [ ] Diagramme (Mermaid, Draw.io)
```

## Questions Cles

### Architecture
- Pourquoi ces choix technologiques ?
- Quels sont les bottlenecks connus ?
- Y a-t-il des SPOFs ?

### Code
- Quelles parties du code sont les plus fragiles ?
- Ou est la logique metier critique ?
- Quels modules personne ne veut toucher ?

### Equipe
- Qui connait le mieux le systeme ?
- Quelles competences manquent ?
- Quelle est la capacite de changement ?

## Voir Aussi

- `assessment/debt-analysis` pour quantifier la dette
- `assessment/risk-assessment` pour les risques
- `strategies/` pour les options de modernisation
