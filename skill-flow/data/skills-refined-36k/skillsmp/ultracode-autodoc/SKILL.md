---
name: UltraCode AutoDoc
version: 1.0.0
description: Working with .autodoc/ directory, automatic documentation generation, semantic doc search
triggers:
  - autodoc
  - documentation
  - .autodoc
  - doc generation
---

# UltraCode AutoDoc — Claude Code Skill

**Auto-activated for**: Working with `.autodoc/` directory, documentation generation

AutoDoc — automatic code documentation system with semantic search.

## Key Features

### 🔗 Auto-updated Code References
All code references in AutoDoc are **automatically kept up-to-date**. When code moves or changes, line number references are updated automatically — they're always accurate.

### 🧠 Project Memory
AutoDoc describes the **meaning** of your application — processes, scenarios, business logic. Search finds relevant code even when there are **no keywords or comments** in the code itself. The documentation links directly to code sections.

### 📝 Human + Auto Hybrid
- **Empty `AUTODOC.md` files** in module folders are auto-generated from code structure
- **You can enrich them** with descriptions, scenarios, business context
- Everything you add is **preserved** and becomes searchable "project memory"
- System only updates code line references, never overwrites your content

### ⚡ Instant Semantic Search
`autodoc_search` searches **code AND documentation simultaneously**. Results are enriched with context from both sources — find code by business meaning, not just keywords.

---

## Concept

**AutoDoc ≠ code comments**

| Comments | AutoDoc |
|----------|---------|
| HOW code works | WHY, WHO uses, WHICH scenarios |
| Local context | Business context + architecture |
| For developer in IDE | For AI + system understanding |
| Keywords required to find | Find by meaning, no keywords needed |

---

## .autodoc/ Structure

```
.autodoc/
├── ARCHITECTURE.md    # System components (create manually)
├── FLOW.md            # Business scenarios (create manually)
├── PROCESSES.md       # Technical processes (create manually)
├── DEPENDENCIES.md    # Packages, APIs, microservices (create manually)
├── DEPLOYMENT.md      # Build, CI/CD, ENV (create manually)
├── GLOSSARY.md        # Terms (create manually)
│
└── src/               # Mirrors code structure
    ├── _index.md      # Directory overview
    ├── module/
    │   ├── AUTODOC.md # Auto-generated, enrichable
    │   └── ...
    └── ...
```

> **Note**: Top-level documents (`ARCHITECTURE.md`, `FLOW.md`, etc.) should be created manually. Module-level `AUTODOC.md` files are auto-generated but can be enriched. All code references are auto-updated.

---

## Using AutoDoc

### If Project Has `.autodoc/`

**ALWAYS use AutoDoc for understanding the project:**

1. **Start with `autodoc_search`** — instant semantic search across code + docs
2. **Read `.autodoc/` files** — business context that helps find code by meaning

| File | Read when... |
|------|--------------|
| `ARCHITECTURE.md` | Need to understand project structure |
| `FLOW.md` | Need to understand business scenarios |
| `PROCESSES.md` | Need to understand technical processes |
| `DEPENDENCIES.md` | Need to understand external dependencies |
| `DEPLOYMENT.md` | Need to understand build, CI/CD |
| `src/**/AUTODOC.md` | Need to understand specific module |

### If Project Doesn't Have `.autodoc/`

Suggest to user: "Would you like to enable AutoDoc for this project?"
→ `autodoc_init({ language: 'ru' })` or `'en'`

Then:
1. Auto-generate module `AUTODOC.md` files: `autodoc_generate preview=false`
2. Create top-level docs manually: `ARCHITECTURE.md`, `FLOW.md`, etc.
3. Enrich module docs with business context as you learn the codebase

---

## MCP Tools

### Initialization & Status

#### `autodoc_init`
Initialize AutoDoc. Sets documentation language.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | true | Enable AutoDoc |
| `language` | enum | "en" | `en` / `ru` / `zh` |
| `docsDir` | string | ".autodoc" | Documentation directory |

#### `autodoc_status`
Status: enabled/disabled, statistics (docs, sections, refs).

#### `autodoc_detect_language`
Auto-detect language from code comments and existing docs.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `scope` | enum | "all" | `comments` / `docs` / `all` |
| `sampleSize` | number | 20 | Files to sample |

### Search & Read

#### `autodoc_search`
**Semantic search across code + documentation.**
Use instead of regular search — provides context!

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | **required** | Search query |
| `mode` | enum | "hybrid" | `text` / `semantic` / `hybrid` |
| `limit` | number | 10 | Max results |

