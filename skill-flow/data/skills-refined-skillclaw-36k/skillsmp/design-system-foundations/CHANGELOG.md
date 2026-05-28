# Changelog

Toutes les modifications notables de ce skill sont documentées ici.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

## [1.1.0] - 2025-12-22

### Added

#### Test Suite
- `tests/run-tests.sh` - Test runner with Node.js version check (v14+)
- `tests/validate-skill.test.js` - SKILL.md structure validation
- `tests/validate-levels.test.js` - Atomic Design levels validation
- `tests/validate-agents.test.js` - Agent structure and frontmatter validation
- `tests/validate-tokens.test.js` - CSS token pattern validation
- `tests/validate-docs.test.js` - Documentation completeness validation
- `tests/config.js` - Centralized test configuration
- `tests/utils.js` - Shared test utilities

#### CI/CD
- `.github/workflows/design-system-foundations-tests.yml` - GitHub Actions workflow
- JSON_SUMMARY output for reliable CI parsing

#### Documentation
- `docs/accessibility-checklist.md` - WCAG AA checklist with contrast requirements
- `cn()` utility function documentation in getting-started.md
- CSS Nesting browser compatibility notes in naming-conventions.md
- Inputs.md variants documentation table

### Changed

#### Accessibility Improvements
- Renamed color tokens for WCAG AA clarity:
  - `--color-success` now uses green-600 (4.5:1 contrast ratio)
  - `--color-success-bg` for backgrounds (green-500, requires dark text)
- Added explicit contrast ratio comments to all color tokens
- Badge component uses spacing tokens instead of hardcoded values
- Dark mode aware notification badge border

#### Code Quality
- YAML frontmatter added to all 21 agent files
- Computed `TOTAL_AGENT_COUNT` constant in test config
- Production environment warning in tests/utils.js
- Improved orchestrator routing with both hyphenated and non-hyphenated agent name checks

### Fixed
- Templates orchestrator routing test (agent name format mismatch)
- Agent count in documentation (corrected to 21 total)

## [1.0.0] - 2025-12-21

### Added

#### Orchestrateur Principal
- SKILL.md avec architecture Atomic Design complète
- Routing intelligent par niveau (Foundations, Atoms, Molecules, Templates)
- Philosophie et principes fondamentaux documentés

#### Foundations (4 agents)
- `colors.md` - Système de couleurs avec palettes 50-900, tokens sémantiques, contraste WCAG, dark mode
- `typography.md` - Échelle modulaire 1.25, fluid typography, font loading optimisé
- `spacing.md` - Système 8pt, tokens sémantiques (inset, stack, inline), grid system
- `shadows.md` - Niveaux d'élévation, z-index scale, focus rings, dark mode shadows

#### Atoms (5 agents)
- `buttons.md` - 5 variants, 5 tailles, états, icon support, loading state
- `inputs.md` - Text, select, checkbox, radio, toggle, validation states
- `labels.md` - Form labels, tags (solid/soft/outline), chips interactifs
- `icons.md` - Système de tailles, styles (outline/solid), icon registry
- `badges.md` - Status, count, dot indicators, notification badges

#### Molecules (5 agents)
- `forms.md` - FormField, FormGroup, validation patterns, multi-step wizard
- `cards.md` - Base card, product card, user card, stats card
- `navigation.md` - Navbar, sidebar, tabs, breadcrumbs, pagination
- `modals.md` - Dialog, sheet/drawer, popover, alert dialog, focus trap
- `alerts.md` - Inline alert, banner, toast system, snackbar

#### Templates (3 agents)
- `hero-sections.md` - Hero variants, features grid, testimonials, stats, CTA
- `layouts.md` - Dashboard, marketing, auth, docs, settings layouts
- `pages.md` - List, detail, article, error (404/500), empty state, loading

#### Documentation
- `docs/getting-started.md` - Guide de démarrage rapide
- `docs/naming-conventions.md` - Conventions BEM, tokens, composants
- `references/resources.md` - Liens vers outils et design systems publics

### Technical
- Architecture hiérarchique avec orchestrateurs par niveau
- 21 agents au total (4 orchestrateurs + 17 agents spécialisés)
- CSS + React/TypeScript pour chaque composant
- Checklists d'accessibilité intégrées
- Exemples Storybook inclus
