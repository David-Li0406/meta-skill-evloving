# Project Structure

Our projects follow a consistent, feature-oriented structure to ensure scalability and clarity.

## Directory Layout (Front-end Web Example)

```
src/
├─ app/               # Next.js app directory (routes, layouts, pages) or main app entry
├─ assets/            # Static files (images, fonts, etc.)
├─ components/        # Reusable presentational components
│  ├─ ui/             # Shared low-level UI primitives (buttons, inputs)
│  └─ common/         # Higher-level reusable components (Navbar, Footer)
├─ features/          # Feature modules (group by business domain)
│  ├─ <featureName>/
│  │   ├─ components/    # Feature-specific UI components
│  │   ├─ hooks/         # Feature-specific hooks or logic (if not using Effect)
│  │   ├─ routes/        # Pages or API routes related to this feature (Next.js or Express routes)
│  │   ├─ services/      # Feature-specific business logic (could use Effect)
│  │   └─ types.ts       # Feature-specific TypeScript types
├─ lib/              # Utilities and library code (not feature-specific)
│  ├─ api/            # API clients or networking code
│  ├─ config/         # Configuration (perhaps tsdown config, tailwind config, etc.)
│  ├─ hooks/          # Reusable hooks (if not using Effect exclusively)
│  └─ utils/          # Generic utility functions (dates, strings, etc.)
├─ state/            # Global state management (e.g., Zustand stores or context providers)
├─ tests/            # Test utilities or integration test setups (if not colocated)
└─ index.tsx         # App entry (for React/Vite) or main server file (for Node)
```

This structure groups by feature, which scales better than grouping strictly by technical type. Features encapsulate their UI, logic, and types, reducing cross-module coupling.

For backend Node projects (Express, etc.), a similar approach applies:

```
src/
├─ modules/          # Business domains or bounded contexts
│   └─ <moduleName>/
│        ├─ routes/        # Express routers or API endpoints
│        ├─ controllers/   # Route handlers controlling request flow
│        ├─ services/      # Core business logic (pure logic, or using Effect)
│        ├─ models/        # Data models (DB schema or domain models)
│        └─ types.ts       # Module-specific types
├─ lib/               # Shared libraries (database client setup, external API clients)
├─ middleware/        # Express (or other framework) middleware
├─ config/            # Configuration files (loaded via env or similar)
└─ index.ts           # Entry point to start the server
```

In Node, also consider grouping by context (e.g. a monorepo might have `packages/server` and `packages/shared` etc., but within a service, use feature modules as above).

## Feature-Focused Organization

Why feature modules? It limits the mental load. A developer can go to the `features/shoppingCart` directory and see everything about shopping cart logic in one place (UI, hooks, logic, types). This reduces hopping around and makes refactoring simpler.

Within a feature:

- Keep internal structure consistent (e.g., if one feature has a `hooks` folder, all should if they have custom hooks).
- Co-locate tests with the code when practical (e.g., `MyComponent.test.tsx` next to `MyComponent.tsx`) to make it easy to find tests.

## Shared vs Feature Code

Use `components/ui` for extremely reusable, context-agnostic pieces (e.g., a `Button` component). Use `components/common` for moderately reusable pieces that might span a couple of features (e.g., a generic modal). Everything domain-specific goes in a feature folder.

Similarly, utilities that are widely useful (like a date format function) go in `lib/utils`. But a helper function only relevant to orders should live in `features/orders` (possibly in `services` or `utils` under that feature).

## Layering and Boundaries

Observe clear separation between:

- **UI Layer**: React components or CLI output formatting. These should not directly perform data fetching or complex computations; they call into hooks or services.
- **Service/Logic Layer**: Pure functions or Effect pipelines that implement business rules, do calculations, etc., oblivious to UI. They may call lower-level libraries (like a database client).
- **Data Layer**: Modules interfacing with external systems (database, filesystem, external APIs). Encapsulate these so that the rest of the app calls a clean interface (e.g., functions or Effect services) rather than raw queries.

For example, an Express route handler (in `routes`) calls a service function (in `services`) which might use an ORM or query (in `data` layer or `models`). The service returns a result (or throws), and the controller decides HTTP response. This layering improves testability and clarity.

## Project Config and Scripts

Keep project-wide configs in dedicated files/folders:

- **TSConfig**: have a base `tsconfig.json` and possibly extend for tests or build.
- **ESLint and Prettier** configs at root (ensure they cover all relevant files).
- If using `pnpm` workspaces (monorepo), ensure each package has a clear boundary (no cross-imports except via package exports).
- Leverage a root `README` to explain the structure to newcomers, and possibly a `CONTRIBUTING.md` that references these guidelines.

## Monorepo Considerations

If the project is part of a monorepo (common with `pnpm` workspaces):

- Each package follows a similar internal structure as above.
- Shared code goes in a `/packages/shared` or similar library package.
- Ensure no circular dependencies between packages; design with layering (e.g., a `core` library is used by both frontend and backend packages).
- Use tools like Nx or Turborepo if necessary to manage building and testing across packages, but keep each package cohesive.

## Example: CLI Tool Structure

For CLI projects (using Oclif):

```
src/
├─ commands/      # Oclif commands (each command as a file or folder with subcommands)
├─ core/          # Core logic that can be unit-tested (business logic behind commands)
├─ utils/         # CLI-specific utilities (parsing, formatting output)
├─ lib/           # External library wrappers or integrations (if any)
└─ index.ts       # CLI entry (initializes Oclif run)
```

This ensures commands remain thin (just argument parsing and calling core logic), which follows the same separation of concerns principle.

In all cases, strive for a project structure where finding things is intuitive (by feature or layer) and adding new features doesn’t require massive reorganization.
