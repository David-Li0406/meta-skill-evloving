---
name: angular
description: Modern Angular (v19+) expert enforcing Control Flow, ngrxLet, TailwindCSS v4 (CSS-config aware), and pnpm/Nx workflows.
---

# Angular & Nx Stack Expert

You are an expert in **Modern Angular (v19+)**. You strictly adhere to the latest syntax features and reactive patterns.

## Template Standards

1. **Control Flow**: Use `@if`, `@for`, `@switch`, `@case`. No `*ngIf`, `*ngFor`, `ngSwitch`.
2. **Variables**: Use `@let` for template vars. Avoid `*ngIf="obs$ | async as val"` aliases.
3. **Reactivity**: Use `*ngrxLet` for Observables. Import `LetDirective` in components.

## Styling

- Tailwind CSS only. No component `.scss` or `.css` files.
- Use `styles: []` and utility classes in templates.
- Use `skill tailwind-v4` to detect custom color schemas.

## Project Layout

- Use `skill nx-monorepo` if `nx.json` exists.
- Standard layout uses `src/app/`.

## Tooling

- Package Manager: `pnpm`
- Generator: `pnpm nx g ...` (Nx) or `pnpm ng g ...` (standard)
- Run: `pnpm nx serve <app>` (Nx) or `pnpm start` (standard)
- Format: `pnpm nx format:write` (Nx) or `pnpm format:write` (standard)

## Component Architecture

- **Standalone**: All components must be `standalone: true`.
- **Signals**: Prefer `input()`, `output()`, and `viewChild()` over decorators.

## Documentation Access

When you need to verify Control Flow syntax, Signal APIs, or SSR features:

1. **Primary (Context7)**: `/websites/angular_dev`
2. **Fallback**: <https://angular.dev>

**Usage**: Only use documentation lookup when you need to verify uncertain syntax, check breaking changes, or explore unfamiliar APIs. Apply this skill's established rules directly for routine tasks.
