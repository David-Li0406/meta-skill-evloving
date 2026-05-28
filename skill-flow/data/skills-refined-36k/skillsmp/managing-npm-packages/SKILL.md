---
name: managing-npm-packages
description: Manage npm packages, dependencies, and package.json configuration for React applications. Use when installing packages, updating dependencies, configuring scripts, or when user mentions npm, packages, dependencies, or package management.
---

# Manage npm Packages

Manage npm packages, dependencies, and package.json configuration for React applications. Install production dependencies for runtime code and dev dependencies for build tools, keeping the dependency tree clean and well-organized.

## File Structure

Package configuration is in the project root:

```
package.json              # Package manifest
package-lock.json         # Locked dependency tree
node_modules/             # Installed packages (gitignored)
```

## Core Conventions

### 1. Installing Packages

**Production dependencies:**

```bash
npm install react-hook-form
npm install zod
npm install @inertiajs/react
```

**Development dependencies:**

```bash
npm install -D @types/react
npm install -D typescript
npm install -D eslint
npm install -D prettier
```

**Specific versions:**

```bash
npm install react@19.0.0
npm install tailwindcss@^4.0.0
```

### 2. Package.json Structure

```json
{
  "name": "laravel-skeleton-react",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "checks": "prettier --check . && eslint .",
    "format": "prettier --write .",
    "preview": "vite preview"
  },
  "dependencies": {
    "@hookform/resolvers": "^3.9.1",
    "@inertiajs/react": "^2.0.0",
    "@radix-ui/react-slot": "^1.1.1",
    "axios": "^1.7.9",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "i18next": "^24.2.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-hook-form": "^7.54.2",
    "react-i18next": "^15.2.0",
    "tailwind-merge": "^2.6.0",
    "zod": "^3.24.1"
  },
  "devDependencies": {
    "@eslint/js": "^9.18.0",
    "@inertiajs/core": "^2.0.0",
    "@playwright/test": "^1.49.1",
    "@types/node": "^22.10.2",
    "@types/react": "^19.0.6",
    "@types/react-dom": "^19.0.2",
    "@vitejs/plugin-react": "^4.3.4",
    "eslint": "^9.18.0",
    "eslint-plugin-react-hooks": "^5.1.0",
    "laravel-vite-plugin": "^1.1.1",
    "prettier": "^3.4.2",
    "prettier-plugin-organize-imports": "^4.1.0",
    "prettier-plugin-tailwindcss": "^0.6.9",
    "typescript": "^5.7.2",
    "typescript-eslint": "^8.19.1",
    "vite": "^6.0.3"
  }
}
```

### 3. Common Scripts

**Development:**

```bash
npm run dev          # Start Vite dev server with HMR
```

**Build:**

```bash
npm run build        # Build for production (TypeScript check + Vite build)
```

**Quality checks:**

```bash
npm run checks       # Run Prettier and ESLint
npm run format       # Format code with Prettier
```

**Preview:**

```bash
npm run preview      # Preview production build locally
```

### 4. Managing Dependencies

**Update packages:**

```bash
npm update                    # Update within semver ranges
npm update react              # Update specific package
npm outdated                  # Check for outdated packages
```

**Remove packages:**

```bash
npm uninstall lodash
npm uninstall -D @types/lodash
```

**Check for security issues:**

```bash
npm audit
npm audit fix
```

## Examples

### Example 1: Installing React Packages

```bash
# Install React Hook Form and Zod for form handling
npm install react-hook-form @hookform/resolvers zod

# Install types
npm install -D @types/react @types/react-dom
```

### Example 2: Installing shadcn/ui Components

```bash
# Install shadcn/ui (already done in this project)
# Add individual components
npx shadcn@latest add button
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add dialog
```

### Example 3: Adding Utility Libraries

```bash
# Install es-toolkit (modern lodash alternative)
npm install es-toolkit

# Install date-fns for date utilities
npm install date-fns

# Install react-use for hooks
npm install react-use
```

### Example 4: Adding Testing Packages

```bash
# Install Playwright for browser testing
npm install -D @playwright/test

# Install React Testing Library
npm install -D @testing-library/react @testing-library/jest-dom
```

## Anti-Patterns

### ❌ Don't Do This

```bash
# Don't install packages globally
npm install -g react  # ❌ Use local installation

# Don't mix package managers
npm install react
yarn add vue  # ❌ Use one package manager consistently

# Don't commit node_modules
git add node_modules/  # ❌ Add to .gitignore

# Don't skip package-lock.json
rm package-lock.json  # ❌ Commit this file

# Don't use outdated packages
npm install react@16  # ❌ Use latest stable versions

# Don't install everything as dev dependencies
npm install -D react  # ❌ React is a production dependency
```

### ✅ Do This Instead

```bash
# Install packages locally
npm install react

# Use one package manager (npm in this project)
npm install react

# Gitignore node_modules
# (already configured in .gitignore)

# Commit package-lock.json
git add package-lock.json

# Use latest stable versions
npm install react@latest

# Install production dependencies correctly
npm install react  # Production
npm install -D @types/react  # Development
```

## Package Categories

### Production Dependencies

Packages needed in production:

- **React ecosystem:** `react`, `react-dom`, `react-i18next`
- **Inertia.js:** `@inertiajs/react`
- **Forms:** `react-hook-form`, `zod`, `@hookform/resolvers`
- **UI:** `@radix-ui/*`, `class-variance-authority`, `clsx`, `tailwind-merge`
- **HTTP:** `axios`
- **Utilities:** `es-toolkit`, `date-fns`

### Development Dependencies

Packages only needed during development:

- **TypeScript:** `typescript`, `@types/*`
- **Build tools:** `vite`, `@vitejs/plugin-react`, `laravel-vite-plugin`
- **Linting:** `eslint`, `@eslint/js`, `eslint-plugin-react-hooks`, `typescript-eslint`
- **Formatting:** `prettier`, `prettier-plugin-*`
- **Testing:** `@playwright/test`

## Version Management

**Semver ranges:**

```json
{
  "dependencies": {
    "react": "^19.0.0", // ^: Allow minor and patch updates
    "axios": "~1.7.9", // ~: Allow patch updates only
    "zod": "3.24.1" // Exact version (no prefix)
  }
}
```

**Recommended approach:**

- Use `^` for most packages (allow minor/patch updates)
- Use exact versions for critical packages
- Always commit `package-lock.json`

## Troubleshooting

**Clear cache and reinstall:**

```bash
rm -rf node_modules package-lock.json
npm install
```

**Fix dependency conflicts:**

```bash
npm install --legacy-peer-deps
```

**Update all packages to latest:**

```bash
# Check what would be updated
npm outdated

# Update interactively (use npx npm-check-updates)
npx npm-check-updates -i

# Or update all to latest (careful!)
npx npm-check-updates -u
npm install
```

## Quality Standards

- Always use `npm` (not yarn or pnpm) in this project
- Commit `package-lock.json` to version control
- Install production dependencies without `-D` flag
- Install type definitions as dev dependencies
- Use semantic versioning (semver) ranges appropriately
- Run `npm audit` regularly to check for vulnerabilities
- Keep dependencies up to date (but test thoroughly)
- Document custom scripts in package.json
