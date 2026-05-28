---
name: frontend-engineer
description: Apply when writing React/TypeScript frontend code. Enforces component architecture patterns, type safety, and reusability standards.
---

Code for maintainability. Every component should be reusable without modification at the call site.

## Principles

**Components own their styles**
If a style is needed, it belongs in the component definition — not passed as className overrides at usage. When you see `<Component className="text-sm text-[#6b6b6b]">`, the component is incomplete. Expose props for intentional variants, not escape hatches for ad-hoc styling.

**Margin-free components**
Top-level element of a component must not have margin. Spacing between components is the parent's responsibility. Inner padding is fine. This makes components composable without unexpected spacing side effects.

**No `any`**
TypeScript's `any` is forbidden. Use `unknown` and narrow, or define proper types. If you're tempted to cast to `any`, the types are wrong — fix them.