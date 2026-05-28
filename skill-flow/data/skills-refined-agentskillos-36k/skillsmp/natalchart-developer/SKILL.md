---
name: natalchart-developer
description: Official developer skill for the Natalchart project. Encapsulates architecture, FSD rules, tech stack, and design system patterns.
---

# Natalchart Developer Skill

This skill provides the comprehensive context and rules for developing the **Natalchart** project. It is derived from the approved `project-context.md`, `architecture.md`, and `ux-design-specification.md`.

**ALL AI AGENTS MUST FOLLOW THESE COMPLIANCE RULES.**

## 1. Project Overview

**Natalchart** is a mobile-first web service that provides personal natal chart interpretations in a "One Card, One Topic" format. It emphasizes accuracy ("knows me better than GPT"), easy access (free preview), and high-quality user experience.

- **Core Value**: "One card at a time, discover yourself."
- **Key Features**: Step-by-step Onboarding, Natal Chart Calculation, LLM Interpretation, Paid Unlock System.

## 2. Technology Stack (Strict)

- **Runtime**: Node 20.9+, TypeScript
- **Framework**: Next.js App Router (Turbopack, `src/`, `@/*` alias)
- **UI Framework**: **Base UI (MUI Base)** + **Tailwind CSS**
- **Database**: Prisma (6.x/7.x) + PostgreSQL (SQLite allowed for MVP only)
- **Auth**: NextAuth.js v4 (`next-auth@4.x`)
- **Infrastructure**: Vercel (Hosting, Env, Blob/KV if needed)
- **External**:
    - `circular-natal-horoscope-js` (Chart Calculation)
    - `@eaprelsky/nocturna-wheel` (Wheel Visualization - Client only)
    - LLM API (Interpretation)
    - PG Integration (Payment)

## 3. Architecture: Feature-Sliced Design (FSD)

The project strictly follows **Feature-Sliced Design**.
**Layer Order (Top → Bottom):** `app` → `pages` → `widgets` → `features` → `entities` → `shared`

### Dependency Rules (CRITCAL)

1.  **Top-down only**: Upper layers can import lower layers. Lower layers **CANNOT** import upper layers.
2.  **No Cross-Slice Imports**: Slices in the same layer cannot import each other (e.g., `features/auth` cannot import `features/payment`). Communication must go through `pages` or `app`.
3.  **Shared Layer**: Can be imported by anyone. Cannot import any other layer.

### Directory Structure

```
src/
├── app/          # Routing, Layouts, API Routes
├── pages/        # Page Composition (Landing, Onboarding, Cards)
├── widgets/      # Complex standalone UI blocks (CardViewer, Header)
├── features/     # User Actions (Auth, Payment, Onboarding Form)
├── entities/     # Business logic/models (User, Card, Topic, NatalChart)
└── shared/       # Reusable foundational code (UI, Lib, API, Config)
    ├── ui/       # Base UI Desgin System Components
    ├── lib/      # Prisma(db), Auth, LLM, Chart
    └── api/      # Fetch wrappers
```

## 4. Design System & UX Patterns

### Design Foundation

- **Stack**: **Base UI** (Behavior/Accessbility) + **Tailwind CSS** (Styling).
- **Styling**: Vanilla CSS is allowed but Tailwind is primary.
- **Responsiveness**: Mobile-first (`sm:640px`, `md:768px`...). Touch targets must be **min 44x44px**.
- **Visuals**: Bright, modern tone (not dark/mystical).

### Core UX Patterns

1.  **One Card, One View**: No long scrolling. Each screen focuses on one task or one reading card.
2.  **Step-by-Step Onboarding**:
    - Step 1: Birth Date
    - Step 2: Birth Time (Explicit "I don't know" option)
    - Step 3: Birth Place
3.  **Locked Content**:
    - Free: 4 Topics.
    - Paid: 10 Topics (Locked with Blur/Icon).
    - Pattern: "Unlocked by purchase" -> Show Content.

### Component Implementation

- **Shared UI**: `src/shared/ui` contains Base UI wrappers (Button, Input, Modal).
- **Custom Widgets**: `widgets/card-viewer`, `widgets/onboarding-steps` implement the specific UX patterns.

## 5. Implementation Rules (Do Not Miss)

### Naming Conventions

- **DB/Prisma**: `snake_case` tables (mapped), `camelCase` fields.
- **API**: `/api/cards` (Plural resources), camelCase JSON.
- **Files**: `Component.tsx` (Pascal), `util.ts` (camel), `page.tsx`/`route.ts` (Next.js fixed).
- **Folders**: `kebab-case`.

### Error Handling

- **API Response**: MUST use standard format:
    ```json
    { "error": "User message", "code": "ERR_CODE", "retry": true }
    ```
- **UI**: Display `error.message` and retry button if `retry: true`.
- **Handling**: `try/catch` in Route Handlers/Actions.

### State Management

- **URL-Driven**: Use URL query params for steps/card focus (`?step=2`, `?card=3`).
- **Server State**: React Server Components + Fetch. No global client store (Zustand/Redux) for MVP.

### Performance & Security

- **Loading**: ALWAYS show loading states (`loading.tsx` or Suspense) for Chart/LLM generation.
- **Secrets**: API Keys never exposed to client. Use Server Actions/Route Handlers.

### Code Structure & Maintainability

- **Component Size**: **Avoid "God Components"**. If a file exceeds ~200-250 lines, it MUST be refactored.
    - Extract sub-components (keep in same folder or `_components/` if private).
    - Extract logic into custom hooks.
- **Nesting Depth**:
    - **Logic**: Avoid trying/catch/if/loop nesting deeper than 3 levels. Use early returns (guard clauses).
    - **Tree**: Avoid excessive prop drilling. Use Composition or (if strictly necessary) Context.
- **Modularity**: Keep components focused on a single responsibility.

## 6. Development Workflow

1.  **Reference**: Check `_bmad-output/planning-artifacts/` for full specs.
2.  **Plan**: Create `implementation_plan.md` before coding.
3.  **Verify**: Run accessible checks and mobile view checks.

## 7. Artifact References

- **Context**: `_bmad-output/project-context.md`
- **Architecture**: `_bmad-output/planning-artifacts/architecture.md`
- **UX/Design**: `_bmad-output/planning-artifacts/ux-design-specification.md`
