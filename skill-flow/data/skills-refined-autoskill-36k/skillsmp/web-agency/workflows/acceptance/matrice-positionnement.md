# Matrice de Positionnement Client

> **Triangle Projet** : Budget, Qualité, Délai - On ne peut maximiser que 2 sur 3.

## Principe Fondamental

```
        QUALITÉ
           △
          /|\
         / | \
        /  |  \
       /   |   \
      /    |    \
     /_____|_____\
  BUDGET ◄────► DÉLAI
```

**Règle d'or** : Le client choisit 2 priorités, la 3ème devient la variable d'ajustement.

---

## Matrice de Positionnement

### Profils Types

| Profil | Priorité 1 | Priorité 2 | Variable | Caractéristiques |
|--------|------------|------------|----------|------------------|
| **Startup MVP** | Délai | Budget | Qualité | Livraison rapide, budget serré, dette technique acceptable |
| **Enterprise** | Qualité | Budget | Délai | Standards élevés, ROI maîtrisé, planning flexible |
| **Urgence Marché** | Délai | Qualité | Budget | Time-to-market critique, pas de compromis qualité |
| **Artisan** | Qualité | Délai | Budget | Excellence technique, deadlines respectées |
| **Économique** | Budget | Délai | Qualité | Contrainte financière forte, MVP acceptable |
| **Premium** | Qualité | Budget | Délai | Haut de gamme, investissement justifié |

---

## Grille d'Évaluation Client

```yaml
positionnement_client:
  projet: "[Nom du projet]"
  date: "[Date]"

  # Le client attribue 100 points entre les 3 critères
  # Minimum 10 points par critère, maximum 60 points
  repartition:
    budget: 0      # /100 - Importance maîtrise coûts
    qualite: 0     # /100 - Importance excellence technique
    delai: 0       # /100 - Importance respect planning

  # Contraintes absolues (non négociables)
  contraintes:
    budget_max: null        # € - Plafond absolu
    date_limite: null       # Date - Deadline impérative
    exigences_qualite: []   # Standards obligatoires (RGPD, WCAG, etc.)

  # Flexibilités acceptées
  flexibilites:
    budget_flexible: false   # Peut-on dépasser de 10-20% ?
    delai_flexible: false    # Peut-on décaler de 1-2 semaines ?
    scope_flexible: false    # Peut-on réduire le périmètre ?
```

---

## Impact sur les Livrables par Workflow

> Chaque workflow a ses propres livrables. Le niveau de chaque livrable dépend du positionnement client.

---

### wf-creation : Projet de Création

#### Matrice Livrables × Profils

| Livrable | Startup MVP | Enterprise | Urgence Marché | Artisan | Économique | Premium |
|----------|-------------|------------|----------------|---------|------------|---------|
| **BRIEF** |
| Cahier des charges | Simplifié | Détaillé | Simplifié | Détaillé | Simplifié | Exhaustif |
| Planning | Macro | Détaillé | Macro | Détaillé | Macro | Gantt complet |
| **CONCEPTION** |
| Maquettes | Wireframes | HD + DS | HD | HD + DS | Wireframes | Pixel-perfect |
| Specs techniques | Schéma | C4 + OpenAPI | C4 | C4 + OpenAPI | Schéma | C4 + POC |
| Prototype | - | Cliquable | Cliquable | Cliquable | - | Interactif |
| **PRODUCTION** |
| Tests | 40% critiques | 80% pyramide | 70% auto | 80% pyramide | 40% critiques | 85% + mutation |
| Performance | Acceptable | Optimale | Optimale | Optimale | Acceptable | Exceptionnelle |
| Accessibilité | WCAG A | WCAG AA | WCAG AA | WCAG AA | WCAG A | WCAG AAA |
| Sécurité | Top 10 | Audit complet | OWASP complet | Audit complet | Top 10 | Pentest |
| Documentation | README | Complète | Essentielle | Complète | README | Exhaustive |
| **LIVRAISON** |
| Formation | FAQ | Guide + vidéos | Guide | Guide + vidéos | FAQ | Formation complète |
| Monitoring | Uptime | APM + alerting | APM | APM + alerting | Uptime | Full observabilité |
| Support | Email | SLA défini | SLA strict | SLA défini | Email | Prioritaire |

