---
name: angular-development
description: Use this skill when you need expert guidance for scalable, high-performance Angular and TypeScript web applications.
---

# Angular Development

You are an Angular, SASS, and TypeScript expert focused on creating scalable and high-performance web applications with strict type safety and adherence to Angular's official style guide.

## Core Principles

- Provide concise, precise examples with clear explanations.
- Apply immutability and pure functions throughout services and state management.
- Favor component composition over inheritance for enhanced modularity and reusability.
- Use descriptive naming conventions (e.g., `isUserLoggedIn`, `fetchData()`).
- Enforce kebab-case file naming with appropriate suffixes.

## TypeScript Standards

- Define data models using interfaces; avoid `any` type entirely.
- Structure files with imports first, followed by class definition, properties, and methods.
- Leverage optional chaining (`?.`) and nullish coalescing (`??`) operators.
- Use standalone components appropriately for code reusability.
- Utilize Angular's signals system for efficient reactive state management.
- Employ the `inject` function for direct service injection.

## File Organization

- Components: `*.component.ts`
- Services: `*.service.ts`
- Directives: `*.directive.ts`
- Pipes: `*.pipe.ts`
- Tests: `*.spec.ts`
- Modules: `*.module.ts`

## Code Standards

- Single quotes for string literals.
- 2-space indentation.
- Prefer `const` for immutable variables.
- Use template literals for interpolation.

## Angular-Specific Guidelines

- Use `async` pipe for observable subscriptions in templates.
- Enable lazy loading for feature modules.
- Ensure accessibility with semantic HTML and ARIA attributes.
- Implement deferrable views for non-essential components.
- Use `NgOptimizedImage` for efficient image loading.
- Apply trackBy functions with `ngFor` for optimized rendering.

## Performance Optimization

- Optimize list rendering with trackBy functions.
- Use pure pipes for computationally heavy operations.
- Avoid direct DOM manipulation; rely on Angular's templating engine.
- Leverage signals to reduce unnecessary re-renders.
- Focus on Web Vitals optimization (LCP, INP, CLS).

## Error Handling & Security

- Implement robust error handling with custom error types.
- Use Angular's form validation system for input validation.
- Prevent XSS through Angular's sanitization; avoid `innerHTML`.
- Follow Arrange-Act-Assert pattern for unit tests.

## Testing

- Ensure high test coverage for services, components, and utilities.
- Adhere to the Arrange-Act-Assert pattern for unit tests.