---
name: scaffold-[component]
description: [Action] [Context] with standard boilerplate. Use when [User Trigger].
license: Apache-2.0
metadata:
  author: [Author]
  version: "1.0"
---

# [Component] Scaffolding

This skill generates a standard [Component] structure.

## When to use this skill

Use this skill when you need to create a new [Component] from scratch. This ensures adherence to [Style/Library] conventions.

## File Structure

Create the following files:

- `path/to/[name].ts`: Main logic
- `path/to/[name].test.ts`: Unit tests
- `path/to/README.md`: Documentation

## Code Conventions

- Use [Library X] for [Feature].
- Follow [Style Guide] (e.g., functional components, async/await).
- Add JSDoc comments to all public functions.

## Templates

### Main File (`[name].ts`)

```typescript
// [Insert Code Template]
export const [Name] = () => {
  // ...
};
```

### Test File (`[name].test.ts`)

```typescript
// [Insert Test Template]
```

## Progressive Disclosure

If there are many template variations, store them in `assets/templates/` and reference them here.