```yaml
wf_creation_profils:
  startup_mvp:
    brief:
      cahier_charges: simplifié
      planning: macro
    conception:
      maquettes: wireframes
      specs: schema_simple
      prototype: non
    production:
      tests: 40%_critiques
      performance: acceptable
      accessibilite: wcag_a
      securite: owasp_top10
      documentation: readme
    livraison:
      formation: faq
      monitoring: uptime
      support: email

  enterprise:
    brief:
      cahier_charges: détaillé
      planning: détaillé
    conception:
      maquettes: hd_design_system
      specs: c4_openapi
      prototype: cliquable
    production:
      tests: 80%_pyramide
      performance: optimale
      accessibilite: wcag_aa
      securite: audit_complet
      documentation: complète
    livraison:
      formation: guide_videos
      monitoring: apm_alerting
      support: sla_défini

  urgence_marche:
    brief:
      cahier_charges: simplifié
      planning: macro
    conception:
      maquettes: hd
      specs: c4
      prototype: cliquable
    production:
      tests: 70%_auto
      performance: optimale
      accessibilite: wcag_aa
      securite: owasp_complet
      documentation: essentielle
    livraison:
      formation: guide
      monitoring: apm
      support: sla_strict
```

---

### wf-refonte : Projet de Refonte

#### Matrice Livrables × Profils

| Livrable | Startup MVP | Enterprise | Urgence Marché | Artisan | Économique | Premium |
|----------|-------------|------------|----------------|---------|------------|---------|
| **AUDIT** |
| Rapport existant | Synthèse | Exhaustif | Synthèse | Exhaustif | Synthèse | Exhaustif |
| Inventaire contenu | Automatisé | Manuel + auto | Automatisé | Manuel + auto | Automatisé | Complet annoté |
| Analyse dette | Top 10 issues | Complète | Top 10 issues | Complète | Top 10 issues | Complète + roadmap |
| **ANALYSE** |
| Gap analysis | Fonctionnel | Multi-dimensionnel | Fonctionnel | Multi-dimensionnel | Fonctionnel | 360° |
| Plan migration | Simple | Détaillé phasé | Simple | Détaillé phasé | Simple | Avec rollback |
| Matrice traçabilité | URLs critiques | Toutes URLs | URLs critiques | Toutes URLs | URLs critiques | URLs + contenus |
| **MIGRATION** |
| Scripts | Basiques | Robustes + logs | Basiques | Robustes + logs | Basiques | Idempotents + DR |
| Validation données | Comptage | Intégrité | Comptage | Intégrité | Comptage | Intégrité + métier |
| Redirections | 301 critiques | 301 complètes | 301 critiques | 301 complètes | 301 critiques | 301 + monitoring |
| **BASCULE** |
| Plan rollback | Manuel | Automatisé | Automatisé | Automatisé | Manuel | Testé + documenté |
| Communication | Email | Multi-canal | Multi-canal | Multi-canal | Email | Campagne complète |

```yaml
wf_refonte_profils:
  startup_mvp:
    audit:
      rapport: synthèse_5_pages
      inventaire: automatisé_screaming_frog
      dette_technique: top_10_issues
    analyse:
      gap_analysis: fonctionnel_uniquement
      plan_migration: simple
      tracabilite: urls_critiques
    migration:
      scripts: basiques
      validation: comptage_avant_après
      redirections: 301_critiques
    bascule:
      rollback: manuel
      communication: email_simple

  enterprise:
    audit:
      rapport: exhaustif_50_pages
      inventaire: manuel_plus_auto
      dette_technique: complète_priorisée
    analyse:
      gap_analysis: multi_dimensionnel
      plan_migration: détaillé_phasé
      tracabilite: toutes_urls
    migration:
      scripts: robustes_logs_rollback
      validation: intégrité_referentielle
      redirections: 301_complètes_monitoring
    bascule:
      rollback: automatisé_testé
      communication: multi_canal
```

---

### wf-evolution : Évolution Fonctionnelle

#### Matrice Livrables × Profils

