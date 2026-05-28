---
name: shadcn
description: Create, update, and maintain shadcn/ui components in the `apps/web` Next.js project. Use when asked to add UI components, sync styles/theme, adjust Tailwind, or apply shadcn/ui best practices in this codebase.
---

# Shadcn (shadcn/ui)

## Goal

Apply shadcn/ui in `apps/web` using the real project configuration, creating or updating UI components in a consistent, accessible, and maintainable way.

## Workflow

1. Read `references/project.md` to learn current configuration, paths, versions, and registries.
2. Verify `apps/web/components.json` and `apps/web/package.json` before running the CLI.
3. If MCP is available, browse or search items in the `@shadcn` registry first.
4. Run the CLI from `apps/web` using the version installed in the project:

```
bun x shadcn add <component>
```

To update an existing component, allow explicit overwrite:

```
bun x shadcn add <component> --overwrite
```

5. Review changes in `apps/web/src/components/ui` and shared utilities under `apps/web/src/lib`.
6. Adjust global styles in `apps/web/src/index.css` if the component requires it.

## Best practices

- Use project aliases: `@/components/ui`, `@/components`, `@/lib/utils`, `@/lib`.
- Keep the `cn` function and `class-variance-authority` for variants and composable styles.
- Prefer composition over duplicating components.
- Keep `use client` only when the component uses hooks, state, or events.
- Use `next/image` and `next/link` instead of raw `<img>` or `<a>`.
- Respect accessibility: visible labels, correct roles/aria, and focus states.
- Avoid barrel imports in large libraries; import directly when it is critical.

## Verification

- If multiple files are modified, run `bun x ultracite check` before delivery.
- If there are style conflicts, run `bun x ultracite fix` in the workspace.
