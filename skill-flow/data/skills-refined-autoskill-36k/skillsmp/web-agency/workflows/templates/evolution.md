---
id: wf-evolution
name: Workflow Evolution
type: template
version: 1.1.0
description: Workflow pour l'évolution ou amélioration d'un existant
duration_range: "2-8 jours"
phases: 4
applicable_to:
  - nouvelle-feature
  - amelioration
  - optimisation
  - correction
references:
  - acceptance/matrice-positionnement.md
  - acceptance/livrables-par-workflow.md
  - acceptance/criteres-acceptation.md
---

# Workflow Evolution

> Template pour les évolutions et améliorations d'un système existant.

## Vue d'Ensemble

```
DEMANDE → SPECIFICATION → REALISATION → DEPLOIEMENT
```

| Phase | Durée | Validation |
|-------|-------|------------|
| Demande | 10% | Ticket qualifié |
| Spécification | 20% | Specs validées |
| Réalisation | 50% | Code review OK |
| Déploiement | 20% | Production stable |

---

## Phase 1: Demande

### Objectif
Qualifier et prioriser la demande.

### Activités
1. Réception de la demande
2. Clarification du besoin
3. Évaluation de l'impact
4. Priorisation

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Ticket créé** | User story formatée avec contexte | Tous |
| **Impact assessment** | Analyse impact technique et business | Tous |
| **Estimation** | Effort chiffré et validé | Tous |
| **Priorité** | Priorité assignée et justifiée | Tous |

```yaml
livrables_demande:
  ticket:
    criteres:
      - CA-DEM-001: "User story au format standard (As a... I want... So that...)"
      - CA-DEM-002: "Contexte et motivation documentés"
      - CA-DEM-003: "Critères d'acceptation définis"
      - CA-DEM-004: "Demandeur identifié"
    preuve: "Ticket dans l'outil de suivi"

  impact_assessment:
    criteres:
      - CA-DEM-010: "Impact technique évalué (code, archi, perf)"
      - CA-DEM-011: "Impact business évalué (utilisateurs, revenus)"
      - CA-DEM-012: "Dépendances identifiées"
      - CA-DEM-013: "Risques potentiels listés"
    preuve: "Section impact dans ticket"

  estimation:
    criteres:
      - CA-DEM-020: "Estimation en points ou jours/hommes"
      - CA-DEM-021: "Complexité évaluée (S/M/L/XL)"
      - CA-DEM-022: "Hypothèses documentées"
      - CA-DEM-023: "Estimation validée par tech lead"
    preuve: "Estimation dans ticket"

  priorite:
    criteres:
      - CA-DEM-030: "Priorité selon matrice impact/effort"
      - CA-DEM-031: "Justification documentée"
      - CA-DEM-032: "Slot de sprint assigné si urgent"
    preuve: "Priorité dans ticket"
```

### Critères de Sortie
- Demande comprise et acceptée
- Estimation validée
- Slot de dev planifié

---

## Phase 2: Spécification

### Objectif
Définir précisément ce qui doit être fait.

### Activités
1. Analyse d'impact technique
2. Design de la solution
3. Identification des risques
4. Validation avec demandeur

### Livrables et Critères d'Acceptation (selon complexité)

| Livrable | Simple (S/M) | Complexe (L/XL) |
|----------|--------------|-----------------|
| **User stories** | Story principale | Stories découpées |
| **Critères acceptation** | Checklist | Gherkin/BDD |
| **Design technique** | Notes techniques | ADR + diagrammes |
| **Maquettes** | Wireframe si UI | Maquettes HD |

