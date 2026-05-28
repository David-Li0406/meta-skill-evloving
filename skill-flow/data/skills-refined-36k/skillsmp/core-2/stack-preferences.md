# Stack Preferences & Tooling

**Purpose**: Definitive guide to Jean-Marc's technology stack preferences, package managers, code style, and development tooling for Qara system.

---

## 🎯 Core Principles (Always Active)

### Language Hierarchy
1. **TypeScript** (preferred for everything)
2. **Rust** (when performance critical)
3. **Bash** (for system scripts)
4. **Python** (ONLY when explicitly approved)

### Why This Order?
- **TypeScript**: Type safety, excellent tooling, runs everywhere (Node, Deno, Bun)
- **Rust**: Performance, safety, systems programming
- **Bash**: Native to Unix systems, no dependencies
- **Python**: Slow interpreter, dependency hell, whitespace syntax issues

---

## 💾 Language Preferences

### TypeScript > Python (STRICT RULE)

**Default to TypeScript for**:
- Web development (frontend & backend)
- API servers and microservices
- CLI tools and scripts
- Data processing pipelines
- Automation workflows
- Build tools

**Use Python when**:
- Required by external dependency (e.g., machine learning library with no TS alternative)
- Contributing to existing Python codebase

**Why we avoid Python**:
- I am not specifically against python, but mindful of the following:
- Slower execution than TypeScript/Node
- Dependency management complexity (pip, conda, virtualenv, poetry...)
- Indentation-based syntax leads to subtle bugs
- Type hints added as afterthought (not core to language)
- GIL limitations for concurrency

### TypeScript Best Practices
```typescript
// ✅ Good: Explicit types, clear intent
interface User {
  id: string;
  email: string;
  createdAt: Date;
}

function getUserById(id: string): User | null {
  // Implementation
}

// ❌ Bad: Any types, implicit behavior
function getUser(id: any): any {
  // Implementation
}
```

---

## 📦 Package Manager Preferences (MANDATORY)

### JavaScript/TypeScript: Bun (NOT npm/yarn/pnpm)

**Use**: `bun` for all JS/TS projects
```bash
# Install dependencies
bun install

# Run script
bun run dev

# Execute file
bun index.ts

# Add package
bun add react
```

**Why Bun**:
- ⚡ **Fast**: 10-100x faster than npm
- 🎯 **All-in-one**: Package manager + runtime + test runner + bundler
- 🔒 **Secure**: Built-in lockfile, better dependency resolution
- 🆕 **Modern**: Native TypeScript, ESM first

**Forbidden**: npm, yarn, pnpm
- ❌ `npm install` → Use `bun install`
- ❌ `yarn add` → Use `bun add`
- ❌ `pnpm install` → Use `bun install`

### Python: uv (NOT pip)

**Use**: `uv` when Python is unavoidable
```bash
# Install dependencies
uv pip install -r requirements.txt

# Add package
uv pip install requests

# Create virtual environment
uv venv
```

**Why uv**:
- ⚡ **Fast**: Written in Rust, 10-100x faster than pip
- 🎯 **Simple**: Better dependency resolution
- 🔒 **Reliable**: More consistent than pip

**Forbidden**: pip, conda, poetry, pipenv
- ❌ `pip install` → Use `uv pip install`
- ❌ `conda install` → Use `uv pip install`

### Rust: cargo (standard)
```bash
cargo build
cargo test
cargo run
```

---

## 📝 Markup & Content Preferences

### Markdown > HTML (ZEALOTS)

**NEVER use HTML for basic content**:
- ❌ `<p>paragraph</p>` → Use markdown paragraph
- ❌ `<h1>header</h1>` → Use `# Header`
- ❌ `<ul><li>item</li></ul>` → Use `- item`
- ❌ `<a href="url">link</a>` → Use `[link](url)`
- ❌ `<strong>bold</strong>` → Use `**bold**`
- ❌ `<em>italic</em>` → Use `*italic*`

**HTML is ONLY acceptable for**:
- Custom components that don't exist in markdown: `<aside>`, `<callout>`, `<notes>`, `<details>`
- Complex layouts requiring CSS
- Interactive elements (forms, buttons with JavaScript)

**If you see HTML where markdown works**: That's a BUG - fix it.

### Markdown Best Practices
```markdown
✅ Good:
# Heading 1
## Heading 2

**Bold text** and *italic text*

- List item 1
- List item 2

[Link text](https://example.com)

> Blockquote

`inline code`

```typescript
code block
```

❌ Bad:
<h1>Heading 1</h1>
<h2>Heading 2</h2>

<strong>Bold text</strong> and <em>italic text</em>

<ul>
<li>List item 1</li>
<li>List item 2</li>
</ul>
```

---

## 🎨 Code Style & Conventions

### General Principles
- **Deterministic Code First** (from CONSTITUTION.md)
- **CLI-First Architecture** (from CONSTITUTION.md)
- **Explicit over implicit**
- **Readable over clever**
- **Boring is better than exciting**

### Naming Conventions
```typescript
// Files
- lowercase-with-dashes.ts (for files)
- PascalCase.tsx (for React components)

// Variables & functions
const userName = "value";        // camelCase
function getUserData() {}         // camelCase

// Types & interfaces
interface UserData {}             // PascalCase
type APIResponse = {};            // PascalCase

// Constants
const MAX_RETRIES = 3;            // SCREAMING_SNAKE_CASE
```

