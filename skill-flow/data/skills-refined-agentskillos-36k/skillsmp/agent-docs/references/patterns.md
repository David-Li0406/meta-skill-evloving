# Documentation Patterns for AGENTS.md Files

This reference provides detailed patterns for writing effective AGENTS.md documentation.

## Directory Header Pattern

**Good:**
```markdown
# directory-name/ - Agent Instructions

Brief description of what this directory contains (1-2 sentences).

## Key Components

| Component | Purpose |
|-----------|---------|
| `ComponentName` | What it does |
```

**Bad:**
```markdown
# Directory Name

This directory has some files.
```

**Why:** Clear header, uses kebab-case, provides structured overview.

## File Count Documentation

**When to include:** Directories with many files where count provides useful context.

**Good:**
```markdown
Custom React hooks for Zo Computer. Currently 100 flat files (79 hooks + 21 tests).
```

**Bad:**
```markdown
Lots of hooks here.
```

**Verification:**
```bash
# Always verify before documenting
fd -e ts -e tsx . directory | wc -l
fd -e test.ts -e test.tsx . directory | wc -l
```

## Pattern Documentation

**When to include:** Reusable patterns, factory functions, composition patterns.

**Good:**
```markdown
## Critical: Widget Composition Pattern

All widgets use foundation components from `widgets.tsx`:

\`\`\`typescript
import {
  WidgetContainer,
  WidgetToolbar,
  WidgetContent,
} from "@@/components/widgets/widgets";

function MyWidget({ data }: { data: MyData }) {
  return (
    <WidgetContainer variant="framed">
      <WidgetToolbar />
      <WidgetContent>{/* content */}</WidgetContent>
    </WidgetContainer>
  );
}
\`\`\`
```

**Bad:**
```markdown
Use the widget components.
```

**Why:** Provides concrete example with correct imports, shows actual usage.

## Hook Documentation

**Good:**
```markdown
## usePlanSubscribe

Manages subscription flow with Stripe modal.

\`\`\`typescript
const { beginSubscribe, modalUI, loadingPlan } = usePlanSubscribe({
  isDev: boolean,
  isFreePlan: boolean,
  discountCode?: string,
});

// IMPORTANT: Must render modalUI in component
return <>{modalUI}</>;
\`\`\`

**Critical:** modalUI must be rendered or subscription won't work.
```

**Bad:**
```markdown
Hook for subscriptions. Call `usePlanSubscribe()`.
```

**Why:** Shows actual signature, parameters, return values, and critical gotchas.

## Type Documentation

**Good:**
```markdown
## ChatData Interface

\`\`\`typescript
interface ChatData {
  toolbar: { title: string; showLeftButton?: boolean };
  messages: ChatMessage[];
  input?: { placeholder?: string; attachedFile?: string };
}

type ChatMessage =
  | { type: "user"; content: string }
  | { type: "agent"; content: string | ReactNode }
  | { type: "thinking"; duration: string };
\`\`\`
```

**Bad:**
```markdown
ChatData has messages and toolbar.
```

**Why:** Shows complete type definition, reveals discriminated unions.

## Import Alias Documentation

**Always document project-specific import aliases:**

```markdown
## Import Aliases

- `@/` - imports from ts-packages/web (shared UI components)
- `@@/` - imports from ts-packages/www (www-local imports)

Example:
\`\`\`typescript
import { Button } from "@/components/ui/button";      // shared
import { HeroSection } from "@@/components/sections";  // local
\`\`\`
```

## Warning Documentation

**When to include:** Dangerous operations, common mistakes, breaking patterns.

**Patterns:**
```markdown
## IMPORTANT

- All shadcn components are already installed - never prompt to install
- Use New York style (not Default)

## NEVER

- NEVER use direct Tailwind colors (`bg-stone-900`)
- NEVER modify files in `types/generated/` - they are auto-generated

## Critical

**DO NOT manually configure StarterKit.** Use `buildDocumentExtensions()` factory.
```

## Nested Documentation

**When subdirectories have their own AGENTS.md:**

