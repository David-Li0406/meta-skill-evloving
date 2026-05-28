---
name: angular-style-guide-and-architecture
description: Use this skill for establishing naming conventions, file structure, and architectural standards in Angular projects.
---

# Angular Style Guide and Architecture

## **Priority: P0 (CRITICAL)**

### Principles

- **Single Responsibility**: One component/service per file. Small functions (< 75 lines).
- **Size Limits**: Keep files under 400 lines. Refactor if larger.
- **Feature-Based Organization**: Organize by feature, not type (e.g., `features/dashboard/` containing components, services, and models).
- **Standalone First**: Use Standalone Components/Pipes/Directives. Eliminate `NgModule` unless interacting with legacy libs.
- **Core vs Shared**:
  - `core/`: Global singletons (e.g., AuthService, Interceptors).
  - `shared/`: Reusable UI components, pipes, utils (e.g., Buttons, Formatters).
- **Smart vs Dumb Components**:
  - **Smart (Container)**: Talks to services, manages state.
  - **Dumb (Presentational)**: Inputs/Outputs only. No logic.
- **LIFT**: **L**ocate, **I**dentify, **F**lat structure, **T**ry DRY.

### Naming Standards

- **Files**: `kebab-case.type.ts`
- **Classes**: `PascalCase` + `Type` suffix (e.g., `HeroListComponent`)
- **Directives**: `camelCase` selector (e.g., `appHighlight`)
- **Pipes**: `camelCase` name (e.g., `truncate`)
- **Services**: `PascalCase` + `Service` suffix (e.g., `HeroService`)

### Guidelines

- **Lazy Loading**: All feature routes MUST be lazy loaded using `loadComponent` or `loadChildren`.
- **Flat Modules**: Avoid deep nesting of modules.
- **Barrel Files**: Use carefully. Prefer direct imports for better tree-shaking in some build tools.

### Anti-Patterns

- **Logic in Templates**: Move complex logic to the component class or a computed signal.
- **Deep Nesting**: Avoid more than 3 levels of folder nesting.
- **Prefixing Interfaces**: No `IUser`. Use `User`.

### References

- [Naming Conventions](references/naming-convention.md)
- [Folder Structure](references/folder-structure.md)