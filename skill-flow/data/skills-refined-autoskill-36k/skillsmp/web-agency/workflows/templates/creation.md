---
id: wf-creation
name: Workflow Création
type: template
version: 1.1.0
description: Workflow pour la création from scratch d'un livrable
duration_range: "5-15 jours"
phases: 4
applicable_to:
  - nouveau-projet
  - nouvelle-fonctionnalite
  - nouveau-composant
references:
  - acceptance/matrice-positionnement.md
  - acceptance/livrables-par-workflow.md
  - acceptance/criteres-acceptation.md
---

# Workflow Création

> Template pour tout projet de création partant de zéro.

## Vue d'Ensemble

```
BRIEF → CONCEPTION → PRODUCTION → LIVRAISON
```

| Phase | Durée | Validation |
|-------|-------|------------|
| Brief | 10-15% | Cahier des charges signé |
| Conception | 25-30% | Maquettes/specs validées |
| Production | 45-50% | Livrable fonctionnel |
| Livraison | 10-15% | PV de recette signé |

---

## Phase 1: Brief

### Objectif
Comprendre le besoin et définir le périmètre.

### Activités
1. Réunion de cadrage client
2. Collecte des informations existantes
3. Analyse des contraintes (budget, délai, technique)
4. **Positionnement Triangle Projet** (Budget/Qualité/Délai)
5. Rédaction du cahier des charges

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Compte-rendu de réunion** | Participants, décisions, actions listés | Tous |
| **Matrice de positionnement** | Triangle rempli, signé par client | Tous |
| **Cahier des charges** | Périmètre défini, objectifs mesurables | Tous |
| **Planning macro** | Jalons identifiés, réaliste | Tous |
| **Devis détaillé** | Postes chiffrés, hypothèses documentées | Tous |

```yaml
livrables_brief:
  matrice_positionnement:
    criteres:
      - CA-BRIEF-001: "Triangle Budget/Qualité/Délai rempli"
      - CA-BRIEF-002: "Contraintes absolues identifiées"
      - CA-BRIEF-003: "Signature client obtenue"
    preuve: "Document signé"

  cahier_charges:
    criteres:
      - CA-BRIEF-010: "Contexte et objectifs documentés"
      - CA-BRIEF-011: "Périmètre fonctionnel défini (in/out)"
      - CA-BRIEF-012: "Critères de succès mesurables"
      - CA-BRIEF-013: "Contraintes techniques listées"
    preuve: "Document validé"

  planning:
    criteres:
      - CA-BRIEF-020: "Phases et jalons identifiés"
      - CA-BRIEF-021: "Points de validation planifiés"
      - CA-BRIEF-022: "Ressources identifiées"
    preuve: "Gantt ou timeline"

  devis:
    criteres:
      - CA-BRIEF-030: "Postes budgétaires détaillés"
      - CA-BRIEF-031: "Hypothèses documentées"
      - CA-BRIEF-032: "Exclusions explicites"
      - CA-BRIEF-033: "Marge erreur < 20%"
    preuve: "Devis signé"
```

### Critères de Sortie
- Client a signé le cahier des charges
- Matrice de positionnement validée
- Budget et planning validés

---

## Phase 2: Conception

### Objectif
Concevoir la solution avant production.

### Activités
1. Recherche et benchmark
2. Esquisse des concepts
3. Itérations avec le client
4. Finalisation des spécifications

### Livrables et Critères d'Acceptation (selon positionnement)

| Livrable | Minimal | Standard | Premium |
|----------|---------|----------|---------|
| **Maquettes** | Wireframes | HD responsive | Pixel-perfect + DS |
| **Specs techniques** | Schéma archi | C4 + OpenAPI | + POC technique |
| **Prototype** | - | Cliquable | Interactif animé |
| **ADR** | - | Choix majeurs | Complet |

