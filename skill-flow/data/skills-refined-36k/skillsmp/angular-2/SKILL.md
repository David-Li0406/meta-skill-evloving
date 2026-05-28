---
name: angular
description: Expert guidance on Angular 20+, Clean Architecture, Signals best practices, and Performance optimization.
---

# Angular Guidelines

## Core Philosophy

You are an Angular Architecture expert. When writing or reviewing Angular code, you strictly adhere to modern best
practices (Angular 20+)

**Motto:** "Stability, performance, and type safety above all."

## TypeScript Best Practices

- Use strict type checking
- Prefer type inference when the type is obvious
- Avoid the `any` type; use `unknown` when type is uncertain
- Use `readonly` for properties that should not change

## Angular Best Practices

- Use Angular MCP when needed (refer to Angular documentation and reference) `npx -y @angular/cli mcp`
- Always use standalone components over NgModules
- Must NOT set `standalone: true` inside Angular decorators. It's the default in Angular v20+.
- Use signals for state management
- Implement lazy loading for feature routes
- Do NOT use the `@HostBinding` and `@HostListener` decorators. Put host bindings inside the `host` object of the
  `@Component` or `@Directive` decorator instead
- Use `NgOptimizedImage` for all static images.
    - `NgOptimizedImage` does not work for inline base64 images.

## Accessibility Requirements

- It MUST pass all AXE checks.
- It MUST follow all WCAG AA minimums, including focus management, color contrast, and ARIA attributes.

### Components

- Keep components small and focused on a single responsibility
- Use `input()` and `output()` functions instead of decorators
- Use `computed()` for derived state
- Set `changeDetection: ChangeDetectionStrategy.OnPush` in `@Component` decorator
- Prefer inline templates
- Use always the (experimental) signal forms instead of any other forms (reactive or template driven)
- Do NOT use `ngClass`, use `class` bindings instead
- Do NOT use `ngStyle`, use `style` bindings instead
- When using external templates/styles, use paths relative to the component TS file.

## State Management

- Use signals for local component state
- Use `computed()` for derived state
- Keep state transformations pure and predictable
- Use the `resource` signal for async data.
- Use RxJS only for complex asynchronous event streams.

## Templates

- Keep templates simple and avoid complex logic
- Use native control flow (`@if`, `@for`, `@switch`) instead of `*ngIf`, `*ngFor`, `*ngSwitch`
- Use the async pipe to handle observables
- Do not assume globals like (`new Date()`) are available.
- Do not write arrow functions in templates (they are not supported).

## Services

- Design services around a single responsibility
- Use the `providedIn: 'root'` option for singleton services
- Use the `inject()` function instead of constructor injection

## Testing

- Use vitest for unit testing
    - Unit test services, pipes, and directives
    - Unit test presentational components
- Use Playwright for end-to-end testing
    - E2E test routed components (features) and user flows

## Error Handling

Every action that may fail MUST have proper error handling. If error not supposed to be handled at the current level, it
MUST be propagated to the caller.

Top level components (routed components/features) MUST display user-friendly error messages when an error occurs. Use
toast services or error components/page based on the context.

## Performance Optimization

TBD

## Routing

TBD

## Structure & Organization

First check local project guidelines, if any. If none, follow the existing directory structure. If none exists, follow
this structure:

```
- app
  - app (top level component, should only contain the router outlet)
  - config
- features (grouping by feature, a routed module)
  - feature-one
    - component-one (top level route)
    - component-two (top level route)
    - shared
- modules (grouping by domain, non routed module)
    - module-one 
        - ...
- shared
  - components
  - directives
  - pipes
  - services
  - utils
```

Module in this context means a logical grouping of related code that is not a routed feature and not `@NgModule`.

## Dependency Injection

---

# Appendix

## Components Types

#### Presentational Components

Presentational components (or "dumb" components) are components that interact only via inputs and outputs (both
signals). They do not manage state. The may inject view related services (like the `Location` service that helps with
history back navigation).

#### Image Like Components

A presentational component (semi "dumb") that takes a URL or path as input and fetches the structured data it displays
in its template.

A native example would be an image component that takes an image URL as input, fetches the image data, and displays.

An Angular example could be a `SourcedTableComponent` that takes a URL to CSV/JSON data as an input, fetches it, and
displays it in a table.

#### Composite Components

Composite components are presentational components that contain other presentational components. It may manage local UI
state.

#### Smart Components

Smart components manage state and inject services. They can contain other smart or presentational components.

#### Form Components

A smart component that manages a form. It handles validation, submission, and state management for the form. It may
split the form into multiple form components for better organization.

#### Routed Components

Routed components (features) are the top-level smart components associated with routes. And we treat each of them as an
independent application.