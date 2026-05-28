# Changelog

Toutes les modifications notables de ce skill sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.4.0] - 2024-12-XX

### Modifié

- **Refactoring SRP complet** - Application du Single Responsibility Principle :

  **Agents refactorisés (contenu générique délégué à `web-dev-process`)** :
  - `accessibility-expert.md` → Focus sur accessibilité Gutenberg/WordPress uniquement
  - `seo-expert.md` → Focus sur wp_head, Yoast/RankMath, WP sitemaps uniquement
  - `design/design-tokens.md` → Focus sur theme.json v3 uniquement
  - `tooling/cicd-pipelines.md` → Focus sur WP test suite et matrice PHP×WP
  - `tooling/build-tooling.md` → Focus sur @wordpress/scripts et .asset.php
  - `tooling/local-dev.md` → Focus sur wp-env et WP-CLI
  - `tooling/quality-check.md` → Focus sur PHPCS WordPress et text domain i18n
  - `tooling/environment-config.md` → Focus sur wp-config.php et constantes WP
  - `testing/php-unit-tests.md` → Focus sur WP_UnitTestCase et Brain Monkey
  - `tooling/repository-setup.md` → Focus sur structures WP (theme/plugin/site)
  - `tooling/issue-management.md` → Focus sur templates WordPress-spécifiques

  **Agents déplacés vers `web-dev-process`** :
  - `design/visual-review.md` → `web-dev-process/agents/testing/visual-regression.md`

  **Agents conservés tels quels (déjà WordPress-spécifiques)** :
  - `testing/e2e-tests.md` - Utilise `@wordpress/e2e-test-utils-playwright`
  - `testing/js-unit-tests.md` - Utilise `@wordpress/scripts test-unit-js`

### Supprimé

- Contenu générique (WCAG, Playwright config, Git workflow, etc.) déplacé vers `web-dev-process`

## [1.3.0] - 2024-01-XX

### Ajouté

- **i18n Localization Expert** (`agents/i18n-localization.md`)
    - Fonctions de traduction PHP (__(), _e(),_x(), _n())
    - Génération POT/PO/MO avec WP-CLI
    - JavaScript i18n avec wp.i18n
    - Intégration WPML et Polylang

- **SEO Expert** (`agents/seo-expert.md`)
    - Meta tags et Open Graph
    - Schema.org JSON-LD
    - Sitemaps WordPress
    - Hooks Yoast SEO et Rank Math

- **Accessibility Expert** (`agents/accessibility-expert.md`)
    - Conformité WCAG 2.1
    - Attributs ARIA
    - Navigation clavier
    - Tests avec axe-core

- **GDPR & Consent API** (`agents/gdpr-consent-api.md`)
    - WP Consent API
    - Catégories de consentement
    - Intégration CMP

- **Issue Management** (`agents/tooling/issue-management.md`)
    - Templates GitHub Issue Forms
    - Templates GitLab
    - Labels normalisés WordPress

### Modifié

- **Refactoring SRP** - Division des agents multi-responsabilités :
    - `hooks-security.md` → `hooks-filters.md` + `security-validation.md`
    - `cicd-deployment.md` → `repository-setup.md` + `cicd-pipelines.md` + `deployment-ssh.md`
    - `fse-templates.md` → `block-theme.md` + `templates-patterns.md`

- Mise à jour des orchestrateurs avec les nouveaux agents
- Total agents : 31 → 35

## [1.2.0] - 2024-01-XX

### Ajouté

- **Tooling domain split** - Division de `project-bootstrap.md` :
    - `project-init.md` - Structure projet, Composer, package.json
    - `environment-config.md` - .env, wp-config.php, constantes
    - `local-dev.md` - wp-env, Docker, Local by Flywheel
    - `staging-setup.md` - Serveur staging, .htpasswd, utilisateurs

### Modifié

- Tooling orchestrator avec 8 agents
- Documentation des combinaisons d'agents

## [1.1.0] - 2024-01-XX

### Ajouté

- **Testing domain** (`agents/testing/`)
    - `php-unit-tests.md` - PHPUnit, WP_UnitTestCase
    - `js-unit-tests.md` - Jest, React Testing Library
    - `e2e-tests.md` - Playwright, tests d'intégration

- **Design domain** (`agents/design/`)
    - `design-tokens.md` - Extraction maquette → theme.json
    - `visual-review.md` - Diff visuel, régression Playwright

- **Theme domain** (`agents/theme/`)
    - `fse-templates.md` - Block themes, FSE, patterns
    - `style-engine.md` - Style Engine API, CSS generation
    - `interactivity-api.md` - @wordpress/interactivity

### Modifié

- Architecture hiérarchique avec sous-orchestrateurs
- Routing par mots-clés amélioré

## [1.0.0] - 2024-01-XX

### Ajouté

- **WP Core domain** (`agents/wp-core/`)
    - `custom-post-types.md`
    - `custom-taxonomies.md`
    - `custom-roles.md`
    - `custom-meta.md`
    - `hooks-security.md`

- **Gutenberg domain** (`agents/gutenberg-blocks/`)
    - `custom-blocks.md`
    - `block-variations.md`
    - `block-styles.md`
    - `data-stores.md`

- **Tooling domain** (`agents/tooling/`)
    - `wp-cli-commands.md`
    - `project-bootstrap.md`
    - `build-tooling.md`
    - `cicd-deployment.md`

- **Direct agents**
    - `wp-rest-api-expert.md`

- Orchestrateur principal (`SKILL.md`)
- Système de routing hiérarchique
- Documentation française

---

## Légende

- **Ajouté** : Nouvelles fonctionnalités
- **Modifié** : Changements dans les fonctionnalités existantes
- **Déprécié** : Fonctionnalités qui seront supprimées
- **Supprimé** : Fonctionnalités supprimées
- **Corrigé** : Corrections de bugs
- **Sécurité** : Corrections de vulnérabilités
