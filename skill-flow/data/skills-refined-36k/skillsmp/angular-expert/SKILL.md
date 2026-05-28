---
name: angular-expert
description: Enterprise Angular v21+ architecture and testing expert. Use when writing, reviewing, or designing Angular components, services, stores, or tests. Covers Zoneless change detection, Signals, SignalStore, module boundaries, testing strategy, and architectural heuristics. Triggers on Angular file creation/modification (.component.ts, .service.ts, .store.ts, .spec.ts), architectural discussions, state management, and testing decisions.
---

# Angular Expert

Expert guidance for enterprise Angular v21+ development. Enforces architectural heuristics that prevent maintenance nightmares at scale.

## Core Architectural Imperatives

These rules apply to ALL Angular code. Violations create technical debt.

### 1. Standalone Components Only
All components, directives, and pipes MUST be standalone. `SharedModule` pattern is prohibited.
```typescript
@Component({
  standalone: true,
  imports: [CommonModule, RouterLink], // Explicit imports
})
```

### 2. Dependency Ladder (Strict)
Dependencies flow downward ONLY: `Feature → UI → Data-Access → Utility`
- **Feature**: Smart components, routing, orchestration
- **UI**: Dumb/presentational components (NO service injection)
- **Data-Access**: Stores, facades, HTTP services, entities
- **Utility**: Pure functions, validators, types

### 3. Component-Service Firewall
Smart components NEVER inject `HttpClient`, `Router`, or raw stores directly. Inject domain-specific Facades.
```typescript
// ❌ VIOLATION
constructor(private http: HttpClient) {}

// ✅ COMPLIANT
constructor(private userFacade: UserFacade) {}
```

### 4. Humble Components
Extract ALL complex logic to services/facades. Components should be thin glue with minimal branching.

### 5. Signals for State, RxJS for Events
- **Signals**: Hold data, derive values, render to view (synchronous)
- **RxJS**: Streams of actions, HTTP requests, complex timing coordination
- Use `toSignal()` to convert final Observable stage for templates

### 6. Push State Down
```
Global State  → User session, theme, language (Root store/service)
Feature State → Filters, pagination, form data (SignalStore in route)
Component State → UI toggles, ephemeral input (signal() on component)
```

### 7. Zoneless-Ready Code
Never mutate state expecting Angular to "magically" detect it. Always use Signals or AsyncPipe. No relying on Zone.js patches for `setTimeout`/`setInterval`.

## Testing Philosophy: Sociable Tests

Reject the Mockist approach. Test behavior, not implementation.

### The No-Mock Policy
- ✅ Provide REAL services in TestBed
- ✅ Mock ONLY at system boundaries: Network (MSW), Time, Browser APIs
- ❌ Never use `jasmine.createSpyObj` or `vi.fn()` for services
- ❌ Never spy on internal methods

### Verification Pattern
```typescript
// ❌ MOCKIST (Banned)
expect(spy.getUsers).toHaveBeenCalled();

// ✅ SOCIABLE (Required)
expect(screen.getByText('John')).toBeVisible();
```

### Zoneless Testing
```typescript
it('should work', async () => {
  await component.doSomething();
  await fixture.whenStable(); // Wait for framework tasks
  fixture.detectChanges();    // Explicit view update
  expect(...).toBe(...);
});
```

Use `TestBed.tick()` after setting signals that drive effects.

## Reference Guides

Load these when working on specific concerns:

- **[Architecture & Boundaries](references/architecture.md)**: Module boundaries, Nx constraints, Hexagonal architecture, circular dependency prevention. Load when designing new features or restructuring.

- **[Testing Strategy](references/testing.md)**: Vitest configuration, MSW setup, Harness patterns, VRT. Load when writing tests or setting up test infrastructure.

- **[Signal Patterns](references/signal-patterns.md)**: SignalStore, Signal Forms, computed patterns, effect synchronization. Load when implementing state management or forms.

- **[Code Templates](references/code-templates.md)**: Ready-to-use templates for components, stores, tests, harnesses. Load when scaffolding new files.

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