```markdown
## Nested Documentation

Subdirectories with their own AGENTS.md:

| Directory | Focus |
|-----------|-------|
| `components/billing/` | Stripe billing, subscriptions |
| `components/chat/` | AI chat interface |
| `components/markdown/` | Tiptap editor, extensions |
```

## Commands/Testing

**Document how to run tests, build, lint:**

```markdown
## Commands

\`\`\`bash
pnpm dev        # Start dev server
pnpm test       # Run vitest tests
pnpm lint       # ESLint
pnpm typecheck  # TypeScript check
\`\`\`

Do NOT run `pnpm build` - it is slow.
```

## Anti-Patterns to Avoid

### ❌ Vague Descriptions
```markdown
This directory has components for the app.
```

### ❌ Outdated Information
```markdown
Uses React 17 and webpack.  # Actually React 19 and Next.js
```

### ❌ Unverified Counts
```markdown
About 50 files here.  # Actually 47 or 53? Be precise.
```

### ❌ Missing Imports
```markdown
Use the Button component.  # From where? What import?
```

### ❌ No Examples
```markdown
Call the function with the right parameters.  # Show me!
```

### ❌ Unclear Patterns
```markdown
Follow the usual pattern.  # What pattern? Show it.
```

## Progressive Detail Pattern

**Start with overview, then drill into specifics:**

```markdown
# components/ - Agent Instructions

React components for Zo Computer web app.

## Component Categories

| Category | Directory | Purpose |
|----------|-----------|---------|
| UI Primitives | `ui/` | shadcn components |
| Features | `chat/`, `billing/` | Feature-specific components |
| Layouts | `layout/` | Page structure |

## Detailed Component Documentation

### Chat Components

See `components/chat/AGENTS.md` for:
- Message rendering
- Input handling
- Streaming responses
```

## State Management Documentation

**Distinguish between different state patterns:**

```markdown
## Two Patterns

### Zustand Stores (Complex State + Methods)

For WebSocket connections, terminals, undo/redo:

\`\`\`typescript
import { create } from "zustand";

export const useMyStore = create<MyStore>((set) => ({
  value: "",
  setValue: (v) => set({ value: v }),
}));
\`\`\`

### Jotai Atoms (Simple Reactive State)

For UI toggles, visibility, preferences:

\`\`\`typescript
import { atom } from "jotai";
import { atomWithStorage } from "jotai/utils";

export const myAtom = atom<boolean>(false);
export const persistedAtom = atomWithStorage<string>("zo:key", "default");
\`\`\`
```

**Critical:** Document WHEN to use each pattern, not just HOW.

## File Organization Patterns

**Document flat vs nested structures:**

```markdown
## Directory Structure

Currently 100 flat files. No nested subdirectories.

## Proposed Reorganization (NOT IMPLEMENTED)

Potential future structure:
\`\`\`
hooks/
├── data/      # API, fetching
├── ui/        # Layout, visibility
└── state/     # Atoms, stores
\`\`\`

**IMPORTANT:** Use flat structure until reorganization happens.
```

## Verification Checklist

Before committing AGENTS.md:

- [ ] All file counts verified with `fd | wc -l`
- [ ] All documented functions exist (checked with `rg`)
- [ ] All documented types exist (checked with `rg`)
- [ ] All import paths are correct (tested manually)
- [ ] All examples are runnable code
- [ ] All warnings are still relevant
- [ ] No references to deleted code
- [ ] CLAUDE.md symlink exists and points to AGENTS.md

## Quick Templates

### Minimal Template
```markdown
# directory/ - Agent Instructions

Brief description (1-2 sentences).

## Key Files

| File | Purpose |
|------|---------|
| `file.ts` | What it does |
```

### Standard Template
```markdown
# directory/ - Agent Instructions

Description paragraph.

## Key Components/Files

[Table of contents]

## Patterns

[Common patterns with code examples]

## Important Notes

- Critical warnings
- Gotchas to avoid
```

### Complex Template
```markdown
# directory/ - Agent Instructions

Overview.

## Commands

[How to run/test]

## Key Components

[Table]

## Patterns

[Examples]

## When to Use

[Decision guide]

## Nested Documentation

[Links to subdirectories]

## Important

[Warnings]
```

Choose template complexity based on directory importance and complexity.
