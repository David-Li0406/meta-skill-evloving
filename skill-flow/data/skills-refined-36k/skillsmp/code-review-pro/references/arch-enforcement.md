# Architectural Enforcement (Boundary Protection)

## Monorepo Boundaries
In a monorepo, it's easy to accidentally import a "Private" utility into a "Public" package.

### 1. The "Public vs. Private" Rule
- **Rule**: Apps cannot import from `src/` of another package. They must use the defined `exports` in `package.json`.
- **Enforcement**: Use `eslint-plugin-import` or `dependency-cruiser` to flag violations.

---

### 2. Service Pattern Enforcement
- **Rule**: UI components cannot call the DB directly. They must go through a Service layer.
- **Audit**: Search for `PrismaClient` or `ctx.db` calls inside `.tsx` files.

---

### 3. State Management Isolation
- **Rule**: Global state (Zustand/Redux) should not be directly mutated by child components.
- **Elite Pattern**: Use "Action Hooks" to encapsulate all mutations.

---

### 4. Cross-App Communication
- **Rule**: Apps should communicate via APIs or Shared Packages, never by direct file referencing.
- **Audit**: Look for relative paths that exit the workspace directory (e.g., `../../../apps/other-app/...`).
