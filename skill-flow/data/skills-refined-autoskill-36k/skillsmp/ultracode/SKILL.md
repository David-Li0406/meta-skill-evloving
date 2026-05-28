---
name: UltraCode
version: 1.0.0
description: Code analysis for TS/JS/Python/Go/Rust/Java/C++/Swift/Kotlin/Bash
triggers:
  - code analysis
  - semantic search
  - refactoring
  - code modification
  - impact analysis
---

# UltraCode — Claude Code Skill

**Auto-activated for**: TS/JS/Python/Go/Rust/Java/C++/Swift/Kotlin/Bash code analysis

## When to Use

**ALWAYS use instead of Grep/Glob** — 5-10x faster, understands meaning.

| Task | Tool | Why |
|------|------|-----|
| Search code by meaning | `semantic_search` | Understands natural language |
| Find similar code | `find_similar_code` | Semantic similarity |
| Impact analysis | `analyze_code_impact` | Shows what breaks |
| Find duplicates | `detect_code_clones` | Semantic detection |
| List entities in file | `get_members` | AST parsing |
| Show dependencies | `list_entity_relationships` | Dependency graph |
| Modify code safely | `modify_code` | With preview & rollback |
| Rename across project | `rename_symbol` | Updates all references |

## Supported Languages

| Language | Support | Features |
|----------|---------|----------|
| TypeScript | ⭐⭐⭐ | Full type analysis, JSX/TSX |
| JavaScript | ⭐⭐⭐ | ES6+, JSX, CommonJS/ESM |
| Python | ⭐⭐⭐ | Type hints, async, decorators |
| Go | ⭐⭐⭐ | Goroutines, interfaces |
| Rust | ⭐⭐⭐ | Traits, lifetimes, macros |
| Java | ⭐⭐ | Generics, annotations |
| C++ | ⭐⭐ | Templates, namespaces |
| Swift | ⭐⭐ | Protocols, extensions |
| Kotlin | ⭐⭐ | Coroutines, data classes |
| Bash | ⭐ | Functions, variables |

> **For C# projects** use UltrasharpTools MCP — uses Roslyn for deep analysis.

---

## Code Modification via MCP

### ⚡ Automatic Validation

All code modifications (`modify_code`, `add_member`, `create_file`, `rename_symbol`) **automatically run linting and error checking**. Results are returned immediately in the response:

- ✅ **No errors** — change applied successfully
- ⚠️ **Warnings** — change applied, warnings listed
- ❌ **Errors** — change applied but errors detected, fix needed

No need to manually run validation — you get instant feedback on every change.

### Safe Modification Workflow

```
1. semantic_search query="target code"       # Find what to modify
2. get_members filePath="file.ts"            # Get entity IDs
3. analyze_code_impact entityId="..."        # Check what breaks
4. create_snapshot description="Before..."   # Backup
5. modify_code entityId="..." preview=true   # Preview changes
6. modify_code entityId="..." preview=false  # Apply + auto-validate
```

### Available Modification Tools

#### `modify_code` — Replace Entity Code
Replaces the entire entity (function, class, method) with new code.

```typescript
modify_code({
  entityId: "src/utils.ts::processData",  // Entity ID from get_members
  newCode: `function processData(input: string): Result {
    // New implementation
    return transform(input);
  }`,
  preview: true,        // Preview first!
  preserveComments: true,
  updateImports: true
})
```

#### `rename_symbol` — Smart Rename
Renames symbol and updates ALL references across the project.

```typescript
rename_symbol({
  entityName: "oldFunctionName",
  newName: "newFunctionName",
  preview: true,         // Preview first!
  updateReferences: true
})
```

#### `add_member` — Add to Class/Interface
Adds new method, property, or field to existing class.

```typescript
add_member({
  filePath: "/path/to/file.ts",
  entityId: "MyClass",
  memberCode: `async fetchData(): Promise<Data> {
    return await this.api.get('/data');
  }`,
  position: "end"  // start | end | after
})
```

#### `create_file` — Create New File
Creates file and auto-indexes it into the graph.

```typescript
create_file({
  filePath: "/path/to/new-file.ts",
  content: `export function helper() { ... }`,
  updateGraph: true
})
```

### Rollback & Safety

