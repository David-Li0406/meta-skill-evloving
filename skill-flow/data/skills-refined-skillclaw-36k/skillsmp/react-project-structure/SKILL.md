---
name: react-project-structure
description:
  File and folder organization conventions for React + Vite + shadcn/ui
  projects. Use when creating new components, organizing files, deciding folder
  structure, naming files/folders, or reviewing project organization. Covers
  folder-per-component vs flat structure, naming conventions, barrel exports,
  internal elements, and form patterns.
---

# React Project Structure Guidelines

## Core Conventions

| Convention    | Rule                                                           |
| ------------- | -------------------------------------------------------------- |
| Folder naming | `lowercase` = grouping folder, `PascalCase` = component folder |
| Exports       | Named exports only (except `ui/`)                              |
| Export style  | Inline `export const` for components; bottom exports for `index.js` and `ui/` |
| Functions     | Arrow functions (except `ui/`)                                 |
| Imports       | Use `index.js` barrel files                                    |
| File naming   | `ComponentName.jsx` (not just `index.jsx`)                     |
| Suffixes      | Keep descriptive suffixes (`LoginPrompt`, `ConfirmDialog`)     |

## Folder vs Flat Decision

| Condition               | Structure                                    | Example                                     |
| ----------------------- | -------------------------------------------- | ------------------------------------------- |
| Single `.jsx` file only | Flat in grouping folder OR standalone folder | `prompts/LoginPrompt.jsx` or `Header/`      |
| 2+ related files        | Folder-per-component                         | `DataTable/` with hooks, sub-components     |
| Tests                   | `__tests__/` in component or grouping folder | `Header/__tests__/` or `prompts/__tests__/` |
| Stories (single)        | PascalCase matching component name           | `Header/Header.stories.jsx`                 |
| Stories (group)         | lowercase matching folder name               | `prompts/prompts.stories.jsx`               |

## Internal Folder Naming

| Location            | Internal folder     | Purpose                                     |
| ------------------- | ------------------- | ------------------------------------------- |
| `src/components/*/` | `elements/`         | Small atomic primitives (Label, Error)      |
| `src/components/*/` | `assets/` or domain | Static resources (flags/, icons/)           |
| `src/pages/*/`      | `components/`       | Shared pieces used by 2+ sibling pages      |
| `src/pages/*/`      | `containers/`       | Shared layout utilities for sibling pages   |

**Important**: Only create `components/` or `containers/` folders in pages when
helpers are shared by multiple sibling pages. For single-page helpers, keep
files flat in the page folder.

## Directory Structure

```zsh
src/
├── components/          # Shared/reusable components
│   ├── Header/          # Standalone component (PascalCase at top level OK)
│   │   ├── index.js
│   │   ├── Header.jsx
│   │   ├── elements/
│   │   └── __tests__/   # Tests can live in component folder
│   ├── prompts/         # Grouping folder (flat structure)
│   │   ├── index.js
│   │   ├── LoginPrompt.jsx
│   │   ├── SignupPrompt.jsx
│   │   ├── elements/    # Internal primitives
│   │   └── __tests__/   # Or in grouping folder for multiple components
│   ├── dialogs/
│   │   ├── PricingSliderDialog/  # Complex → folder-per-component
│   │   │   ├── index.js
│   │   │   ├── PricingSliderDialog.jsx
│   │   │   ├── hooks/
│   │   │   └── elements/
│   │   └── ConfirmDialog.jsx    # Simple → flat
│   ├── pricing/         # Mixed: flat files + nested folders OK
│   │   ├── index.js
│   │   ├── CustomPricingCard.jsx
│   │   ├── StandardPricingCard.jsx
│   │   ├── PricingSlider/       # Complex component gets folder
│   │   └── elements/
│   ├── LanguageDropdown/
│   │   ├── index.js
│   │   ├── LanguageDropdown.jsx
│   │   ├── flags/       # Domain-specific assets folder
│   │   └── elements/
│   ├── form/            # Form utilities pattern
│   │   ├── index.js
│   │   ├── FormController.jsx
│   │   ├── FormField.jsx
│   │   ├── elements/    # Shared primitives
│   │   └── containers/  # Layout utilities (not layouts/)
│   └── ui/              # shadcn/ui primitives ONLY
├── layouts/
├── pages/
│   ├── admin/Users/
│   │   ├── index.js
│   │   ├── UsersPage.jsx
│   │   └── Toolbar/     # Single-page helper → flat in page folder
│   ├── errors/          # Multiple pages sharing helpers
│   │   ├── General/
│   │   ├── Network/
│   │   ├── NotFound/
│   │   ├── components/  # Shared by all error pages
│   │   └── containers/  # Shared layout utilities
│   └── public/Pricing/
│       ├── index.js
│       ├── PricingPage.jsx
│       ├── EnterpriseTab.jsx   # Single-page helpers → flat
│       └── StandardCards.jsx
└── hooks/               # Shared hooks
```

## File Patterns

### Export Style

| File type          | Style           | Example                                   |
| ------------------ | --------------- | ----------------------------------------- |
| Component `.jsx`   | Inline export   | `export const Button = () => { ... }`     |
| Barrel `index.js`  | Bottom re-export| `export { Button } from './Button'`       |
| `ui/` components   | Bottom default  | `export default function Button() { ... }`|

### index.js (barrel)

```js
export { ComponentName } from './ComponentName'
```

### ComponentName.jsx

```jsx
export const ComponentName = ({ ...props }) => {
  return (/* ... */)
}
```

### When to Extract vs Inline

| Condition                    | Action                 |
| ---------------------------- | ---------------------- |
| Few lines, single-file usage | Inline in same file    |
| Used by 2+ sibling files     | Extract to `elements/` |
| Complex logic                | Extract to `elements/` |

### Inline Helpers Example

```jsx
// ProfileDialog.jsx
const Row = ({ children }) => (
  <div className='flex items-center gap-2'>{children}</div>
)

export const ProfileDialog = ({ profile }) => {
  /* ... */
}
```

## Form Utilities Pattern

```zsh
form/
├── index.js              # Exports: FormController, FormField, FormRoot, FormFields
├── FormController.jsx    # Wrapper for controlled inputs (Select, Switch)
├── FormField.jsx         # Wrapper for native inputs (Input, Textarea)
├── elements/             # Shared primitives (Error, Label, FieldWrapper)
└── containers/           # Layout utilities (FormRoot, FormFields)
```

Use `containers/` (not `layouts/`) to avoid confusion with page layouts.

## src/components/ui/ Rules

- Reserved for shadcn/ui primitives only
- Install via `npx shadcn@latest add <component>`
- Uses regular functions + default exports (shadcn convention)
- Custom wrappers go in `src/components/`, not `ui/`

## Import Examples

```jsx
import { LoginPrompt, SignupPrompt } from '@/components/prompts'
import { PricingSliderDialog } from '@/components/dialogs'
import { Button, Card } from '@/components/ui'
import { FormController, FormRoot } from '@/components/form'
```
