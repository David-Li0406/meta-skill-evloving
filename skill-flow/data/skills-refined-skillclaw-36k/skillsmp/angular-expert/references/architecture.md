# Angular Architecture & Boundaries

Deep guidance for enterprise Angular architecture. Load when designing features, restructuring code, or establishing module boundaries.

## Table of Contents
1. [Modular Monolith vs Micro Frontends](#modular-monolith-vs-micro-frontends)
2. [Library Types and Dependency Flow](#library-types-and-dependency-flow)
3. [Automated Boundary Enforcement](#automated-boundary-enforcement)
4. [Facade Pattern](#facade-pattern)
5. [Hexagonal Architecture](#hexagonal-architecture)
6. [Circular Dependency Prevention](#circular-dependency-prevention)

---

## Modular Monolith vs Micro Frontends

### The Unity Default Heuristic

**Rule**: Default to a Modular Monolith structured via Nx or Sheriff. Micro Frontends (Module Federation) is a "last resort" optimization, permissible only when organizational structure makes a single build pipeline sociologically impossible.

**Trade-off**: Single version policy for dependencies requires coordination during upgrades but guarantees consistency.

**Maintenance Nightmare Prevented**: The "Distributed Monolith" - a system with all coupling disadvantages of a monolith plus deployment complexity of microservices. Specifically avoids runtime integration failures where a remote MFE breaks the host due to shared library version mismatches (undetectable at compile time).

### Comparative Analysis

| Attribute | Modular Monolith (Default) | Micro Frontends |
|-----------|---------------------------|-----------------|
| Coupling Enforcement | Compile-time | Runtime (contracts) |
| State Sharing | Trivial (in-memory) | Complex (events, window) |
| Dependency Management | Single version (consistent) | Multi-version (risky) |
| Refactoring Velocity | High (IDE support) | Low (cross-repo) |
| Developer Experience | Unified debugging | Fragmented |

---

## Library Types and Dependency Flow

### The Four Library Types

Organize by **Domain** (verticals) and **Library Type** (horizontals):

1. **Feature Libraries**: Smart components, routing, orchestration logic. Entry points for user interaction.

2. **UI Libraries**: Dumb/Presentational components. Pure, reusable elements with NO knowledge of business logic or state.

3. **Data-Access Libraries**: The "Brain" - SignalStores, NgRx, HTTP services, Facades, domain entities. Interacts with APIs, manages application truth.

4. **Utility Libraries**: Pure functions, validators, helpers, shared types. Stateless and domain-agnostic.

### The Dependency Ladder Heuristic

**Rule**: Dependencies flow strictly downward: `Feature → UI → Data-Access → Utility`

```
Feature Libraries
      ↓
UI Libraries (NO Data-Access imports!)
      ↓
Data-Access Libraries (NO UI imports!)
      ↓
Utility Libraries (Self-contained)
```

**Trade-off**: More fine-grained libraries. Developers cannot "conveniently" import a service into a shared UI component.

**Maintenance Nightmare Prevented**:
- **Circular Dependencies** - structural cancer that causes bootstrap paradoxes
- **Spaghetti Code** - where a generic `UserCard` accidentally triggers `AuthService.logout()`, making it impossible to reuse or test in isolation

---

## Automated Boundary Enforcement

Architecture in documentation is hallucination. Enforce via build system.

### Nx Constraints and Tagging

In `project.json` or `nx.json`, tag projects with dimensions:
- `scope`: The domain (e.g., `scope:booking`, `scope:check-in`)
- `type`: The layer (e.g., `type:feature`, `type:ui`, `type:data-access`)

Configure `@nx/enforce-module-boundaries` ESLint rule:

```json
{
  "rules": {
    "@nx/enforce-module-boundaries": [
      "error",
      {
        "depConstraints": [
          { "sourceTag": "type:feature", "onlyDependOnLibsWithTags": ["type:ui", "type:data-access", "type:util"] },
          { "sourceTag": "type:ui", "onlyDependOnLibsWithTags": ["type:util"] },
          { "sourceTag": "type:data-access", "onlyDependOnLibsWithTags": ["type:util"] },
          { "sourceTag": "scope:booking", "onlyDependOnLibsWithTags": ["scope:booking", "scope:shared"] }
        ]
      }
    ]
  }
}
```

### Sheriff for TypeScript

For non-Nx projects, use Sheriff via `sheriff.config.ts`:

```typescript
import { defineConfig } from '@softarc/sheriff';

export default defineConfig({
  modules: {
    'src/app/features/<feature>': 'feature:<feature>',
    'src/app/ui': 'ui',
    'src/app/data-access': 'data-access',
    'src/app/util': 'util',
  },
  depRules: {
    'feature:*': ['ui', 'data-access', 'util'],
    'ui': ['util'],
    'data-access': ['util'],
    'util': [],
  },
});
```

### The Automated Gatekeeper Heuristic

**Rule**: Every commit must pass strict linting that verifies module boundaries. NO architectural exemptions (`eslint-disable`) without documented review.

**Maintenance Nightmare Prevented**: The "Big Ball of Mud" where changing a single utility triggers cascading compilation errors across unrelated domains.

---

## Facade Pattern

### The Component-Service Firewall

**Rule**: Smart Components must never inject `HttpClient`, `Router`, or raw State Stores directly. Inject a domain-specific Facade.

```typescript
// ❌ VIOLATION: Direct infrastructure coupling
@Component({...})
export class UserListComponent {
  constructor(
    private http: HttpClient,
    private store: Store<AppState>
  ) {}

  loadUsers() {
    this.http.get('/api/users').subscribe(users =>
      this.store.dispatch(setUsers({ users }))
    );
  }
}

// ✅ COMPLIANT: Facade abstraction
@Component({...})
export class UserListComponent {
  users = this.userFacade.users; // Signal

  constructor(private userFacade: UserFacade) {}

  loadUsers() {
    this.userFacade.loadUsers();
  }
}
```

**Trade-off**: Additional layer of indirection (a class) for every feature.

**Maintenance Nightmare Prevented**: **Refactoring Paralysis** - If backend API changes (REST → GraphQL) or state library is swapped (Akita → SignalStore), every component consuming that data requires rewriting. With a Facade, only the Facade implementation changes; hundreds of dependent components remain untouched.

---

## Hexagonal Architecture (Ports and Adapters)

For complex, long-lived business rules, use Angular's DI to implement strict Hexagonal Architecture.

### The Invert the Infrastructure Heuristic

**Rule**: Core Domain defines Ports (Abstract Classes/Injection Tokens) for external data access. Infrastructure implements these as Adapters.

```typescript
// 1. PORT: In Domain Library
export abstract class UserGateway {
  abstract getAll(): Observable<User[]>;
  abstract getById(id: string): Observable<User>;
}

// 2. ADAPTER: In Infrastructure Library
@Injectable()
export class HttpUserGateway implements UserGateway {
  constructor(private http: HttpClient) {}

  getAll(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }

  getById(id: string): Observable<User> {
    return this.http.get<User>(`/api/users/${id}`);
  }
}

// 3. PROVISION: In app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    { provide: UserGateway, useClass: HttpUserGateway }
  ]
};
```

**Trade-off**: High cognitive load for setup. Requires understanding DI tokens and abstract classes.

**Maintenance Nightmare Prevented**:
- **Vendor Lock-in**: Enables full domain testing without browser/network by swapping `HttpUserGateway` with `InMemoryUserGateway`
- **Platform Migration**: Core logic remains invariant when moving to Electron, Capacitor, or other platforms

---

## Circular Dependency Prevention

### The Third-Party Arbiter Heuristic

**Rule**: If Service A needs Service B, and Service B needs Service A, extract shared state/logic into Service C that both depend on. The dependency graph MUST be a Directed Acyclic Graph (DAG).

```
// ❌ CIRCULAR
ServiceA ←→ ServiceB

// ✅ ACYCLIC
ServiceA → ServiceC ← ServiceB
```

**Trade-off**: Requires vigilance and frequent refactoring. Forces redesign over "quick fix" imports.

**Maintenance Nightmare Prevented**:
- **Bootstrap Paradox**: Application fails at startup unpredictably based on module load order
- **Bundle Bloat**: Circular deps prevent tree-shaking and code splitting, creating massive initial bundles

---

## Pattern Reference Summary

| Pattern | Context | Goal | Nightmare Prevented |
|---------|---------|------|---------------------|
| Facade | Component ↔ State | Decouple UI from Business Logic | Refactoring Paralysis |
| SignalStore | Feature State | Localized reactive state | The God Store |
| Humble Object | Unit Testing | Extract logic from View | The TestBed Tax |
| Hexagonal | Data Access | Swappable Infrastructure | Vendor Lock-in |
| Standalone | Module Structure | Tree-shakability | SharedModule Bloat |
| Library Types | Folder Structure | Enforce Dependency Rules | Spaghetti Graph |