#### `create_snapshot` — Backup Before Changes
```typescript
create_snapshot({ description: "Before auth refactoring" })
```

#### `undo` — Rollback to Snapshot
```typescript
undo({ snapshotId: "snap-123" })
```

#### `list_snapshots` — View Backups
```typescript
list_snapshots({ limit: 10 })
```

---

## Common Workflows

### 1. Understanding New Project

```
1. detect_technology_stack                   # Detect stack
2. get_graph_stats                           # View statistics
3. analyze_hotspots metric="complexity"      # Find complex code
4. semantic_search query="entry point"       # Find entry points
```

### 2. Safe Refactoring

```
1. semantic_search query="target code"       # Find target
2. analyze_code_impact entityId="..."        # Assess what breaks
3. create_snapshot description="Before..."   # Backup
4. modify_code entityId="..." preview=true   # Preview changes
5. modify_code entityId="..." preview=false  # Apply changes
```

### 3. Finding Problematic Code

```
semantic_search minCyclomatic=10             # Complex code
semantic_search hasAwaits=true hasExceptions=false  # Async without try/catch
semantic_search hasDocumentation=false       # Undocumented
```

### 4. Safe Rename Across Project

```
1. list_entity_relationships entityName="OldName"
2. analyze_code_impact entity="OldName"
3. create_snapshot description="Before renaming"
4. rename_symbol entityName="OldName" newName="NewName" preview=true
5. rename_symbol entityName="OldName" newName="NewName" preview=false
```

---

## Tool Reference

### Indexing

#### `index`
Manually trigger codebase indexing. **Indexing is automatic** — use this only for troubleshooting when search results seem incomplete or outdated.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `directory` | string | current | Directory to index |
| `incremental` | boolean | false | Changed files only |
| `reset` | boolean | false | Clear graph before indexing |

> **Note**: If semantic search returns incomplete results, try `index reset=true` to rebuild the graph.

### Search

#### `semantic_search`
**Semantic search by meaning.** Returns rich metadata: complexity, control flow, docs.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | **required** | Natural language search |
| `limit` | number | 10 | Max results |
| `projectPath` | string | current | Cross-project search |
| `minCyclomatic` | number | - | Min complexity |
| `hasExceptions` | boolean | - | Must have try-catch |
| `hasAwaits` | boolean | - | Must have await |
| `hasDocumentation` | boolean | - | Must have docs |

#### `pattern_search`
Advanced search: `entity` / `content` / `semantic` / `hybrid` modes.

#### `find_similar_code`
Find semantically similar code by snippet.

### Entity Analysis

#### `get_members`
List all entities in file. **Use to get entity IDs for modify_code.**

#### `list_entity_relationships`
Show entity dependencies (callers, callees).

#### `analyze_code_impact`
**Change impact analysis** — what breaks when entity changes.

### Code Quality

#### `detect_code_clones`
Semantic duplicate detection.

#### `analyze_hotspots`
Find complex code: `complexity` / `changes` / `coupling`.

#### `validate_file`
Validate file syntax/types (ESLint/Pylint).

### Code Modification

#### `modify_code`
Replace entity code with preview and rollback support.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `entityId` | string | **required** | Entity ID |
| `newCode` | string | **required** | New code |
| `preview` | boolean | true | Preview changes |
| `preserveComments` | boolean | true | Keep comments |
| `updateImports` | boolean | true | Update imports |

#### `rename_symbol`
Rename symbol across project with reference updates.

#### `create_file`
Create new file with auto-indexing.

#### `add_member`
Add member to class/interface.

### Snapshots & Rollback

#### `create_snapshot`
Create backup before changes.

#### `undo`
Rollback to snapshot.

#### `list_snapshots`
List available snapshots.

### Git Integration

#### `list_branches` / `switch_branch`
Branch management for indexed branches.

#### `get_changed_files`
Files changed between branches.

---

## Related Skills

- **`ultracode-trace`** — Debugging, flow analysis, "why not called"
- **`ultracode-autodoc`** — Project memory with auto-updated code refs, find code by business meaning

---

## Cross-Project Support

```
# Switch context via index
index directory="D:\\other\\project"

# Or search in another project directly
semantic_search query="auth" projectPath="D:\\other\\project"
```

Storage: `%LOCALAPPDATA%\UltraScriptTools\projects\{hash}/`