```yaml
livrables_specification:
  user_stories:
    niveau_simple:
      criteres:
        - CA-SPEC-001: "Story principale définie"
        - CA-SPEC-002: "Critères d'acceptation listés"
      preuve: "Ticket mis à jour"
    niveau_complexe:
      criteres:
        - CA-SPEC-001: "Epic décomposée en stories"
        - CA-SPEC-002: "Dépendances entre stories identifiées"
        - CA-SPEC-003: "Ordre de réalisation défini"
        - CA-SPEC-004: "Stories indépendantes et testables"
      preuve: "Epic + stories liées"

  criteres_acceptation:
    niveau_simple:
      criteres:
        - CA-SPEC-010: "Checklist des comportements attendus"
        - CA-SPEC-011: "Cas nominaux couverts"
      preuve: "Checklist dans ticket"
    niveau_complexe:
      criteres:
        - CA-SPEC-010: "Scénarios Gherkin (Given/When/Then)"
        - CA-SPEC-011: "Cas nominaux et limites couverts"
        - CA-SPEC-012: "Cas d'erreur documentés"
        - CA-SPEC-013: "Critères non-fonctionnels définis"
      preuve: "Fichiers .feature ou specs"

  design_technique:
    niveau_simple:
      criteres:
        - CA-SPEC-020: "Approche technique documentée"
        - CA-SPEC-021: "Fichiers impactés identifiés"
      preuve: "Notes dans ticket"
    niveau_complexe:
      criteres:
        - CA-SPEC-020: "ADR pour décisions structurantes"
        - CA-SPEC-021: "Diagramme séquence si pertinent"
        - CA-SPEC-022: "Modèle de données si impact"
        - CA-SPEC-023: "Plan de migration si nécessaire"
      preuve: "ADR + diagrammes"

  maquettes:
    niveau_simple:
      criteres:
        - CA-SPEC-030: "Wireframe rapide si changement UI"
      preuve: "Sketch ou wireframe"
    niveau_complexe:
      criteres:
        - CA-SPEC-030: "Maquettes HD validées"
        - CA-SPEC-031: "États et interactions définis"
        - CA-SPEC-032: "Responsive considéré"
      preuve: "Fichiers Figma"
```

### Critères de Sortie
- Solution technique validée
- Pas de bloqueur identifié
- Demandeur en accord

---

## Phase 3: Réalisation

### Objectif
Implémenter l'évolution.

### Activités
1. Développement
2. Tests unitaires
3. Code review
4. Tests d'intégration
5. Documentation

### Livrables et Critères d'Acceptation (selon complexité)

| Livrable | Simple (S/M) | Complexe (L/XL) |
|----------|--------------|-----------------|
| **Code** | Standards respectés | + Refactoring clean |
| **Tests** | Tests unitaires | + Integration + E2E |
| **Documentation** | Inline comments | + README + API docs |
| **Code review** | 1 reviewer | 2+ reviewers |

```yaml
livrables_realisation:
  code:
    niveau_simple:
      criteres:
        - CA-REAL-001: "Code lint clean"
        - CA-REAL-002: "Standards projet respectés"
        - CA-REAL-003: "Pas de régression introduite"
      preuve: "CI verte"
    niveau_complexe:
      criteres:
        - CA-REAL-001: "Code lint clean, 0 warnings"
        - CA-REAL-002: "Patterns projet respectés"
        - CA-REAL-003: "Code refactoré si dette"
        - CA-REAL-004: "Performance validée"
      preuve: "CI + métriques"

  tests:
    niveau_simple:
      criteres:
        - CA-REAL-010: "Tests unitaires nouveaux cas"
        - CA-REAL-011: "Coverage maintenu ou amélioré"
      preuve: "Rapport coverage"
    niveau_complexe:
      criteres:
        - CA-REAL-010: "Tests unitaires exhaustifs"
        - CA-REAL-011: "Tests intégration ajoutés"
        - CA-REAL-012: "Tests E2E si parcours critique"
        - CA-REAL-013: "Coverage > 80% sur nouveau code"
      preuve: "Rapports tests complets"

  documentation:
    niveau_simple:
      criteres:
        - CA-REAL-020: "Code commenté si logique complexe"
        - CA-REAL-021: "Commit messages explicites"
      preuve: "Code + commits"
    niveau_complexe:
      criteres:
        - CA-REAL-020: "README mis à jour si nécessaire"
        - CA-REAL-021: "API documentation si endpoints"
        - CA-REAL-022: "Changelog mis à jour"
        - CA-REAL-023: "Guide utilisateur si UI majeure"
      preuve: "Documentation à jour"

  code_review:
    niveau_simple:
      criteres:
        - CA-REAL-030: "Review par 1 développeur"
        - CA-REAL-031: "Commentaires adressés"
      preuve: "PR approuvée"
    niveau_complexe:
      criteres:
        - CA-REAL-030: "Review par 2+ développeurs"
        - CA-REAL-031: "Review archi si structurant"
        - CA-REAL-032: "Tous commentaires résolus"
        - CA-REAL-033: "Approbation tech lead"
      preuve: "PR multi-approuvée"
```

