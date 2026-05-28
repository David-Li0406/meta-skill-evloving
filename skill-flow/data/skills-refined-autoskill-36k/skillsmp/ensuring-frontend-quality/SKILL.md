---
name: ensuring-frontend-quality
description: Run frontend quality checks including ESLint, Prettier, and TypeScript compilation. Use when ensuring frontend code quality, before committing, running checks, or when user mentions quality, checks, ESLint, Prettier, TypeScript, or npm run checks.
---

# Ensure Frontend Quality

Run frontend quality checks including ESLint for linting, Prettier for formatting, and TypeScript compilation for type safety. Execute `npm run checks` before committing to ensure all code meets project standards and catches issues early.

## Quality Tools

This project uses these frontend quality tools:

1. **ESLint** - JavaScript/TypeScript linting
2. **Prettier** - Code formatting
3. **TypeScript** - Type checking and compilation
4. **Vite** - Build tool for production bundles

## Running All Checks

```bash
npm run checks
```

This runs:

1. ESLint with auto-fix
2. Prettier with auto-fix

## Individual Tools

### ESLint - Code Linting

**Run ESLint:**

```bash
npm run lint
# or
eslint --fix 'resources/js/**/*.{js,jsx,ts,tsx}'
```

**What it does:**

- Finds code quality issues
- Enforces coding standards
- Detects potential bugs
- Auto-fixes many issues

**Configuration:** `eslint.config.js`

**Rules enforced:**

- React best practices
- TypeScript rules
- React Hooks rules
- Prettier integration

**Common issues caught:**

- Unused variables
- Missing dependencies in useEffect
- Incorrect hook usage
- Type errors
- Console statements in production

### Prettier - Code Formatting

**Run Prettier:**

```bash
npm run format
# or
prettier --write 'resources/js/**/*.{js,jsx,ts,tsx}'
```

**What it does:**

- Formats code consistently
- Enforces style rules
- Auto-fixes formatting
- Organizes imports

**Configuration:** `.prettierrc`

**Formats:**

- Indentation (2 spaces)
- Line length (80-100 chars)
- Quote style (single quotes)
- Semicolons (consistent)
- Trailing commas
- Import organization (with prettier-plugin-organize-imports)
- Tailwind class sorting (with prettier-plugin-tailwindcss)

### TypeScript - Type Checking

**Run TypeScript check:**

```bash
npx tsc --noEmit
```

**What it does:**

- Checks type correctness
- Validates imports
- Ensures type safety
- Catches type errors before runtime

**Configuration:** `tsconfig.json`

**Strict mode enabled:**

- No implicit any
- Strict null checks
- Strict function types
- No unused locals/parameters

### Vite Build Check

**Run production build:**

```bash
npm run build
```

**What it does:**

- Compiles TypeScript
- Bundles for production
- Optimizes assets
- Validates imports
- Checks for build errors

**Configuration:** `vite.config.js`

## Quality Standards

### Required for All Frontend Code

1. **Type Safety:**
   - Use `import type` for type imports
   - Full type annotations on function parameters
   - Return types on complex functions
   - No `any` types (use `unknown` if needed)

2. **Code Style:**
   - Passes ESLint checks
   - Formatted with Prettier
   - Organized imports
   - Sorted Tailwind classes

3. **React Best Practices:**
   - Use React 19 patterns (no FC type)
   - Proper hook dependencies
   - Key props on lists
   - Type-safe props with TypeScript

4. **Import Patterns:**
   - Use path aliases (@/components, @/hooks)
   - Type imports with `import type`
   - Named exports (except pages use default)

## Common Issues and Fixes

### Issue: Type Import Error

```
❌ 'PropsWithChildren' is a type and must be imported using a type-only import
```

**Fix:**

```tsx
// Before
import { PropsWithChildren } from 'react'

// After
import type { PropsWithChildren } from 'react'
```

### Issue: Missing Hook Dependencies

```
❌ React Hook useEffect has a missing dependency: 'fetchData'
```

**Fix:**

```tsx
// Before
useEffect(() => {
  fetchData()
}, [])

// After
useEffect(() => {
  fetchData()
}, [fetchData]) // Add dependency

// Or use useCallback
const fetchData = useCallback(() => {
  // ...
}, [])
```

### Issue: Type Errors

```
❌ Property 'name' does not exist on type 'User | null'
```

**Fix:**

```tsx
// Before
const userName = user.name

// After
const userName = user?.name ?? 'Guest'

// Or check first
if (user) {
  const userName = user.name
}
```

### Issue: Unused Variables

```
❌ 'response' is assigned a value but never used
```

**Fix:**

```tsx
// Before
const response = await fetch(url)

// After
await fetch(url)

// Or use it
const response = await fetch(url)
console.log(response.status)
```

