---
name: react-three-fiber-best-practices
description: Use this skill when developing applications with React Three Fiber, Three.js, and modern React practices to ensure optimal performance and maintainability.
---

# Skill body

## Core Principles

- Write concise, technical responses with accurate React examples.
- Employ functional, declarative programming paradigms; avoid class-based approaches.
- Prioritize iteration and modularity over code duplication.
- Use descriptive variable names incorporating auxiliary verbs (e.g., `isLoading`, `hasError`).
- Directory naming: lowercase with dashes (e.g., `components/auth-wizard`).
- Favor named exports for all components.

## JavaScript/TypeScript Standards

- Use `function` keyword for pure functions; omit semicolons.
- TypeScript mandatory for all code; prefer interfaces over type aliases.
- Avoid enums; use maps instead.
- File organization: exported component -> subcomponents -> helpers -> static content -> types.
- Omit unnecessary braces in single-line conditionals.

## Error Handling

- Address errors and edge cases at function entry points.
- Employ early returns for error conditions to avoid deeply nested if statements.
- Position happy path logic last for enhanced readability.
- Use guard clauses for preconditions and invalid states.

## React-Specific Practices

- Use functional components exclusively.
- Use `function` syntax, not `const`, for component declarations.
- Leverage Next UI and Tailwind CSS for styling.
- Implement responsive design throughout.
- Wrap client components in Suspense with fallbacks.
- Use dynamic loading for non-critical components.
- Return expected errors as values; avoid try/catch for anticipated errors.
- Implement error boundaries using `error.tsx` and `global-error.tsx`.

## Three.js and React Three Fiber Best Practices

- Use declarative 3D scene composition with React components.
- Leverage hooks like `useFrame`, `useThree`, and `useLoader` for animations and scene access.
- Implement proper cleanup in `useEffect` for 3D resources.
- Use drei library helpers for common 3D patterns.
- Optimize performance with instancing for repeated geometries.
- Handle window resize and device pixel ratio appropriately.
- Properly dispose of geometries, materials, and textures when no longer needed.
- Use object pooling for frequently created/destroyed objects.
- Implement level of detail (LOD) for complex scenes.
- Minimize draw calls through geometry merging and instancing.
- Use appropriate texture sizes and formats.
- Implement frustum culling for large scenes.
- Profile and optimize render loops.