```yaml
livrables_conception:
  maquettes:
    niveau_minimal:
      criteres:
        - CA-CONC-001: "Wireframes pages principales"
        - CA-CONC-002: "1 résolution cible"
      preuve: "Fichiers Figma/Sketch"
    niveau_standard:
      criteres:
        - CA-CONC-001: "Maquettes HD toutes pages"
        - CA-CONC-002: "3 breakpoints (mobile/tablet/desktop)"
        - CA-CONC-003: "Design system tokens définis"
      preuve: "Fichiers Figma + DS"
    niveau_premium:
      criteres:
        - CA-CONC-001: "Maquettes pixel-perfect"
        - CA-CONC-002: "5 breakpoints"
        - CA-CONC-003: "Design system complet"
        - CA-CONC-004: "Micro-interactions spécifiées"
      preuve: "Fichiers Figma + DS + prototypes"

  specifications:
    niveau_minimal:
      criteres:
        - CA-CONC-010: "Schéma architecture global"
        - CA-CONC-011: "Liste des endpoints"
      preuve: "Document technique"
    niveau_standard:
      criteres:
        - CA-CONC-010: "Diagrammes C4 (context, container)"
        - CA-CONC-011: "Specs API OpenAPI 3.0"
        - CA-CONC-012: "Modèle de données"
      preuve: "Specs + OpenAPI"
    niveau_premium:
      criteres:
        - CA-CONC-010: "C4 complet (+ component)"
        - CA-CONC-011: "OpenAPI + exemples"
        - CA-CONC-012: "Modèle données + migrations"
        - CA-CONC-013: "POC technique validé"
      preuve: "Specs + POC fonctionnel"
```

### Critères de Sortie
- Conception validée par le client (selon niveau positionné)
- Aucune zone d'ombre sur le périmètre
- ADR documentés pour choix structurants

---

## Phase 3: Production

### Objectif
Réaliser le livrable selon les specs validées.

### Activités
1. Mise en place environnement
2. Production itérative
3. Tests internes
4. Corrections et ajustements

### Livrables et Critères d'Acceptation (selon positionnement)

| Livrable | Minimal | Standard | Premium |
|----------|---------|----------|---------|
| **Code** | Lint OK, 40% coverage | 70% coverage, 0 warnings | 85%+, mutation testing |
| **Tests** | Chemins critiques | Pyramide complète | + Tests mutation |
| **Performance** | CWV "needs improvement" | CWV "good" | Top 10% |
| **Accessibilité** | WCAG A | WCAG AA | WCAG AAA |
| **Sécurité** | OWASP Top 10 | OWASP complet | + Audit externe |
| **Documentation** | README + inline | + API docs | Exhaustive |

```yaml
livrables_production:
  code:
    niveau_minimal:
      criteres:
        - CA-CODE-001: "0 erreurs lint"
        - CA-CODE-002: "Coverage > 40%"
        - CA-CODE-003: "0 vulnérabilités critiques"
      preuve: "Rapports CI"
    niveau_standard:
      criteres:
        - CA-CODE-001: "0 erreurs, < 10 warnings lint"
        - CA-CODE-002: "Coverage > 70%"
        - CA-CODE-003: "0 vulnérabilités high/critical"
        - CA-CODE-004: "Code review approuvée"
      preuve: "Rapports CI + PR merged"
    niveau_premium:
      criteres:
        - CA-CODE-001: "Lint clean"
        - CA-CODE-002: "Coverage > 85%, mutation > 60%"
        - CA-CODE-003: "0 vulnérabilités"
        - CA-CODE-004: "Revue architecture validée"
      preuve: "Rapports complets + audit"

  performance:
    niveau_minimal:
      criteres:
        - CA-PERF-001: "LCP < 4s, FID < 300ms, CLS < 0.25"
      preuve: "Lighthouse"
    niveau_standard:
      criteres:
        - CA-PERF-001: "LCP < 2.5s, FID < 100ms, CLS < 0.1"
        - CA-PERF-002: "Bundle JS < 250KB"
      preuve: "Lighthouse + bundle analysis"
    niveau_premium:
      criteres:
        - CA-PERF-001: "LCP < 1.5s, FID < 50ms, CLS < 0.05"
        - CA-PERF-002: "Bundle JS < 150KB"
        - CA-PERF-003: "TTFB < 200ms"
      preuve: "WebPageTest + monitoring"

  accessibilite:
    niveau_minimal:
      criteres:
        - CA-A11Y-001: "0 erreurs WCAG A (axe-core)"
      preuve: "Rapport axe"
    niveau_standard:
      criteres:
        - CA-A11Y-001: "0 erreurs WCAG AA"
        - CA-A11Y-002: "Navigation clavier validée"
      preuve: "Rapport axe + test manuel"
    niveau_premium:
      criteres:
        - CA-A11Y-001: "WCAG AAA (< 5 erreurs)"
        - CA-A11Y-002: "Test lecteur écran validé"
        - CA-A11Y-003: "Audit expert passé"
      preuve: "Rapports + audit"

  securite:
    niveau_minimal:
      criteres:
        - CA-SEC-001: "OWASP Top 10 protégé"
        - CA-SEC-002: "Headers security D+"
      preuve: "Scan OWASP ZAP"
    niveau_standard:
      criteres:
        - CA-SEC-001: "OWASP ASVS niveau 1"
        - CA-SEC-002: "Headers security B+"
        - CA-SEC-003: "RGPD conforme"
      preuve: "Scan + checklist RGPD"
    niveau_premium:
      criteres:
        - CA-SEC-001: "OWASP ASVS niveau 2"
        - CA-SEC-002: "Headers security A+"
        - CA-SEC-003: "Pentest externe passé"
      preuve: "Rapport pentest"
```

