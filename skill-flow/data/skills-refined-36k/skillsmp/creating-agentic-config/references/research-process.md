# Research Process for Creating AGENTS.md

Step-by-step process for analyzing a project and creating an effective AGENTS.md.

## Step 1: Analyze Project Structure

**Investigate thoroughly:**

1. **Identify tech stack:**
   - Backend: Check `composer.json`, `package.json`, `requirements.txt`, `go.mod`, etc.
   - Frontend: Check `package.json` for React, Vue, Svelte, etc.
   - Build tools: Vite, Webpack, esbuild, etc.
   - Testing: Jest, Vitest, Pest, Playwright, etc.

2. **Find version information:**
   - Parse package managers for versions
   - Check framework-specific files (e.g., `bootstrap/app.php` for Laravel)
   - Identify language versions from config files

3. **Locate configuration files:**
   - Build: `vite.config.js`, `webpack.config.js`, `tsconfig.json`
   - Test: `vitest.config.js`, `jest.config.js`, `phpunit.xml`, `pest.php`
   - Lint: `.eslintrc`, `pint.json`, `phpstan.neon`, `rector.php`
   - Format: `.prettierrc`, `pint.json`

4. **Map directory structure:**
   - Read top-level directories
   - Identify key source directories
   - Find test directories
   - Locate asset directories

## Step 2: Identify Commands

**Extract from multiple sources:**

1. **Package manager scripts:**
   - `package.json` → `scripts` section
   - `composer.json` → `scripts` section
   - `Makefile` → targets
   - `justfile` → recipes

2. **Common commands to find:**
   - Development server: `npm run dev`, `composer run dev`, `make dev`
   - Build: `npm run build`, `composer run build`
   - Test: `npm test`, `composer test`, `pytest`, `go test`
   - Lint: `npm run lint`, `composer run lint`
   - Format: `npm run format`, `composer run pint`
   - Type check: `npm run type-check`, `composer run stan`
   - Quality: `composer run checks`, `npm run checks`

3. **Look for combined commands:**
   - All-in-one quality checks
   - Pre-commit hooks
   - CI/CD scripts in `.github/workflows/`

## Step 3: Discover Architecture Decisions

**Read project documentation and code:**

1. **Check existing documentation:**
   - README.md
   - CONTRIBUTING.md
   - docs/ directory
   - Architecture Decision Records (ADRs)
   - Inline comments in config files

2. **Infer from code patterns:**
   - State management: Redux, Zustand, Vuex, Context API
   - Data fetching: TanStack Query, SWR, Apollo
   - Routing: React Router, Next.js, Inertia.js
   - API layer: tRPC, REST, GraphQL
   - Code organization: Feature-based, domain-driven, MVC

3. **Identify conventions:**
   - File naming (camelCase, kebab-case, PascalCase)
   - Component patterns (hooks, composition, class components)
   - Import patterns (absolute vs relative, barrel exports)
   - Error handling approaches
   - Testing strategies (unit, integration, e2e)

## Step 4: Find Quality Standards

**Determine verification requirements:**

1. **Coverage thresholds:**
   - Check test config files for coverage thresholds
   - Look for coverage requirements in CI

2. **Type coverage:**
   - TypeScript strict mode settings
   - PHPStan level
   - Type coverage requirements

3. **Linting rules:**
   - ESLint configuration
   - Pint/PHP-CS-Fixer rules
   - Custom rule sets

4. **Pre-commit hooks:**
   - Check `.husky/`, `lefthook.yml`, `.git/hooks/`
   - Identify automated checks

## Step 5: Create Progressive Disclosure Structure

**Organize detailed documentation:**

1. **Identify what should be external:**
   - Detailed API patterns
   - Component style guides
   - Testing strategies
   - Deployment procedures
   - Troubleshooting guides

2. **Create `docs/` or `agent_docs/` directory if needed**

3. **Reference in AGENTS.md:**
   - Use `@path/to/doc.md` syntax
   - Keep references concise
   - Only reference truly useful docs

## Step 6: Draft AGENTS.md

**Writing process:**

1. **Start with the stack summary** (1-2 sentences)
2. **Add Quick Commands** (5-10 most essential)
3. **Map Key Directories** (5-10 most important with PURPOSE)
4. **Document Architecture Decisions** (3-5 critical ones)
5. **List Verification Requirements** (clear checklist)
6. **Add Progressive Disclosure references** (if applicable)
7. **Count lines** - aim for 60-100 lines
8. **Review and ruthlessly cut** anything not universal

## Step 7: Handle Existing AGENTS.md

If AGENTS.md already exists:

1. **Read the current file completely**
2. **Analyze what's working:**
   - Accurate commands?
   - Current tech stack?
   - Useful architecture notes?
3. **Identify improvements:**
   - Outdated information?
   - Non-universal instructions?
   - Missing critical commands?
   - Too long (>100 lines)?
4. **Preserve good content:**
   - Keep accurate, universal instructions
   - Keep valid custom commands/agents references
   - Keep working progressive disclosure links
5. **Improve or replace:**
   - Update outdated tech versions
   - Remove non-universal instructions
   - Add missing critical commands
   - Move detailed content to external docs
   - Reduce to 60-100 lines if too long

## Step 8: Create External Documentation (If Needed)

If content exceeds 100 lines:

1. **Create docs directory:**

   ```bash
   mkdir -p docs/agent_docs
   ```

2. **Move detailed content to separate files:**
   - `docs/agent_docs/architecture.md` - Detailed architecture
   - `docs/agent_docs/testing-guide.md` - Testing strategies
   - `docs/agent_docs/api-patterns.md` - API conventions
   - `docs/agent_docs/component-guide.md` - Component patterns

3. **Reference in AGENTS.md:**

   ```markdown
   ## For More Context

   - @docs/agent_docs/architecture.md for architecture details
   - @docs/agent_docs/testing-guide.md for testing strategies
   ```

## Step 9: Validate and Refine

**Quality checklist:**

1. **Length check**: Is it under 100 lines? If not, move content to external docs
2. **Universal check**: Is every instruction applicable to EVERY task?
3. **Actionable check**: Are commands exact with no ambiguity?
4. **Freshness check**: Will this stay fresh or go stale? (No code snippets!)
5. **Verification check**: Can developers actually follow the "Before Committing" steps?

## Step 10: Explain to User

After creating/updating AGENTS.md, explain:

1. **What was created/updated**
2. **Key sections included**
3. **Why certain decisions were made**
4. **What was intentionally excluded (and why)**
5. **How to use the file**
6. **Suggestion to commit to Git**
