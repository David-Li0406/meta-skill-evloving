---
name: Coding Style
description: Enforced coding standards and best practices for the project, including rules on comments and libraries.
---

# Coding Style & Standards

## 1. Comments

- **NO COMMENTS in Code**: Do not generate comments explaining what the code does (e.g., `// This function adds two numbers`). Code must be self-documenting.

## 2. Icons

- **Library**: ALWAYS use `@hugeicons/core-free-icons` and `@hugeicons/react`.
- **Component**: Use the `HugeiconsIcon` wrapper component.
- **Pattern**:

  ```tsx
  import { SomeIcon } from "@hugeicons/core-free-icons";
  import { HugeiconsIcon } from "@hugeicons/react";

  <HugeiconsIcon icon={SomeIcon} className="size-4" />
  ```

- **No Custom SVGs**: Do not create custom SVG components if a suitable Hugeicon acts as a replacement.

## 3. UI Components

- **Tailwind CSS**: Use Tailwind utility classes for styling.
- **Base UI / Shadcn**: Prefer existing basic components from `@/components/ui`.

## 4. TypeScript / React

- **Types**: Explicitly define types/interfaces. Avoid `any`.
- **Functional Components**: Use React functional components.
- **Clean Code**: Keep components small and focused.