### Critères de Sortie
- Tous les critères du niveau positionné validés
- Environnement de recette accessible
- Prêt pour recette client

---

## Phase 4: Livraison

### Objectif
Livrer et transférer au client.

### Activités
1. Présentation au client
2. Formation si nécessaire
3. Recette client
4. Corrections finales
5. Mise en production

### Livrables et Critères d'Acceptation (selon positionnement)

| Livrable | Minimal | Standard | Premium |
|----------|---------|----------|---------|
| **Production** | Smoke tests OK | + Monitoring actif | + Alerting configuré |
| **Documentation** | FAQ 10 questions | Guide utilisateur | Base de connaissances |
| **Formation** | - | Tutoriels vidéo (3) | Formation complète |
| **Support** | Email | + SLA défini | + Support prioritaire |

```yaml
livrables_livraison:
  production:
    niveau_minimal:
      criteres:
        - CA-LIV-001: "Smoke tests passants"
        - CA-LIV-002: "SSL valide"
        - CA-LIV-003: "DNS configuré"
      preuve: "Checklist go-live"
    niveau_standard:
      criteres:
        - CA-LIV-001: "Smoke tests passants"
        - CA-LIV-002: "Monitoring actif (uptime)"
        - CA-LIV-003: "Backups configurés"
        - CA-LIV-004: "Logs centralisés"
      preuve: "Checklist + accès monitoring"
    niveau_premium:
      criteres:
        - CA-LIV-001: "Tests complets passants"
        - CA-LIV-002: "APM configuré"
        - CA-LIV-003: "Alerting multi-canal"
        - CA-LIV-004: "Disaster recovery testé"
      preuve: "Runbooks + tests DR"

  documentation_utilisateur:
    niveau_minimal:
      criteres:
        - CA-LIV-010: "FAQ 10 questions/réponses"
      preuve: "Document FAQ"
    niveau_standard:
      criteres:
        - CA-LIV-010: "Guide utilisateur complet"
        - CA-LIV-011: "Tutoriels vidéo (3 minimum)"
        - CA-LIV-012: "Screenshots annotés"
      preuve: "Guide + vidéos publiées"
    niveau_premium:
      criteres:
        - CA-LIV-010: "Base de connaissances structurée"
        - CA-LIV-011: "Tutoriels vidéo tous parcours"
        - CA-LIV-012: "Recherche intégrée"
        - CA-LIV-013: "Chatbot support (optionnel)"
      preuve: "KB accessible + analytics"

  pv_recette:
    tous_niveaux:
      criteres:
        - CA-LIV-020: "Liste fonctionnalités validées"
        - CA-LIV-021: "Anomalies résiduelles documentées"
        - CA-LIV-022: "Plan de correction si applicable"
        - CA-LIV-023: "Signatures client + agence"
      preuve: "PV signé"

  transfert:
    tous_niveaux:
      criteres:
        - CA-LIV-030: "Credentials transmis de façon sécurisée"
        - CA-LIV-031: "Accès environnements confirmés"
        - CA-LIV-032: "Contacts support communiqués"
      preuve: "Email de transfert"
```

### Critères de Sortie
- PV de recette signé
- Documentation livrée selon niveau positionné
- Client autonome sur le livrable
- Support/garantie activé

---

## Points de Contrôle

| Checkpoint | Timing | Décision |
|------------|--------|----------|
| Go/No-Go Brief | Fin Phase 1 | Continuer ou ajuster périmètre |
| Go/No-Go Conception | Fin Phase 2 | Valider avant production |
| Go/No-Go Recette | Fin Phase 3 | Prêt pour livraison client |

## Escalade

Escalader vers supervision humaine si:
- Dépassement > 20% du budget
- Retard > 1 semaine
- Changement de périmètre significatif
- Conflit avec le client
