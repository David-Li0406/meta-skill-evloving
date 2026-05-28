---
id: wf-audit
name: Workflow Audit
type: template
version: 1.1.0
description: Workflow pour les audits, diagnostics et analyses
duration_range: "3-10 jours"
phases: 4
applicable_to:
  - audit-technique
  - audit-ux
  - audit-seo
  - audit-securite
  - audit-accessibilite
  - diagnostic
  - benchmark
references:
  - acceptance/matrice-positionnement.md
  - acceptance/livrables-par-workflow.md
  - acceptance/criteres-acceptation.md
---

# Workflow Audit

> Template pour les missions d'audit, diagnostic et analyse.

## Vue d'Ensemble

```
CADRAGE → COLLECTE → ANALYSE → RESTITUTION
```

| Phase | Durée | Validation |
|-------|-------|------------|
| Cadrage | 10-15% | Périmètre validé |
| Collecte | 25-30% | Données complètes |
| Analyse | 35-40% | Findings documentés |
| Restitution | 20-25% | Rapport livré |

---

## Phase 1: Cadrage

### Objectif
Définir le périmètre et les objectifs de l'audit.

### Activités
1. Comprendre le contexte et les enjeux
2. Définir les objectifs de l'audit
3. Identifier le périmètre (inclus/exclus)
4. Planifier les accès nécessaires

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Périmètre audit** | Scope défini avec inclusions/exclusions | Tous |
| **Grille d'évaluation** | Critères et métriques définis | Tous |
| **Planning** | Jalons et livrables datés | Tous |
| **Accès** | Tous accès nécessaires obtenus | Tous |

```yaml
livrables_cadrage:
  perimetre_audit:
    criteres:
      - CA-CAD-001: "Objectifs de l'audit clairement définis"
      - CA-CAD-002: "Périmètre inclus documenté (pages, fonctionnalités, systèmes)"
      - CA-CAD-003: "Exclusions explicitement listées"
      - CA-CAD-004: "Critères de succès de l'audit définis"
    preuve: "Note de cadrage signée"

  grille_evaluation:
    criteres:
      - CA-CAD-010: "Critères d'évaluation listés par domaine"
      - CA-CAD-011: "Échelle de notation définie (ex: 1-5, A-F)"
      - CA-CAD-012: "Seuils de conformité établis"
      - CA-CAD-013: "Pondération des critères si applicable"
    preuve: "Grille d'évaluation"

  planning:
    criteres:
      - CA-CAD-020: "Phases de l'audit planifiées"
      - CA-CAD-021: "Interviews/ateliers planifiés"
      - CA-CAD-022: "Date de restitution fixée"
      - CA-CAD-023: "Ressources identifiées (auditeur, client)"
    preuve: "Planning partagé"

  acces:
    criteres:
      - CA-CAD-030: "Liste des accès requis documentée"
      - CA-CAD-031: "Accès environnements obtenus"
      - CA-CAD-032: "Accès outils analytics obtenus"
      - CA-CAD-033: "Contacts techniques identifiés"
    preuve: "Checklist accès validée"
```

### Critères de Sortie
- Objectifs clairs et validés
- Accès obtenus
- Planning accepté

---

## Phase 2: Collecte

### Objectif
Rassembler toutes les données nécessaires à l'analyse.

### Activités
1. Collecte documentaire
2. Interviews stakeholders
3. Analyse automatisée (outils)
4. Observation/tests manuels

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Données brutes** | Données exhaustives collectées | Tous |
| **Screenshots/preuves** | Captures annotées des constats | Tous |
| **Logs outils** | Rapports outils automatisés | Tous |
| **Comptes-rendus** | Synthèse interviews documentée | Tous |

```yaml
livrables_collecte:
  donnees_brutes:
    criteres:
      - CA-COL-001: "Données quantitatives collectées (analytics, logs)"
      - CA-COL-002: "Données qualitatives collectées (interviews, observations)"
      - CA-COL-003: "Couverture du périmètre > 90%"
      - CA-COL-004: "Données datées et sourcées"
    preuve: "Dossier données brutes"

  screenshots_preuves:
    criteres:
      - CA-COL-010: "Captures d'écran des problèmes identifiés"
      - CA-COL-011: "Annotations explicatives ajoutées"
      - CA-COL-012: "Contexte de capture documenté (navigateur, device)"
      - CA-COL-013: "Organisation par catégorie/critère"
    preuve: "Dossier captures annotées"

  logs_outils:
    criteres:
      - CA-COL-020: "Rapports Lighthouse/PageSpeed exportés"
      - CA-COL-021: "Scans sécurité (OWASP ZAP, etc.) exécutés"
      - CA-COL-022: "Audits accessibilité (axe, WAVE) exportés"
      - CA-COL-023: "Crawl SEO si applicable"
    preuve: "Rapports outils"

  comptes_rendus_interviews:
    criteres:
      - CA-COL-030: "Interviews stakeholders clés réalisées"
      - CA-COL-031: "Pain points documentés"
      - CA-COL-032: "Attentes et priorités notées"
      - CA-COL-033: "Synthèse validée par interviewé si sensible"
    preuve: "CR interviews"
```