### Code Organization
```
project/
├── src/
│   ├── components/    # React components
│   ├── lib/           # Utility functions
│   ├── types/         # TypeScript types
│   └── index.ts       # Entry point
├── tests/
├── scripts/
└── README.md
```

---

## 🔧 Development Tools

### Editor
- [x] PHPStorm
- [x] Windsurf
- [x] VS Code


### Terminal
- [x] Warp
- [x] iTerm2 (macOS)
- [x] Konsole (Linux)

### Shell
- **Bash** (default for scripts)
- Fish/Zsh (if preferred for interactive use)

### Git Client
- **CLI-first approach** (git command line)
- GUI tools acceptable for complex merges/diffs
- `tig` for terminal-based git UI

---

## 🧪 Testing Philosophy

See `testing-guide.md` for comprehensive guide. Quick reference:

### Test Hierarchy (Preference Order)
1. **Unit tests** - Fast, isolated, many
2. **Integration tests** - Medium speed, some integration
3. **E2E tests** - Slow, full system, few

### Testing Tools
```typescript
// Preferred: Vitest (for unit/integration)
import { describe, it, expect } from 'vitest';

describe('getUserById', () => {
  it('returns user when found', () => {
    const user = getUserById('123');
    expect(user).toBeDefined();
  });
});

// Preferred: Playwright (for E2E)
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');
  // ...
});
```

---

## 🚀 Runtime Preferences

### JavaScript/TypeScript Runtimes
1. **Bun** (preferred) - Fast, all-in-one
2. **Node.js** (acceptable) - Wide compatibility
3. **Deno** (acceptable) - Good security model

### When to Use Each
- **Bun**: New projects, scripts, local tools
- **Node**: When ecosystem compatibility required
- **Deno**: When enhanced security needed

---

## 📊 Data Formats

### Preference Order
1. **JSON** - Configuration, APIs, data exchange
2. **YAML** - Human-readable config (use sparingly)
3. **TOML** - Rust projects
4. **XML** - Avoid unless required by external system

### Configuration Files
```typescript
// ✅ Preferred: JSON with comments (package.json, tsconfig.json)
{
  "name": "project",
  "version": "1.0.0"
}

// ✅ Acceptable: YAML for complex config
services:
  api:
    image: api:latest
    ports: [3000]

// ❌ Avoid: Custom config formats
```

---

## 🎯 Analysis vs Action Rule

**Critical Workflow Principle**: Distinguish between analysis and action requests.

### When User Says "Analyze"
```
✅ Do:
- Provide detailed analysis
- Explain findings
- Recommend options
- DON'T change anything

❌ Don't:
- Make code changes
- Modify files
- Execute actions
```

### When User Says "Implement" / "Fix" / "Update"
```
✅ Do:
- Take action
- Make changes
- Implement solution

❌ Don't:
- Just provide analysis
- Stop at recommendations
```

### Examples
```
"Analyze this code" → Analyze only, don't change
"Analyze and fix" → Both analyze AND fix
"What's wrong with X?" → Analyze only
"Fix X" → Take action
"Should I use X or Y?" → Analysis/recommendation
"Use X for this" → Take action
```

---

## 🛠️ Build & Bundle Tools

### Preferred Tools
- **Bun** - Build, bundle, test (all-in-one)
- **esbuild** - Fast bundling when Bun not suitable
- **Vite** - Frontend development (uses esbuild)

### Avoid
- Webpack (too slow, complex config)
- Rollup (unless specific plugin needed)
- Parcel (less control)

---

## 🗄️ Database Preferences

### Relational
- [x] SQLite
- [ ] MySQL
- [ ] PostgreSQL
- [ ] Other: ___________

### NoSQL
- [x] MongoDB
- [ ] Other: ___________

### ORM/Query Builders
- [x] Prisma
- [ ] Drizzle
- [ ] Other: ___________

---

## 🌐 Web Framework Preferences

### Frontend
- **Vue** - Component-based UI
- **Svelte** - Component-based UI
- **React** - Component-based UI
- **Next.js** - React with SSR/SSG
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Component library

### Backend
- **Hono** - Fast, lightweight web framework (Bun-compatible)
- **Fastify** - High-performance Node.js framework
- **Express** - When compatibility required (legacy)

---

## 📋 Linting & Formatting

### TypeScript/JavaScript
```bash
# Formatting: Prettier
bun run prettier --write .

# Linting: ESLint
bun run eslint .
```

### Configuration
```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}

// .eslintrc.json
{
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  "rules": {
    "no-console": "warn"
  }
}
```

---

## 🔗 Related Documentation
- See `testing-guide.md` for comprehensive testing guide (includes Playwright E2E setup)
- See `CONSTITUTION.md` for CLI-First and Deterministic Code principles
- See `TOOLS.md` for complete tool inventory

---

## 📝 Quick Reference Card

```
Languages:    TypeScript > Rust > Bash > (Python)
Packages:     bun (JS/TS), uv (Python)
Markup:       Markdown (HTML only for custom components)
Testing:      Vitest (unit), Playwright (E2E)
Runtime:      Bun > Node > Deno
Formatting:   Prettier + ESLint
Frontend:     React + Tailwind + shadcn/ui
Backend:      Hono > Fastify > Express
Analysis:     Don't change unless explicitly asked
```

---

**Last Updated**: 2025-11-19
**Needs Jean-Marc Input**:
- [ ] Why we hate Python (specific reasoning)
- [ ] Preferred editor
- [ ] Preferred terminal
- [ ] Database preferences
- [ ] ORM preference