| Livrable | Startup MVP | Enterprise | Urgence Marché | Artisan | Économique | Premium |
|----------|-------------|------------|----------------|---------|------------|---------|
| **DEMANDE** |
| Ticket | Titre + description | Template complet | Titre + description | Template complet | Titre + description | Template + impacts |
| Impact assessment | Optionnel | Obligatoire | Optionnel | Obligatoire | Optionnel | Détaillé |
| Estimation | T-shirt | Heures | T-shirt | Heures | T-shirt | Heures + risques |
| **SPECIFICATION** |
| User stories | Informelle | Given/When/Then | Informelle | Given/When/Then | Informelle | BDD complet |
| Critères acceptation | Implicites | Explicites | Implicites | Explicites | Implicites | Testables auto |
| Design | Croquis | Maquette | Croquis | Maquette | Croquis | Maquette + proto |
| **RÉALISATION** |
| Code review | Automatique | Manuelle | Automatique | Manuelle | Automatique | Manuelle + archi |
| Tests | Smoke | Couverture feature | Smoke | Couverture feature | Smoke | Couverture + régression |
| Documentation | Commit message | Changelog + docs | Commit message | Changelog + docs | Commit message | Changelog + ADR |
| **DÉPLOIEMENT** |
| Release notes | Interne | Client | Interne | Client | Interne | Client + public |
| Déploiement | Direct | Blue/green | Direct | Blue/green | Direct | Canary |
| Validation | Smoke tests | Tests complets | Smoke tests | Tests complets | Smoke tests | Tests + monitoring |

```yaml
wf_evolution_profils:
  startup_mvp:
    demande:
      ticket: titre_description
      impact: optionnel
      estimation: t_shirt
    specification:
      user_stories: informelles
      criteres: implicites
      design: croquis_optionnel
    realisation:
      code_review: automatique_lint
      tests: smoke_only
      documentation: commit_message
    deploiement:
      release_notes: interne
      strategie: direct_push
      validation: smoke_tests

  enterprise:
    demande:
      ticket: template_complet
      impact: obligatoire_documenté
      estimation: heures_détaillées
    specification:
      user_stories: given_when_then
      criteres: explicites_testables
      design: maquette_validée
    realisation:
      code_review: manuelle_obligatoire
      tests: couverture_feature_80%
      documentation: changelog_docs
    deploiement:
      release_notes: client_formatées
      strategie: blue_green
      validation: tests_complets_monitoring
```

---

### wf-audit : Mission d'Audit

#### Matrice Livrables × Profils

| Livrable | Startup MVP | Enterprise | Urgence Marché | Artisan | Économique | Premium |
|----------|-------------|------------|----------------|---------|------------|---------|
| **CADRAGE** |
| Périmètre | Verbal | Documenté signé | Verbal | Documenté signé | Verbal | Contrat détaillé |
| Grille évaluation | Standard | Personnalisée | Standard | Personnalisée | Standard | Sur-mesure |
| Planning | Indicatif | Engagé | Indicatif | Engagé | Indicatif | Engagé + jalons |
| **COLLECTE** |
| Données | Automatisé | Auto + manuel | Automatisé | Auto + manuel | Automatisé | Exhaustif |
| Preuves | Screenshots | Screenshots annotés | Screenshots | Screenshots annotés | Screenshots | Vidéos + logs |
| Outils | Gratuits | Premium | Gratuits | Premium | Gratuits | Enterprise |
| **ANALYSE** |
| Profondeur | Surface | Approfondie | Surface | Approfondie | Surface | Expert |
| Benchmark | Optionnel | 3-5 concurrents | Optionnel | 3-5 concurrents | Optionnel | Secteur complet |
| Score | Global | Par catégorie | Global | Par catégorie | Global | Pondéré personnalisé |
| **RESTITUTION** |
| Rapport | 5 pages | 20+ pages | 5 pages | 20+ pages | 5 pages | 50+ pages |
| Présentation | - | 1h avec Q&A | - | 1h avec Q&A | - | Atelier 1/2 journée |
| Remédiation | Liste | Plan priorisé chiffré | Liste | Plan priorisé chiffré | Liste | Roadmap 12 mois |

