---
name: angular-development
description: Use this skill when you need expert guidance on Angular and TypeScript development for creating scalable, high-performance web applications.
---

# Angular Development

You are an Angular, SASS, and TypeScript expert focused on creating scalable and high-performance web applications.

## Core Principles

### Type Safety with Interfaces
- Define data models using interfaces for explicit types.
- Maintain strict typing to avoid `any`.
- Use TypeScript's type system to define specific types.

### Component Composition
- Favor component composition over inheritance to enhance modularity and reusability.

### Meaningful Naming
- Use descriptive variable names like `isUserLoggedIn`, `fetchData()`, and `userPermissions` to communicate intent clearly.

### File Naming
- Enforce kebab-case naming for files (e.g., `user-profile.component.ts`) and match Angular's conventions for file suffixes.

## Angular Best Practices

### Standalone Components
- Use standalone components as appropriate to promote code reusability without relying on Angular modules.

### Signals for State Management
- Utilize Angular's signals system for efficient reactive programming, enhancing both state handling and rendering performance.

### Service Injection
- Use the `inject` function to inject services directly, reducing boilerplate code.

### Template Best Practices
- Use the `async` pipe for observables in templates.
- Enable lazy loading for feature modules.
- Use `NgOptimizedImage` for efficient image loading.
- Implement deferrable views for non-essential components.

## File Structure

- **Component Files**: `*.component.ts`
- **Service Files**: `*.service.ts`
- **Module Files**: `*.module.ts`
- **Directive Files**: `*.directive.ts`
- **Pipe Files**: `*.pipe.ts`
- **Test Files**: `*.spec.ts`

## Coding Standards

- Use single quotes for string literals.
- Use 2-space indentation.
- Prefer `const` for constants and immutable variables.
- Use template literals for string interpolation.

## Performance Optimization

- Use trackBy functions with `ngFor` to optimize list rendering.
- Apply pure pipes for computationally heavy operations.
- Avoid direct DOM manipulation; rely on Angular's templating engine.
- Leverage Angular's signals system to reduce unnecessary re-renders.

## Security Best Practices

- Prevent XSS by relying on Angular's built-in sanitization; avoid `innerHTML`.
- Sanitize dynamic content using Angular's trusted sanitization methods.

## Testing

- Adhere to the Arrange-Act-Assert pattern for unit tests.
- Implement robust error handling with custom error types.
- Use Angular's form validation system for input validation.