## Integration with Workflow

### Pre-commit Checks

Run before committing:

```bash
npm run checks
```

### Development Mode

Vite provides hot module replacement:

```bash
npm run dev
```

### Production Build

Test production build:

```bash
npm run build
```

## File Organization Standards

### Components

```
resources/js/components/
├── ui/              # shadcn/ui components
├── icons/           # Icon components
├── data-table/      # Data table components
└── *.tsx            # Shared components
```

### Pages (Inertia)

```
resources/js/pages/
├── auth/            # Authentication pages
├── account/         # Account pages
└── dashboard/       # Dashboard pages
```

### Hooks

```
resources/js/hooks/
└── use-*.ts         # Custom hooks
```

### Types

```
resources/js/types/
├── index.d.ts       # Inertia types
├── models.d.ts      # Laravel model types
└── global.d.ts      # Global types
```

## Anti-Patterns

### ❌ Don't Do This

```tsx
// Don't use React.FC
const Component: React.FC = () => {} // ❌

// Don't skip type imports
import { User } from '@/types/models' // ❌ for types

// Don't use any
function handle(data: any) {} // ❌

// Don't ignore ESLint
// eslint-disable-next-line // ❌

// Don't commit unformatted code
git commit -m "Quick fix" // ❌ Run checks first
```

### ✅ Do This Instead

```tsx
// Use function components
function Component() {}

// Use type imports
import type { User } from '@/types/models'

// Type properly
function handle(data: FormData) {}

// Fix ESLint issues
// (properly handle the warning)

// Run checks before commit
npm run checks
git commit -m "Fix form validation"
```

## Quality Checklist

Before committing frontend code:

- [ ] ESLint passes (no linting errors)
- [ ] Prettier formatted (code formatted)
- [ ] TypeScript compiles (no type errors)
- [ ] Build succeeds (npm run build works)
- [ ] No console.log in production code
- [ ] Imports organized and using path aliases
- [ ] Types properly imported with `import type`
- [ ] Components follow React 19 patterns

## Fixing Failed Checks

### ESLint Failed

```bash
# Auto-fix most issues
npm run lint

# See errors without fixing
npx eslint 'resources/js/**/*.{js,jsx,ts,tsx}'

# Fix specific file
npx eslint --fix resources/js/pages/auth/login.tsx
```

### Prettier Failed

```bash
# Auto-fix formatting
npm run format

# Check without fixing
npx prettier --check 'resources/js/**/*.{js,jsx,ts,tsx}'
```

### TypeScript Failed

```bash
# Check types
npx tsc --noEmit

# See detailed errors
npx tsc --noEmit --pretty

# Fix errors manually (no auto-fix)
```

### Build Failed

```bash
# See build errors
npm run build

# Common fixes:
# - Fix import paths
# - Fix type errors
# - Remove unused imports
# - Fix syntax errors
```

## IDE Integration

### VS Code

**Recommended extensions:**

- ESLint
- Prettier
- TypeScript and JavaScript Language Features
- Tailwind CSS IntelliSense

**Settings (.vscode/settings.json):**

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

### PHPStorm/WebStorm

**Configuration:**

- Enable ESLint: Preferences → Languages → JavaScript → ESLint
- Enable Prettier: Preferences → Languages → JavaScript → Prettier
- Set Prettier as default formatter
- Enable "Run eslint --fix on save"

## Quality Commands Reference

```bash
# Run all checks
npm run checks

# Individual tools
npm run lint        # ESLint with auto-fix
npm run format      # Prettier with auto-fix
npm run dev         # Development server
npm run build       # Production build

# With options
npx eslint --fix path/to/file.tsx  # Fix specific file
npx prettier --write path/to/file.tsx  # Format specific file
npx tsc --noEmit  # Type check only
```

## Common ESLint Rules

**React Hooks:**

- `react-hooks/rules-of-hooks` - Enforces hooks rules
- `react-hooks/exhaustive-deps` - Checks effect dependencies

**TypeScript:**

- `@typescript-eslint/no-unused-vars` - No unused variables
- `@typescript-eslint/no-explicit-any` - Avoid any types
- `@typescript-eslint/explicit-module-boundary-types` - Type function returns

**React:**

- `react/prop-types` - Disabled (using TypeScript)
- `react/react-in-jsx-scope` - Disabled (React 19)
- `react/jsx-key` - Require keys on list items

## Maintaining High Quality

1. Run checks frequently during development
2. Fix issues immediately (don't accumulate)
3. Use TypeScript strictly (no `any`)
4. Keep imports organized with aliases
5. Format on save in your IDE
6. Run full checks before pushing
7. Test production build periodically
