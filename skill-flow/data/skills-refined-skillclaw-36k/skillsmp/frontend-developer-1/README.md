# Frontend Developer Skill

Skill d'**implémentation** (NIVEAU 3 : COMMENT) pour le développement front-end moderne.

## Position dans l'Architecture

```
NIVEAU 1 : POURQUOI → direction-technique (décisions stratégiques)
NIVEAU 2 : QUOI     → web-dev-process (processus, workflows)
NIVEAU 3 : COMMENT  → frontend-developer (ce skill - code, config)
```

Ce skill fournit le **code et les configurations** pour implémenter les décisions de `direction-technique` selon les processus de `web-dev-process`.

## Vue d'ensemble

Ce skill est organisé en **8 domaines** avec **33 agents** (+ délégations vers `react-expert` et `wordpress-gutenberg-expert`) :

| Domaine | Agents | Description |
|---------|--------|-------------|
| Foundations | 5 | HTML, CSS, accessibilité, responsive |
| JavaScript | 5 | ES6+, TypeScript, DOM, API |
| Frameworks | 6 | React (→ délégation), Vue, Next.js, WordPress (→ délégation), patterns |
| Styling | 4 | Tailwind, CSS-in-JS, animations |
| State Management | 3 | React state, server state |
| Testing | 4 | Unit, component, E2E |
| Performance | 3 | Core Web Vitals, bundle |
| Tooling | 3 | Build, linting, formatting |

## Utilisation

Invoquez ce skill quand vous avez des questions sur :

- **Fondamentaux** : HTML sémantique, CSS moderne, accessibilité WCAG
- **JavaScript** : ES6+, TypeScript, manipulation DOM, intégration API
- **Frameworks** : React hooks, Vue Composition API, Next.js, patterns
- **Styling** : Tailwind CSS, styled-components, animations CSS
- **État** : useState, Zustand, Redux, React Query, SWR
- **Tests** : Jest, Vitest, Testing Library, Playwright
- **Performance** : Core Web Vitals, code splitting, lazy loading
- **Outils** : Vite, ESLint, Prettier

## Structure

```
frontend-developer/
├── SKILL.md              # Orchestrateur principal
├── CHANGELOG.md          # Historique des versions
├── README.md             # Ce fichier
├── agents/
│   ├── foundations/      # HTML, CSS, a11y, responsive
│   ├── javascript/       # JS, TS, DOM, API
│   ├── frameworks/       # React, Vue, Next.js
│   ├── styling/          # Tailwind, CSS-in-JS, animations
│   ├── state-management/ # React state, server state
│   ├── testing/          # Unit, component, E2E
│   ├── performance/      # Web Vitals, bundle
│   └── tooling/          # Build, lint, format
├── docs/                 # Documentation additionnelle
└── templates/            # Templates réutilisables
```

## Ce que ce skill fournit

- ✅ **Code** : React, Vue, TypeScript, CSS, animations
- ✅ **Configurations** : Vite, Webpack, ESLint, Prettier, Tailwind
- ✅ **Patterns** : Hooks, composables, patterns de composants
- ✅ **Exemples** : Prêts à copier-coller

## Ce que ce skill ne fournit PAS

- ❌ **Décisions stratégiques** → `direction-technique`
- ❌ **Processus d'équipe** → `web-dev-process`
- ❌ **Conventions organisationnelles** → `direction-technique`

## Exemples de questions

```
"Comment structurer un formulaire accessible ?"
→ agents/foundations/accessibilite.md

"Quelle est la différence entre useMemo et useCallback ?"
→ agents/frameworks/react-expert.md

"Comment configurer Tailwind avec dark mode ?"
→ agents/styling/tailwind-expert.md

"Comment optimiser le LCP de ma page ?"
→ agents/performance/core-web-vitals.md

"Comment tester un composant React avec des hooks ?"
→ agents/testing/component-testing.md
```

## Version

**1.0.0** - Décembre 2024

Voir [CHANGELOG.md](./CHANGELOG.md) pour l'historique complet.
