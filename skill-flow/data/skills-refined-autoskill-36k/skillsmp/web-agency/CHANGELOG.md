# Changelog

Toutes les modifications notables du framework d'orchestration sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

## [4.2.0] - 2026-01-18

### Changé

#### Restructuration du Framework d'Orchestration

- **BREAKING**: Déplacement de `.web-agency/skills/web-agency/` vers `.web-agency/orchestration-framework/`
- **BREAKING**: Déplacement de `task-orchestrator` vers `orchestration-framework/task-orchestrator/`
- Déplacement de `skills/examples/` vers `.web-agency/examples/`
- Déplacement de `skills/scripts/` vers `.web-agency/scripts/`
- Renommage du workflow GitHub `web-agency-tests.yml` → `orchestration-framework-tests.yml`
- Clarification : ce n'est pas un skill mais un framework de coordination
- Mise à jour de `tests/config.js` pour refléter la nouvelle structure de chemins

### Migration

```diff
- .web-agency/skills/web-agency/
+ .web-agency/orchestration-framework/

- .web-agency/skills/task-orchestrator/
+ .web-agency/orchestration-framework/task-orchestrator/

- .web-agency/skills/examples/
+ .web-agency/examples/

- .web-agency/skills/scripts/
+ .web-agency/scripts/
```

## [1.0.0] - 2025-12-21

### Ajouté

#### Domaine 1 : Gestion de Projet & Relation Client

**5 sous-domaines avec 24 agents SRP :**

- **Avant-Projet** (7 agents)
  - `collecte-besoin` - Extraction d'informations depuis sources client
  - `formalisation-brief` - Structuration du brief standardisé
  - `questions-clarification` - Génération des questions de clarification
  - `analyse-perimetre` - Découpage en lots fonctionnels
  - `chiffrage` - Estimation des charges en jours/homme
  - `hypotheses-risques` - Documentation des hypothèses et risques
  - `redaction-proposition` - Rédaction de la proposition commerciale

- **Pilotage** (5 agents)
  - `creation-planning` - Création du planning projet
  - `analyse-dependances` - Analyse des dépendances entre tâches
  - `analyse-ecarts` - Détection des écarts planning vs réalité
  - `alertes-projet` - Génération des alertes projet
  - `reporting-hebdo` - Production du reporting hebdomadaire

- **Communication** (6 agents)
  - `email-relance` - Emails de relance client
  - `email-demande-validation` - Demandes de validation
  - `email-annonce-livraison` - Annonces de livraison
  - `email-demande-information` - Demandes d'information
  - `email-annonce-retard` - Annonces de retard
  - `compte-rendu` - Comptes-rendus de réunion

- **Livraison** (4 agents)
  - `plan-recette` - Plan de recette
  - `grille-recette` - Grille de tests
  - `suivi-anomalies` - Suivi des anomalies
  - `pv-recette` - Procès-verbal de recette

- **Facturation** (2 agents)
  - `preparation-facture` - Préparation des factures
  - `suivi-paiements` - Suivi des paiements

**Templates (8 fichiers) :**
- `brief-client.md` - Template de brief client
- `estimation.md` - Template d'estimation
- `proposition.md` - Template de proposition commerciale
- `planning.md` - Template de planning
- `reporting.md` - Template de reporting hebdomadaire
- `compte-rendu.md` - Template de compte-rendu
- `pv-recette.md` - Template de PV de recette
- `bilan-projet.md` - Template de bilan projet

**Tests (7 suites, 209 assertions) :**
- `validate-agents.test.js` - Validation structure agents
- `validate-routing.test.js` - Validation cohérence routage
- `validate-templates.test.js` - Validation existence templates
- `validate-workflows.test.js` - Tests d'intégration workflows
- `validate-orchestrator-routing.test.js` - Validation routage vs capacités
- `validate-template-generation.test.js` - Tests génération templates
- `validate-agent-examples.test.js` - Cas de test par type d'agent

**CI/CD :**
- GitHub Actions workflow pour exécution automatique des tests sur PR
- Rapport de test automatique en commentaire de PR

**Documentation :**
- `SKILL.md` - Description du skill principal
- `README.md` - Documentation d'utilisation
- `docs/web-agency-vision.md` - Vision et roadmap

### Architecture

- Principe SRP (Single Responsibility Principle) appliqué à tous les agents
- Orchestrateurs hiérarchiques (skill → domaine → sous-domaine)
- Configuration centralisée dans `tests/config.js`

## [À venir]

### Domaine 2 : Stratégie & Conseil
- Audit digital
- Benchmark concurrentiel
- Recommandations stratégiques

### Domaine 3 : Design & Création Graphique
- Briefs créatifs
- Revue de maquettes
- Charte graphique

### Domaine 4 : Contenu & Rédaction
- Stratégie éditoriale
- Rédaction web
- SEO éditorial

### Domaine 5 : Marketing Digital
- SEO technique
- SEA / Ads
- Social media
- Analytics