#### `autodoc_get`
Get documentation by path. If section specified — only that section.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `filePath` | string | - | File path |
| `docId` | string | - | Document ID |

### Save

#### `autodoc_save`
Save document. Automatically:
- Parses references
- Generates embeddings for semantic search
- Extracts sections

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `filePath` | string | **required** | File path |
| `content` | string | **required** | Markdown content |
| `type` | enum | - | Document type |

### Validation & Sync

#### `autodoc_validate`
Check all references, optionally fix broken ones.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `fixBroken` | boolean | false | Fix broken refs |

#### `autodoc_sync`
Sync documentation with code changes.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `scope` | enum | "outdated" | `all` / `outdated` / `file` |
| `direction` | enum | "both" | `both` / `disk-to-db` / `db-to-disk` |

### Auto-generate

#### `autodoc_generate`
Auto-generate documentation for the codebase.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `preview` | boolean | true | Preview without writing |
| `useLlm` | boolean | false | Use LLM for descriptions |
| `incremental` | boolean | true | Only update changed |
| `language` | enum | "auto" | `auto` / `en` / `ru` / `zh` |
| `module` | string | - | Generate for single module |

### History

#### `autodoc_changelog`
View documentation change history.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | number | 20 | Max entries |
| `since` | timestamp | - | Filter since |

---

## Workflows

### 1. Initialize Project Documentation

```
User: "Document this project"

1. autodoc_detect_language({ scope: 'comments' })
   → Detect language from comments

2. autodoc_init({ enabled: true, language: 'ru' })
   → Initialize AutoDoc

3. autodoc_status()
   → Show current state

4. Create .autodoc/ with documentation
   autodoc_save({ filePath: 'ARCHITECTURE.md', content: '...' })
```

### 2. Understand Existing Project

```
User: "How does authentication work?"

1. autodoc_search({ query: "authentication auth", mode: 'semantic' })
   → Finds documentation + code

2. autodoc_get({ filePath: 'FLOW.md', section: 'registration' })
   → Business scenario

3. autodoc_get({ filePath: 'PROCESSES.md', section: 'auth-flow' })
   → Technical implementation
```

### 3. After Code Changes

```
User: "Added rate limiting to AuthService"

1. autodoc_sync({ scope: 'outdated' })
   → Find outdated documents

2. autodoc_validate()
   → Check references

3. autodoc_save({
     filePath: 'src/services/auth/auth.service.md',
     content: '...'
   })

4. autodoc_changelog({ limit: 5 })
   → Show recent changes
```

### 4. Auto-Update (Watcher)

AutoDoc Watcher works automatically when enabled:

```yaml
# ultrascript.yaml
mcp:
  autodoc:
    watcherEnabled: true
    debounceMs: 45000    # base delay
```

On .ts/.js file changes:
1. Watcher detects changes via KnowledgeBus
2. Debounce 30-60 sec (groups multiple changes)
3. Updates AUTODOC.md in corresponding module:
   - Adds new exports
   - Removes deleted exports
   - Updates line numbers in references

---

## Entity-Level Documentation Format

**DON'T duplicate comments!** Write about:
- Role in system (WHY)
- Who uses it (BY WHOM)
- Participation in processes (WHERE)
- Business invariants
- Critical dependencies
- Known issues

```markdown
# AuthService

[→ auth.service.ts:15-120](auth.service.ts#L15-L120)

## Role in System

**Why needed**: Single point for authentication management...

## Who Uses

| Consumer | How |
|----------|-----|
| [→ API Gateway](../../gateway/README.md) | Token validation |

## Participation in Processes

- [→ FLOW.md#registration](../../FLOW.md#registration)
- [→ PROCESSES.md#auth-flow](../../PROCESSES.md#auth-flow)

## Business Invariants

- One active token per user
- Rate limiting: 5 attempts/min
```

---

## Reference Syntax

```markdown
[→ file.ts:25-50](file.ts#L25-L50)     # To code lines
[→ ModuleName](./_index.md)             # To documentation
[→ FLOW.md#scenario](../../FLOW.md#scenario)  # To section
```

In code comments:
```typescript
/**
 * @see docs://.autodoc/PROCESSES.md#auth-flow
 * @flow user-registration, api-auth
 */
```

---

## Related Skills

- **`ultracode`** — Code analysis, semantic search, refactoring, code modification
- **`ultracode-trace`** — Debugging, flow analysis, "why not called"