```yaml
wf_audit_profils:
  startup_mvp:
    cadrage:
      perimetre: verbal_email
      grille: standard_agence
      planning: indicatif
    collecte:
      donnees: automatisé_outils_gratuits
      preuves: screenshots_basiques
      profondeur: surface
    analyse:
      benchmark: non
      score: global_unique
      details: top_10_issues
    restitution:
      rapport: 5_pages_synthèse
      presentation: non
      remediation: liste_simple

  enterprise:
    cadrage:
      perimetre: documenté_signé
      grille: personnalisée_pondérée
      planning: engagé_jalons
    collecte:
      donnees: auto_plus_manuel
      preuves: screenshots_annotés_videos
      profondeur: approfondie
    analyse:
      benchmark: 3_5_concurrents
      score: par_categorie_pondéré
      details: exhaustif
    restitution:
      rapport: 20_plus_pages
      presentation: 1h_qa
      remediation: plan_priorisé_chiffré

  premium:
    cadrage:
      perimetre: contrat_détaillé
      grille: sur_mesure_validée
      planning: engagé_jalons_revues
    collecte:
      donnees: exhaustif_multi_sources
      preuves: videos_logs_captures
      profondeur: expert_code_review
    analyse:
      benchmark: secteur_complet
      score: multi_dimensionnel
      details: root_cause_analysis
    restitution:
      rapport: 50_plus_pages
      presentation: atelier_demi_journée
      remediation: roadmap_12_mois
```

---

### wf-support : Ticket Support

#### Matrice Livrables × Profils (SLA)

| Livrable | Basic | Standard | Premium | Critical |
|----------|-------|----------|---------|----------|
| **RÉCEPTION** |
| Accusé réception | 24h | 4h | 1h | 15min |
| Canal | Email | Email + ticket | Multi-canal | Hotline dédiée |
| Catégorisation | Manuelle | Semi-auto | Automatique | Auto + humain |
| **DIAGNOSTIC** |
| Temps diagnostic | 48h | 24h | 4h | 1h |
| Communication | Fin diagnostic | Étapes clés | Temps réel | Temps réel + escalade |
| Escalade | Sur demande | Automatique L2 | Automatique L3 | Direct expert |
| **RÉSOLUTION** |
| SLA résolution P1 | 1 semaine | 48h | 24h | 4h |
| SLA résolution P2 | 2 semaines | 1 semaine | 48h | 24h |
| SLA résolution P3 | Best effort | 2 semaines | 1 semaine | 48h |
| **CLÔTURE** |
| Enquête satisfaction | Non | Email | Téléphone | Appel manager |
| Postmortem | Non | P1 uniquement | P1-P2 | Tous incidents |
| KB update | Non | Récurrents | Systématique | Systématique + formation |

```yaml
wf_support_sla:
  basic:
    reception:
      accuse_reception: 24h
      canal: email
      categorisation: manuelle
    diagnostic:
      temps_max: 48h
      communication: fin_diagnostic
      escalade: sur_demande
    resolution:
      sla_p1: 1_semaine
      sla_p2: 2_semaines
      sla_p3: best_effort
    cloture:
      satisfaction: non
      postmortem: non
      kb_update: non

  standard:
    reception:
      accuse_reception: 4h
      canal: email_ticket
      categorisation: semi_auto
    diagnostic:
      temps_max: 24h
      communication: etapes_cles
      escalade: automatique_l2
    resolution:
      sla_p1: 48h
      sla_p2: 1_semaine
      sla_p3: 2_semaines
    cloture:
      satisfaction: email
      postmortem: p1_uniquement
      kb_update: recurrents

  premium:
    reception:
      accuse_reception: 1h
      canal: multi_canal
      categorisation: automatique
    diagnostic:
      temps_max: 4h
      communication: temps_reel
      escalade: automatique_l3
    resolution:
      sla_p1: 24h
      sla_p2: 48h
      sla_p3: 1_semaine
    cloture:
      satisfaction: telephone
      postmortem: p1_p2
      kb_update: systematique

  critical:
    reception:
      accuse_reception: 15min
      canal: hotline_dediée
      categorisation: auto_plus_humain
    diagnostic:
      temps_max: 1h
      communication: temps_reel_escalade
      escalade: direct_expert
    resolution:
      sla_p1: 4h
      sla_p2: 24h
      sla_p3: 48h
    cloture:
      satisfaction: appel_manager
      postmortem: tous_incidents
      kb_update: systematique_formation
```

