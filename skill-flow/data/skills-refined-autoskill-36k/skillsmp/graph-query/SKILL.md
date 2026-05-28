---
name: graph-query
description: Query the code graph for callers, dependencies, and blast radius. Use when you need to understand code relationships, find what calls a function, determine impact of changes, or explore the codebase structure.
allowed-tools: Bash
---

# Graph Query Skill

Query the code graph built from ts-morph static analysis to understand codebase structure and relationships.

## MCP Tools (Preferred)

When the MCP server is available, use native tools:

| Tool                 | Purpose                                       |
| -------------------- | --------------------------------------------- |
| `graph_what_calls`   | Find all callers of a function                |
| `graph_blast_radius` | Find impact of changes to a file (transitive) |
| `graph_find`         | Search for entities by name and type          |

**Use graph tools instead of Grep chains. 1 query = 10 greps worth of info.**

## CLI Quick Reference (Fallback)

```bash
# Shortcuts
bun run g:calls <function>    # Who calls this?
bun run g:deps <type>         # Who uses this type?
bun run g:blast <file>        # Impact of change?
bun run g:find <name>         # Where is this?
bun run g:summary             # Stats for codebase

# Long form (equivalent)
bun run checkpoint graph what-calls <function>
bun run checkpoint graph what-depends-on <type>
bun run checkpoint graph blast-radius <file>
bun run checkpoint graph find <name>
bun run checkpoint graph exports <package>
```

---

## When to Use

- Finding what calls a specific function
- Understanding dependencies on a module/class/type
- Assessing blast radius before refactoring
- Searching for entities by name or type
- Exploring package exports
- Getting codebase statistics

## CLI Reference

All commands use the checkpoint CLI:

```bash
bun run checkpoint graph <command> [args...]
```

## Commands

### Parse Package

Parse a package directory and store the graph data:

```bash
bun run checkpoint graph parse <package-path> [package-name] [--quiet]
```

Example:

```bash
bun run checkpoint graph parse packages/openbadges-types
bun run checkpoint graph parse packages --quiet  # Suppress verbose output
```

### What Calls

Find all callers of a function or method:

```bash
bun run checkpoint graph what-calls <name>
```

Example:

```bash
bun run checkpoint graph what-calls parsePackage
bun run checkpoint graph what-calls storeGraph
```

### Callers (Direct)

Find direct callers of a function (simpler output than what-calls):

```bash
bun run checkpoint graph callers <function-name>
```

Example:

```bash
bun run checkpoint graph callers handleGraphCommands
```

### What Depends On

Find all entities that depend on a given entity:

```bash
bun run checkpoint graph what-depends-on <name>
```

Example:

```bash
bun run checkpoint graph what-depends-on OB3Credential
bun run checkpoint graph what-depends-on BadgeClass
```

### Blast Radius

Find all entities that would be affected by changes to a file:

```bash
bun run checkpoint graph blast-radius <file-path>
```

Example:

```bash
bun run checkpoint graph blast-radius src/graph/index.ts
bun run checkpoint graph blast-radius packages/openbadges-types/src/index.ts
```

### Find Entities

Search for entities by name, optionally filtered by type:

```bash
bun run checkpoint graph find <name> [type]
```

Valid types: `function`, `class`, `type`, `interface`, `variable`, `file`

Example:

```bash
bun run checkpoint graph find Badge
bun run checkpoint graph find Badge class
bun run checkpoint graph find Credential type
```

### Exports

List all exported entities from a package:

```bash
bun run checkpoint graph exports [package-name]
```

Example:

```bash
bun run checkpoint graph exports openbadges-types
bun run checkpoint graph exports  # All packages
```

### Summary

Show graph statistics for a package or entire codebase:

```bash
bun run checkpoint graph summary [package-name]
```

Example:

```bash
bun run checkpoint graph summary claude-knowledge
bun run checkpoint graph summary  # All packages
```

## Example: Understanding Impact Before Refactoring

```bash
# 1. Find what the function is called
bun run checkpoint graph what-calls createBadge

# 2. Check what depends on the type it returns
bun run checkpoint graph what-depends-on Badge

# 3. Get full blast radius for the file
bun run checkpoint graph blast-radius src/badges/create.ts
```

## Example: Exploring Unfamiliar Code

```bash
# 1. Get overview of a package
bun run checkpoint graph summary openbadges-types

# 2. See what it exports
bun run checkpoint graph exports openbadges-types

# 3. Find specific entities
bun run checkpoint graph find Credential
```

## Output Format

### Query Commands

Most commands (`what-calls`, `what-depends-on`, `blast-radius`, `find`, `exports`, `callers`) return JSON with:

- `query`: The command type
- `results`: Array of matching entities/relationships
- `count`: Number of results

Entity objects include:

- `id`: Unique identifier
- `name`: Entity name
- `type`: Entity type (function, class, type, interface, variable, file)
- `package`: Package containing the entity
- `file`: File path
- `line`: Line number (where applicable)

### Parse Command

The `parse` command returns a different schema:

- `command`: "parse"
- `packagePath`: Path that was parsed
- `packageName`: Resolved package name
- `files`: Number of files parsed
- `entities`: Number of entities found
- `relationships`: Number of relationships found
- `stored`: Object with `entities` and `relationships` counts stored to database

### Summary Command

The `summary` command returns statistics without a `results` array:

- `query`: "summary"
- `package`: Package name or "all"
- `totalEntities`: Total entity count
- `totalRelationships`: Total relationship count
- `byType`: Breakdown of entities by type
