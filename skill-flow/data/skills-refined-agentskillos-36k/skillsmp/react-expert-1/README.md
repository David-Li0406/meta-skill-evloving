# React Expert Skill

Skill spécialisé dans l'écosystème React moderne avec **28 agents** couvrant les hooks, composants, state management, data fetching, testing, styling et performance.

## Position dans l'Architecture

```
NIVEAU 1 : POURQUOI → direction-technique
NIVEAU 2 : QUOI     → web-dev-process
NIVEAU 3 : COMMENT  → react-expert ← CE SKILL
```

Ce skill fournit l'**implémentation concrète** pour React. Il ne fournit pas les décisions stratégiques (`direction-technique`) ni les processus d'équipe (`web-dev-process`).

## Structure

```
react-expert/
├── SKILL.md                    # Orchestrateur principal
├── README.md                   # Ce fichier
├── agents/
│   ├── hooks/                  # 5 agents
│   │   ├── orchestrator.md
│   │   ├── state-hooks.md      # useState, useReducer
│   │   ├── effect-hooks.md     # useEffect, useLayoutEffect
│   │   ├── ref-hooks.md        # useRef, forwardRef
│   │   └── custom-hooks.md     # Création de hooks
│   │
│   ├── components/             # 5 agents
│   │   ├── orchestrator.md
│   │   ├── functional.md       # Composants fonctionnels
│   │   ├── composition.md      # Compound, HOC, Render Props
│   │   ├── forms.md            # Formulaires React
│   │   └── error-boundaries.md # Gestion d'erreurs
│   │
│   ├── state/                  # 4 agents
│   │   ├── orchestrator.md
│   │   ├── context.md          # Context API
│   │   ├── zustand.md          # Zustand
│   │   └── redux-toolkit.md    # Redux Toolkit
│   │
│   ├── data/                   # 4 agents
│   │   ├── orchestrator.md
│   │   ├── react-query.md      # TanStack Query
│   │   ├── swr.md              # SWR
│   │   └── suspense.md         # React Suspense
│   │
│   ├── testing/                # 4 agents
│   │   ├── orchestrator.md
│   │   ├── rtl.md              # React Testing Library
│   │   ├── hooks-testing.md    # Tests de hooks
│   │   └── mocking.md          # Mocks et MSW
│   │
│   ├── styling/                # 3 agents
│   │   ├── orchestrator.md
│   │   ├── tailwind-react.md   # Tailwind + React
│   │   └── css-in-js.md        # styled-components, Emotion
│   │
│   └── performance/            # 3 agents
│       ├── orchestrator.md
│       ├── memoization.md      # memo, useMemo, useCallback
│       └── code-splitting.md   # lazy, Suspense
│
└── tests/                      # 4 fichiers de tests
    ├── config.js
    ├── utils.js
    ├── validate-skill.test.js
    ├── validate-agents.test.js
    ├── validate-domains.test.js
    └── validate-routing.test.js
```

## Utilisation

### Exemples de requêtes

```
# Hooks
"Comment créer un custom hook pour le localStorage ?"
→ hooks/custom-hooks.md

"Quelle est la différence entre useEffect et useLayoutEffect ?"
→ hooks/effect-hooks.md

# State Management
"Dois-je utiliser Context ou Zustand ?"
→ state/orchestrator.md (comparaison)

"Comment configurer Zustand avec persist ?"
→ state/zustand.md

# Data Fetching
"Comment utiliser React Query avec TypeScript ?"
→ data/react-query.md

# Testing
"Comment tester un composant avec React Testing Library ?"
→ testing/rtl.md

"Comment mocker une API avec MSW ?"
→ testing/mocking.md

# Performance
"Quand utiliser useMemo vs useCallback ?"
→ performance/memoization.md
```

## Tests

```bash
cd .web-agency/skills/react-expert/tests

# Exécuter tous les tests
node validate-skill.test.js
node validate-agents.test.js
node validate-domains.test.js
node validate-routing.test.js

# Output JSON pour CI
OUTPUT_FORMAT=json node validate-skill.test.js
```

## Relation avec frontend-developer

```
frontend-developer                          react-expert
      │                                           │
      ├── frameworks/                             │
      │      └── react-expert.md ──DÉLÈGUE──►     │ (28 agents)
      │         (agent léger)                     │
      │                                           │
      └── (33 agents)                             └── Skill autonome
```

Le skill `frontend-developer` contient un **agent de délégation** (`frameworks/react-expert.md`) qui redirige automatiquement vers ce skill pour toute question approfondie sur React.

| Type de question | Où ça va |
|------------------|----------|
| Questions rapides React | `frontend-developer/frameworks/react-expert.md` (résumé) |
| Questions approfondies React | `react-expert` (ce skill - 28 agents) |
| Questions JS/TS/CSS | `frontend-developer` (reste dans le skill) |

## Next.js

Ce skill ne couvre **pas** Next.js. Un skill séparé `nextjs-expert` est prévu pour couvrir :
- App Router
- Server Components
- Server Actions
- API Routes
- Middleware

## Version

**1.0.0** - 28 agents sur 7 domaines

## Changelog

Voir SKILL.md section "Changelog"