---

## Grille de Décision Rapide

### Sélection du Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    TYPE DE PROJET ?                          │
├──────────────┬──────────────┬───────────────┬───────────────┤
│  Nouveau     │  Existant    │  Ponctuel     │  Récurrent    │
│  from scratch│  à modifier  │  one-shot     │  continu      │
├──────────────┼──────────────┼───────────────┼───────────────┤
│              │              │               │               │
│  ┌────────┐  │  ┌────────┐  │  ┌─────────┐  │  ┌─────────┐  │
│  │CREATION│  │  │REFONTE │  │  │  AUDIT  │  │  │ SUPPORT │  │
│  └────────┘  │  │   ou   │  │  └─────────┘  │  └─────────┘  │
│              │  │EVOLUTION│  │               │               │
│              │  └────────┘  │               │               │
└──────────────┴──────────────┴───────────────┴───────────────┘
```

### Sélection du Profil

```
BUDGET serré ?
├── OUI ──┬── DÉLAI serré ? ──► Startup MVP
│         └── QUALITÉ importante ? ──► Économique
│
└── NON ──┬── DÉLAI serré ?
          │   ├── OUI + QUALITÉ importante ──► Urgence Marché
          │   └── OUI + QUALITÉ flexible ──► Artisan
          │
          └── QUALITÉ max priorité ?
              ├── OUI + DÉLAI important ──► Premium
              └── OUI + DÉLAI flexible ──► Enterprise
```

### Mapping Rapide Profil → Niveau Global

| Profil | Niveau global conseillé |
|--------|------------------------|
| Startup MVP | **Minimal** partout |
| Économique | **Minimal** partout |
| Urgence Marché | **Standard** Production, Minimal ailleurs |
| Artisan | **Standard** partout |
| Enterprise | **Standard** à **Premium** |
| Premium | **Premium** partout |

---

## Processus de Positionnement

### 1. Questionnaire Initial

```markdown
## Questions de Cadrage

1. **Budget**
   - Avez-vous un budget défini ? [ ] Oui [ ] Non
   - Ce budget est-il : [ ] Ferme [ ] Indicatif [ ] Flexible +20%
   - Fourchette : ____________

2. **Délai**
   - Avez-vous une date de livraison cible ? [ ] Oui [ ] Non
   - Cette date est liée à : [ ] Événement [ ] Contrat [ ] Stratégie [ ] Aucune contrainte
   - Date souhaitée : ____________

3. **Qualité**
   - Secteur d'activité : ____________
   - Contraintes réglementaires : [ ] RGPD [ ] WCAG [ ] PCI-DSS [ ] Autre: ____
   - Niveau de criticité : [ ] Vitrine [ ] Business [ ] Mission critique

4. **Arbitrage**
   Si vous deviez choisir, vous préféreriez :
   [ ] Livrer vite quitte à améliorer après
   [ ] Livrer parfait quitte à prendre plus de temps
   [ ] Respecter le budget quitte à réduire le scope
```

### 2. Atelier de Positionnement

1. Présenter le triangle projet
2. Faire répartir 100 points (min 10, max 60 par critère)
3. Identifier les contraintes absolues
4. Valider les flexibilités acceptées
5. Déduire le profil et les niveaux de livrables

### 3. Validation Formelle

```yaml
validation_positionnement:
  client: "[Nom]"
  date: "[Date]"
  profil_retenu: "[Profil]"

  engagement_agence:
    - "Respecter les niveaux de livrables définis"
    - "Alerter si dérive détectée"
    - "Proposer arbitrages si nécessaire"

  engagement_client:
    - "Valider le positionnement choisi"
    - "Accepter les conséquences sur la variable d'ajustement"
    - "Décider rapidement en cas d'arbitrage"

  signatures:
    client: ________________
    agence: ________________
```

---

## Révision du Positionnement

Le positionnement peut être révisé :
- À chaque phase majeure du projet
- En cas de changement de contexte client
- Si les contraintes initiales évoluent

**Processus de révision** :
1. Identifier le changement de contexte
2. Réévaluer la répartition des 100 points
3. Recalculer les niveaux de livrables
4. Valider avec le client
5. Mettre à jour le contrat si nécessaire
