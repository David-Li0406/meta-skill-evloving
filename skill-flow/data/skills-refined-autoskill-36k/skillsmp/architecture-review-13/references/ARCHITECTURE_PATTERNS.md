# Architecture Patterns Detection Guide

This reference helps identify architectural patterns in JavaScript/TypeScript codebases. Use these patterns when analyzing project structure and providing architectural insights.

---

## Overall Architecture Patterns

### Clean Architecture / Hexagonal
**Indicators:**
- Clear separation between domain, application, and infrastructure layers
- Dependency inversion (outer layers depend on inner layers, not vice versa)
- Domain entities that are framework-agnostic
- Ports and adapters pattern for external integrations

**Directory structure signals:**
```
src/
  domain/          # Core business logic
  application/     # Use cases
  infrastructure/  # External concerns (DB, API clients)
  presentation/    # UI/Controllers
```

### MVC (Model-View-Controller)
**Indicators:**
- `models/`, `views/`, `controllers/` directories
- Clear separation between data, presentation, and control logic
- Often seen in Express.js backends

**Directory structure signals:**
```
src/
  models/
  views/
  controllers/
  routes/
```

### Feature-Based / Domain-Driven
**Indicators:**
- Code organized by feature rather than technical layer
- Each feature folder contains its own components, hooks, services
- Self-contained modules

**Directory structure signals:**
```
src/
  features/
    auth/
      components/
      hooks/
      services/
      types/
    dashboard/
      components/
      hooks/
      services/
```

### Layer-Based
**Indicators:**
- Code organized by technical layer (components, hooks, services)
- Horizontal slicing rather than vertical

**Directory structure signals:**
```
src/
  components/
  hooks/
  services/
  utils/
  types/
```

---

## Frontend Patterns (React/React Native)

### Container/Presenter (Smart/Dumb Components)
**Indicators:**
- Components split into containers (logic) and presenters (UI)
- Containers handle state and data fetching
- Presenters are pure functions of props

**Code signals:**
- Files named `*Container.tsx` and `*View.tsx` or `*Presenter.tsx`
- Components that only render props without hooks
- Components that only have hooks and delegate rendering

### Compound Components
**Indicators:**
- Parent component with multiple child components
- Children share implicit state through context
- Flexible composition API

**Code signals:**
```tsx
<Select>
  <Select.Trigger />
  <Select.Options>
    <Select.Option />
  </Select.Options>
</Select>
```

### Custom Hooks Pattern
**Indicators:**
- Business logic extracted into reusable hooks
- Components are thin wrappers around hooks
- Clear separation of concerns

**Code signals:**
- `hooks/` directory with `use*.ts` files
- Components importing multiple custom hooks
- Hooks that return both state and actions

### Render Props
**Indicators:**
- Components that accept functions as children or render props
- Older pattern, less common in modern React

**Code signals:**
```tsx
<DataFetcher render={(data) => <Display data={data} />} />
```

### Higher-Order Components (HOC)
**Indicators:**
- Functions that wrap components to add functionality
- Often prefixed with `with*`

**Code signals:**
```tsx
export const EnhancedComponent = withAuth(withTheme(BaseComponent));
```

---

## Backend Patterns

### Repository Pattern
**Indicators:**
- Data access abstracted behind repository interfaces
- Business logic doesn't directly access database
- Easy to swap data sources

**Code signals:**
- `repositories/` directory
- Classes/functions like `UserRepository`, `getUsers`, `createUser`
- Interfaces like `IUserRepository`

### Service Layer
**Indicators:**
- Business logic contained in service classes/modules
- Services orchestrate repositories and other services
- Controllers/routes call services

**Code signals:**
- `services/` directory
- Classes like `UserService`, `AuthService`
- Methods like `getUserById`, `createOrder`

### Middleware Chain
**Indicators:**
- Request processing through a chain of middleware
- Each middleware handles a specific concern
- Common in Express, Fastify, Hono

**Code signals:**
- `middleware/` directory
- Functions that take `(req, res, next)` or similar
- `app.use()` calls with custom functions

### CQRS (Command Query Responsibility Segregation)
**Indicators:**
- Separate models for read and write operations
- Different paths for queries vs commands
- Often with event sourcing

**Code signals:**
- `commands/` and `queries/` directories
- Handler classes for specific operations
- Event/message-based communication

---

## Anti-Patterns to Flag

### God Object / God Component
**Indicators:**
- Single file with 500+ lines
- Component handling multiple unrelated responsibilities
- Excessive props (15+)
- Many different hooks in one component

**Impact:** Hard to maintain, test, and understand

### Circular Dependencies
**Indicators:**
- Module A imports Module B which imports Module A
- Often causes initialization issues
- Sign of poor module boundaries

**Impact:** Build issues, runtime bugs, unclear architecture

### Prop Drilling Hell
**Indicators:**
- Same prop passed through 4+ component levels
- Props only used for passing down, not for the component itself
- Missing Context where appropriate

**Impact:** Painful refactoring, verbose code

### Util Soup / Helper Explosion
**Indicators:**
- Large `utils/` directory with unrelated functions
- Functions that should belong to specific domains
- `helpers.ts` file with 50+ exports

**Impact:** Poor discoverability, unclear ownership

### Barrel File Abuse
**Indicators:**
- Excessive `index.ts` files re-exporting everything
- Circular dependency issues from barrel files
- Import paths that hide actual file locations

**Impact:** Slower builds, hidden dependencies

### Mixed Concerns
**Indicators:**
- UI components with direct API calls
- Business logic in event handlers
- Database queries in route handlers

**Impact:** Hard to test, hard to maintain

### Inconsistent Patterns
**Indicators:**
- Same thing done multiple different ways
- Some features use hooks, others use classes
- Inconsistent naming conventions

**Impact:** Confusing for developers, hard to onboard

---

## Pattern Detection Heuristics

When analyzing a codebase, look for:

1. **Directory structure** - What organizational pattern is used?
2. **Import patterns** - How do modules depend on each other?
3. **File naming** - Are there conventions like `*.service.ts`, `*.hook.ts`?
4. **Component structure** - Are components focused or doing too much?
5. **State management** - Context, Redux, Zustand, or prop drilling?
6. **Data fetching** - Where does it happen? Dedicated layer?
7. **Error handling** - Centralized or scattered?
8. **Type definitions** - Co-located or in separate `types/` directory?

---

## Reporting Patterns

When documenting patterns in the architecture review:

1. **Name the pattern** - Use standard terminology
2. **Show evidence** - Point to specific files/directories
3. **Assess consistency** - Is it applied uniformly?
4. **Note deviations** - Where does the pattern break?
5. **Suggest improvements** - If anti-patterns exist, offer alternatives
