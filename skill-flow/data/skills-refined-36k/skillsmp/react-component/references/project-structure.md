# Project Structure

## Directory Layout

```
src/
├─ app/               # Routes, layouts, pages
├─ assets/            # Static files
├─ components/        # Reusable components
│  ├─ ui/             # Shared UI primitives
│  ├─ common/         # Shared non-UI components
├─ features/          # Feature modules (UI + logic)
│  ├─ revenue/        # Example feature module
│  │  ├─ components/  # Feature-specific components
│  │  │  ├─ RevenueCardContainer.tsx
│  │  │  ├─ RevenueCardView.tsx
│  │  │  └─ RevenueCardView.stories.tsx
│  │  ├─ hooks/       # Feature-specific hooks
│  │  │  └─ useRevenue.ts
│  │  ├─ types/       # Feature-specific types
│  │  │  └─ revenue.types.ts
│  │  └─ index.ts     # Public API barrel (explicit exports only)
├─ hooks/             # Cross-feature hooks
├─ lib/               # Framework utilities (api, logger)
├─ services/          # External services (analytics, auth, etc.)
├─ store/             # Shared state only when truly needed
├─ styles/            # Global styles + Tailwind config (globals.css)
├─ types/             # Global shared types
├─ utils/             # Generic utilities
```

## Folder Rules

- Group by **feature**, not type
- Keep code local to features until reuse demands sharing
- Shared UI → `components/ui`, shared logic → `components/common`

## Barrel Rules

- Barrels allowed only when explicit and intentional
- Never `export *`
- Barrels define a feature's public API, not convenience dumps

## Feature Module Structure

Each feature follows this pattern:

```
features/<feature-name>/
├─ components/           # Feature-specific components
│  ├─ <Name>Container.tsx
│  ├─ <Name>View.tsx
│  └─ <Name>View.stories.tsx
├─ hooks/                # Feature-specific hooks
│  └─ use<Feature>.ts
├─ api/                  # TanStack Query files
│  └─ use<Feature>Query.ts
├─ forms/                # Form schemas and hooks
│  ├─ <schema>.ts
│  └─ use-<form>-form.ts
├─ types/                # Feature-specific types
│  └─ <feature>.types.ts
└─ index.ts              # Public API barrel
```

Story (`.stories.tsx`) files are used to create isolated component examples. For best practices on organizing stories and making them interactive, see the [Advanced Storybook Guide](advanced-storybook.md).
