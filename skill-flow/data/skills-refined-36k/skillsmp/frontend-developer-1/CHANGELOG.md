# Changelog

Toutes les modifications notables de ce skill sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.1.0] - 2024-12-25

### Modifié

#### Architecture POURQUOI / QUOI / COMMENT
- Clarification du positionnement en tant que skill **NIVEAU 3 : COMMENT** (implémentation)
- Documentation des liens de composition avec `direction-technique` (POURQUOI) et `web-dev-process` (QUOI)
- Ajout des flux de travail inter-skills avec exemples concrets
- Mise à jour des règles de routage pour différencier code/process/décision

#### Points d'escalade
- Ajout des escalades vers `direction-technique` pour les décisions stratégiques
- Ajout des escalades vers `web-dev-process` pour les processus d'équipe

### Philosophie mise à jour
Ce skill fournit désormais explicitement :
- ✅ Du code (React, Vue, TypeScript, CSS...)
- ✅ Des configurations (Vite, ESLint, Tailwind...)
- ✅ Des patterns d'implémentation

Et ne fournit PAS :
- ❌ Des décisions stratégiques → `direction-technique`
- ❌ Des processus de travail → `web-dev-process`

---

## [1.0.0] - 2024-12-25

### Ajouté

#### Orchestrateur principal
- SKILL.md avec architecture hiérarchique et règles de routage
- 8 domaines spécialisés avec 40 agents au total

#### Domaine Foundations (5 agents)
- `orchestrator.md` - Coordination des agents foundations
- `html-semantique.md` - Structure HTML5, SEO, métadonnées
- `css-moderne.md` - Grid, Flexbox, variables CSS, cascade
- `accessibilite.md` - WCAG, ARIA, tests a11y
- `responsive-design.md` - Mobile-first, breakpoints, media queries

#### Domaine JavaScript (5 agents)
- `orchestrator.md` - Coordination JavaScript/TypeScript
- `javascript-moderne.md` - ES6+, async/await, modules
- `typescript.md` - Typage, interfaces, generics
- `dom-manipulation.md` - DOM API, événements, delegation
- `api-integration.md` - Fetch, REST, GraphQL, WebSockets

#### Domaine Frameworks (5 agents)
- `orchestrator.md` - Coordination des frameworks
- `react-expert.md` - Composants, hooks, patterns React
- `vue-expert.md` - Composition API, Pinia, Vue patterns
- `nextjs-expert.md` - SSR, SSG, App Router, Server Components
- `component-patterns.md` - HOC, Render Props, Compound Components

#### Domaine Styling (4 agents)
- `orchestrator.md` - Coordination du styling
- `tailwind-expert.md` - Configuration, plugins, best practices
- `css-in-js.md` - styled-components, Emotion, CSS Modules
- `animations.md` - CSS transitions, keyframes, Framer Motion

#### Domaine State Management (3 agents)
- `orchestrator.md` - Coordination de la gestion d'état
- `react-state.md` - useState, Context, Redux, Zustand
- `server-state.md` - React Query, SWR, Apollo Client

#### Domaine Testing (4 agents)
- `orchestrator.md` - Coordination des tests
- `unit-testing.md` - Jest, Vitest, mocking, coverage
- `component-testing.md` - React Testing Library, Vue Test Utils
- `e2e-testing.md` - Playwright, Cypress

#### Domaine Performance (3 agents)
- `orchestrator.md` - Coordination de la performance
- `core-web-vitals.md` - LCP, FID, CLS, INP, Lighthouse
- `bundle-optimization.md` - Code splitting, tree shaking, lazy loading

#### Domaine Tooling (3 agents)
- `orchestrator.md` - Coordination de l'outillage
- `build-tools.md` - Vite, Webpack, esbuild
- `linting-formatting.md` - ESLint, Prettier, Stylelint

### Documentation
- README.md avec guide d'utilisation
- CHANGELOG.md

---

## Roadmap

### Prochaines versions
- Agent `nuxt-expert.md` pour Nuxt 3
- Agent `vue-state.md` pour Pinia/Vuex
- Agent `image-optimization.md`
- Agent `runtime-performance.md`
- Intégration avec skill `nextjs-expert` (à créer)
