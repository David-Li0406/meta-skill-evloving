# Item Types Reference

kspec supports several item types that form a hierarchy for organizing specifications. Choosing the right type helps maintain clarity and enables better tooling support.

## Type Hierarchy

```
Project Root
  └── module (organizational grouping)
        ├── feature (user capability)
        │     ├── requirement (specific behavior)
        │     └── constraint (limitation)
        └── decision (architectural choice)

Traits (defined at root level, applied across specs)
```

## Type Definitions

### module

**Purpose**: High-level organizational unit for grouping related specs.

**When to use**:
- Grouping features by domain (e.g., "Authentication", "CLI Commands")
- Creating logical boundaries in large projects
- Organizing specs that share context

**Characteristics**:
- Contains features, decisions, and constraints
- Usually doesn't have AC (organizational, not behavioral)
- Top-level grouping mechanism

```bash
kspec item add --title "Task Management" --type module --slug tasks-module
```

### feature

**Purpose**: User-facing capability that delivers value.

**When to use**:
- Describing something users can do
- Defining a cohesive piece of functionality
- When AC describe user-observable outcomes

**Characteristics**:
- Should have acceptance criteria
- May contain requirements for detailed behaviors
- Links to tasks via `kspec derive`

```bash
kspec item add --under @tasks-module --title "Task Completion" --type feature --slug task-completion
```

### requirement

**Purpose**: Specific, testable behavior within a feature.

**When to use**:
- Breaking down a feature into detailed behaviors
- When a feature has multiple distinct test scenarios
- Describing implementation-level expectations

**Characteristics**:
- Always has acceptance criteria
- Lives under a feature
- More granular than features

```bash
kspec item add --under @task-completion --title "Completion with reason" --type requirement
```

### constraint

**Purpose**: Limitation, boundary, or non-functional requirement.

**When to use**:
- Performance requirements ("must respond in <100ms")
- Security constraints ("must encrypt data at rest")
- Compatibility requirements ("must work on Node 18+")
- Resource limits ("must use <512MB memory")

**Characteristics**:
- Describes what the system must NOT do or limits
- Can exist at module or feature level
- Often has quantifiable criteria

```bash
kspec item add --under @api-module --title "Rate Limiting" --type constraint --slug rate-limit
```

### decision

**Purpose**: Architectural decision record (ADR-style documentation).

**When to use**:
- Documenting why a technology was chosen
- Recording trade-offs considered
- Preserving context for future maintainers

**Characteristics**:
- Captures context, decision, and consequences
- May not have traditional AC
- Serves as documentation, not implementation spec

```bash
kspec item add --under @core-module --title "Use YAML for specs" --type decision
```

### trait

**Purpose**: Reusable bundle of acceptance criteria for cross-cutting concerns.

**When to use**:
- Same behavior needed across 3+ specs
- Cross-cutting concerns (logging, error handling, output formats)
- Ensuring consistency across similar commands

**Characteristics**:
- Defined at project root level
- Has its own acceptance criteria
- Applied to specs via `kspec item trait add`
- See [traits.md](traits.md) for detailed documentation

```bash
kspec trait add "JSON Output" --description "Commands support --json flag" --slug json-output
```

## Choosing the Right Type

| What you're describing | Type | Example |
|------------------------|------|---------|
| A domain or area | module | "Authentication", "CLI" |
| Something users can do | feature | "Login", "Export data" |
| How something behaves | requirement | "Password validation rules" |
| A limitation or boundary | constraint | "Max 1000 items per query" |
| Why a choice was made | decision | "Use PostgreSQL over MySQL" |
| Reusable behavior pattern | trait | "JSON output mode" |

### Decision Tree

```
Is it organizational grouping?
  Yes → module
  No ↓

Is it a user-facing capability?
  Yes → feature
  No ↓

Is it detailed behavior within a feature?
  Yes → requirement
  No ↓

Is it a limitation or boundary?
  Yes → constraint
  No ↓

Is it documenting a choice?
  Yes → decision
  No ↓

Is it reusable across specs?
  Yes → trait
```

## Commands

```bash
# List available types
kspec item types

# Create item with specific type
kspec item add --under <parent> --title "..." --type <type> [--slug <slug>]

# List items filtered by type
kspec item list --type feature
kspec item list --type requirement

# Check item type
kspec item get <ref>  # Shows type in output
```

## Hierarchy Best Practices

1. **Keep hierarchy shallow** - 2-3 levels is usually enough
2. **Use modules sparingly** - Only when you have 5+ related features
3. **Features are the core** - Most specs should be features or requirements
4. **Requirements decompose features** - Use when a feature is complex
5. **Traits reduce duplication** - Extract common AC patterns

## Related

- [Back to Spec Overview](../SKILL.md)
- [Acceptance Criteria Guide](acceptance-criteria.md) - Writing good AC
- [Traits Reference](traits.md) - Cross-cutting behavior patterns