### Critères de Sortie
- Données suffisantes pour analyse
- Pas de zone aveugle majeure
- Preuves documentées

---

## Phase 3: Analyse

### Objectif
Analyser les données et identifier les findings.

### Activités
1. Analyse des données collectées
2. Identification des problèmes
3. Évaluation de la sévérité
4. Recherche des causes racines
5. Formulation des recommandations

### Livrables et Critères d'Acceptation (selon niveau d'audit)

| Livrable | Minimal | Standard | Premium |
|----------|---------|----------|---------|
| **Synthèse par critère** | Note globale | Notes détaillées | + Tendances |
| **Score global** | Score simple | Score pondéré | + Benchmark |
| **Points critiques** | Top 5 | Top 10 priorisés | Exhaustif |
| **Recommandations** | Quick wins | Plan complet | + Roadmap |

```yaml
livrables_analyse:
  synthese_par_critere:
    niveau_minimal:
      criteres:
        - CA-ANAL-001: "Chaque critère évalué"
        - CA-ANAL-002: "Note/score attribué"
      preuve: "Tableau synthèse"
    niveau_standard:
      criteres:
        - CA-ANAL-001: "Chaque critère évalué avec justification"
        - CA-ANAL-002: "Points forts et faibles identifiés"
        - CA-ANAL-003: "Exemples concrets fournis"
      preuve: "Synthèse détaillée"
    niveau_premium:
      criteres:
        - CA-ANAL-001: "Analyse tendancielle si données historiques"
        - CA-ANAL-002: "Comparaison avec benchmarks sectoriels"
        - CA-ANAL-003: "Projection si aucune action"
      preuve: "Analyse avancée"

  score_global:
    niveau_minimal:
      criteres:
        - CA-ANAL-010: "Score global calculé"
        - CA-ANAL-011: "Interprétation du score fournie"
      preuve: "Score + interprétation"
    niveau_standard:
      criteres:
        - CA-ANAL-010: "Score pondéré selon importance critères"
        - CA-ANAL-011: "Scores par domaine"
        - CA-ANAL-012: "Visualisation graphique"
      preuve: "Dashboard scores"
    niveau_premium:
      criteres:
        - CA-ANAL-010: "Benchmark vs concurrents/secteur"
        - CA-ANAL-011: "Positionnement marché"
        - CA-ANAL-012: "Évolution recommandée"
      preuve: "Benchmark complet"

  points_critiques:
    niveau_minimal:
      criteres:
        - CA-ANAL-020: "Top 5 problèmes identifiés"
        - CA-ANAL-021: "Impact estimé pour chaque"
      preuve: "Liste priorisée"
    niveau_standard:
      criteres:
        - CA-ANAL-020: "Top 10 problèmes avec sévérité"
        - CA-ANAL-021: "Causes racines analysées"
        - CA-ANAL-022: "Effort de correction estimé"
      preuve: "Analyse détaillée"
    niveau_premium:
      criteres:
        - CA-ANAL-020: "Inventaire exhaustif des findings"
        - CA-ANAL-021: "Matrice impact/effort"
        - CA-ANAL-022: "Dépendances entre corrections"
      preuve: "Registre complet findings"

  recommandations:
    niveau_minimal:
      criteres:
        - CA-ANAL-030: "Quick wins identifiés (< 1 jour)"
        - CA-ANAL-031: "Actions immédiates listées"
      preuve: "Liste quick wins"
    niveau_standard:
      criteres:
        - CA-ANAL-030: "Plan d'action court/moyen terme"
        - CA-ANAL-031: "Priorisation par ROI"
        - CA-ANAL-032: "Estimation efforts par action"
      preuve: "Plan d'action"
    niveau_premium:
      criteres:
        - CA-ANAL-030: "Roadmap 6-12 mois"
        - CA-ANAL-031: "Jalons et objectifs mesurables"
        - CA-ANAL-032: "Budget estimatif"
        - CA-ANAL-033: "KPIs de suivi définis"
      preuve: "Roadmap complète"
```

### Critères de Sortie
- Findings validés et priorisés
- Recommandations actionnables
- Causes racines identifiées

---

## Phase 4: Restitution

### Objectif
Présenter les résultats et le plan d'action.