### Critères de Sortie
- CI/CD vert
- Code review validée
- Prêt pour staging

---

## Phase 4: Déploiement

### Objectif
Déployer en production de manière sécurisée.

### Activités
1. Déploiement staging
2. Recette sur staging
3. Déploiement production
4. Validation post-déploiement
5. Communication

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Release notes** | Changements documentés pour utilisateurs | Tous |
| **Déploiement** | Staging puis production validés | Tous |
| **Validation** | Tests post-déploiement passants | Tous |
| **Communication** | Demandeur et stakeholders informés | Tous |

```yaml
livrables_deploiement:
  release_notes:
    criteres:
      - CA-DEP-001: "Description des changements en langage utilisateur"
      - CA-DEP-002: "Nouvelles fonctionnalités listées"
      - CA-DEP-003: "Bugs corrigés listés"
      - CA-DEP-004: "Breaking changes signalés si applicable"
    preuve: "Release notes publiées"

  deploiement:
    criteres:
      - CA-DEP-010: "Déploiement staging réussi"
      - CA-DEP-011: "Smoke tests staging OK"
      - CA-DEP-012: "Recette staging validée"
      - CA-DEP-013: "Déploiement production réussi"
      - CA-DEP-014: "Smoke tests production OK"
    preuve: "Logs déploiement + tests"

  validation:
    criteres:
      - CA-DEP-020: "Fonctionnalité accessible en production"
      - CA-DEP-021: "Pas de régression détectée"
      - CA-DEP-022: "Monitoring nominal"
      - CA-DEP-023: "Performance acceptable"
    preuve: "Validation post-deploy"

  communication:
    criteres:
      - CA-DEP-030: "Demandeur notifié de la mise en production"
      - CA-DEP-031: "Ticket mis à jour avec lien production"
      - CA-DEP-032: "Stakeholders informés si impact large"
      - CA-DEP-033: "Documentation utilisateur partagée si nouvelle feature"
    preuve: "Notifications envoyées"
```

### Critères de Sortie
- Fonctionnalité live et stable
- Demandeur notifié
- Ticket fermé

---

## Cas Particuliers

### Hotfix (urgence)

```
DIAGNOSTIC → FIX → DEPLOY → POSTMORTEM
```

- Bypass des étapes non critiques
- Déploiement accéléré
- Documentation a posteriori

### Optimisation

```
MESURE → ANALYSE → OPTIMISATION → VALIDATION
```

- Baseline avant optimisation
- Mesures comparatives après
- Objectif chiffré (ex: -30% temps de chargement)

---

## Points de Contrôle

| Checkpoint | Timing | Décision |
|------------|--------|----------|
| Go/No-Go Dev | Fin Phase 2 | Démarrer le dev |
| Go/No-Go Deploy | Fin Phase 3 | Déployer en staging |
| Go/No-Go Prod | Staging OK | Déployer en production |

## Rollback

Si problème post-déploiement:
1. Identifier le symptôme
2. Évaluer la sévérité
3. Rollback si sévérité > medium
4. Sinon, hotfix forward