### Activités
1. Rédaction du rapport d'audit
2. Préparation de la présentation
3. Restitution aux stakeholders
4. Session Q&A
5. Remise du plan d'action

### Livrables et Critères d'Acceptation (selon niveau d'audit)

| Livrable | Minimal | Standard | Premium |
|----------|---------|----------|---------|
| **Rapport audit** | Synthèse 5-10 pages | Rapport complet | + Annexes détaillées |
| **Présentation** | Slides clés | Présentation complète | + Workshop |
| **Plan remédiation** | Liste priorisée | Plan phasé | + Accompagnement |

```yaml
livrables_restitution:
  rapport_audit:
    niveau_minimal:
      criteres:
        - CA-REST-001: "Executive summary (1-2 pages)"
        - CA-REST-002: "Synthèse des findings clés"
        - CA-REST-003: "Recommandations principales"
      preuve: "Rapport PDF 5-10 pages"
    niveau_standard:
      criteres:
        - CA-REST-001: "Rapport structuré complet"
        - CA-REST-002: "Détail par critère avec preuves"
        - CA-REST-003: "Visualisations et graphiques"
        - CA-REST-004: "Plan d'action intégré"
      preuve: "Rapport PDF 20-40 pages"
    niveau_premium:
      criteres:
        - CA-REST-001: "Rapport complet + annexes techniques"
        - CA-REST-002: "Données brutes fournies"
        - CA-REST-003: "Accès dashboard interactif si applicable"
        - CA-REST-004: "Templates et checklists fournis"
      preuve: "Rapport + annexes + assets"

  presentation:
    niveau_minimal:
      criteres:
        - CA-REST-010: "Slides executive (10-15)"
        - CA-REST-011: "Points clés visuels"
      preuve: "Deck présentation"
    niveau_standard:
      criteres:
        - CA-REST-010: "Présentation complète (20-30 slides)"
        - CA-REST-011: "Session Q&A structurée"
        - CA-REST-012: "Démonstrations si pertinent"
      preuve: "Deck + CR restitution"
    niveau_premium:
      criteres:
        - CA-REST-010: "Présentation C-level + version technique"
        - CA-REST-011: "Workshop priorisation avec équipes"
        - CA-REST-012: "Session hands-on si pertinent"
      preuve: "Decks multiples + CR workshop"

  plan_remediation:
    niveau_minimal:
      criteres:
        - CA-REST-020: "Liste des actions recommandées"
        - CA-REST-021: "Priorisation haute/moyenne/basse"
      preuve: "Liste priorisée"
    niveau_standard:
      criteres:
        - CA-REST-020: "Plan phasé (court/moyen/long terme)"
        - CA-REST-021: "Estimations effort par action"
        - CA-REST-022: "Responsables suggérés"
      preuve: "Plan d'action structuré"
    niveau_premium:
      criteres:
        - CA-REST-020: "Roadmap détaillée avec jalons"
        - CA-REST-021: "Budget prévisionnel"
        - CA-REST-022: "Proposition accompagnement"
        - CA-REST-023: "KPIs de suivi et tableau de bord"
      preuve: "Roadmap + proposition commerciale"
```

### Critères de Sortie
- Rapport remis et présenté
- Plan d'action validé
- Questions répondues
- Prochaines étapes définies

---

## Grille de Sévérité

| Niveau | Label | Description | Action |
|--------|-------|-------------|--------|
| 1 | Critique | Risque immédiat, bloquant | Correction urgente |
| 2 | Majeur | Impact fort, non bloquant | Correction < 1 mois |
| 3 | Modéré | Impact moyen | Correction < 3 mois |
| 4 | Mineur | Impact faible | Backlog |
| 5 | Amélioration | Optimisation | Nice to have |

---

## Templates de Findings

### Finding Standard

```markdown
## [SEVERITY] Titre du Finding

**Constat:** Description factuelle du problème observé.

**Impact:** Conséquences pour l'utilisateur/business.

**Cause:** Analyse de la cause racine.

**Recommandation:** Action corrective proposée.

**Effort:** [S/M/L/XL] - Estimation de l'effort de correction.
```

---

## Types d'Audit Spécialisés

### Audit Technique
- Performance (Core Web Vitals)
- Sécurité (OWASP)
- Code quality (dette technique)
- Infrastructure

### Audit UX
- Heuristiques Nielsen
- Parcours utilisateur
- Tests utilisateurs
- Analytics comportemental

### Audit SEO
- Technique (crawlabilité)
- Contenu (mots-clés)
- Popularité (backlinks)
- Local (GMB)

### Audit Accessibilité
- WCAG 2.1 AA/AAA
- Tests assistifs
- Conformité légale
