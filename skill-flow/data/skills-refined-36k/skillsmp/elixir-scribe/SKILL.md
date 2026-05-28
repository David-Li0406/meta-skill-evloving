---
name: elixir-scribe
description: Single Responsibility Code in Self-Documented Folder Structure
---

# Elixir-Scribe Skill

Use this skill when:
- Organizing code by Domain/Resource/Action structure
- Enforcing Single Responsibility Principle via folder structure
- Building projects without Ash framework
- Creating self-documenting folder structures
- Working with Nerves embedded projects

## When to Use

### Use elixir-scribe instead of Ash when:
- You prefer explicit folder structure over DSL macros
- You're building Nerves projects (embedded systems)
- You want manual control over code organization
- You're migrating from non-Ash codebases
- You prefer code over configuration (no magic)

### Use Ash instead of elixir-scribe when:
- You want declarative resource definitions
- You need automatic code generation (APIs, migrations)
- You're building Phoenix + Ash applications
- You prefer code interfaces over folder structure
- You want framework-level enforcement

## Folder Structure Pattern

### Elixir-Scribe Structure
```
lib/
└── my_app/
    └── domains/
            └── catalog/
                    └── product/
                              ├── create.ex
                              ├── update.ex
                              ├── delete.ex
                              └── list.ex
```

**Key Characteristics**:
- Self-documenting: Folder structure reveals all domains, resources, and actions
- One file per action: Enforces Single Responsibility Principle
- Explicit code: No DSL macros or code generation
- Manual enforcement: Developer discipline via file organization

### Ash Structure (for comparison)
```elixir
defmodule MyApp.Catalog.Product do
  use Ash.Resource

  actions do
    create :create
    update :update
    destroy :delete
    read :list
  end
end
```

**Key Characteristics**:
- Declarative: Actions defined within resource DSL
- Code generation: Framework generates boilerplate automatically
- Framework enforcement: Ash provides conventions and patterns
- Implicit structure: Structure derived from DSL, not explicit folders

## Integration with ai-rules

### Architect Role
- Consult `skills/elixir-scribe/SKILL.md` for folder structure decisions
- Use decision matrix in `roles/architect.md` to choose Ash vs elixir-scribe

### Orchestrator Role
- Follow folder structure when using elixir-scribe
- Use Ash DSL when using Ash framework

### Nerves Template
- Dedicated template: `templates/nerves-elixir-scribe.md` for Nerves projects
- Follows elixir-scribe pattern with embedded systems considerations

## Key Principles (Both Approaches)

### Shared Principles
1. **Domain-first organization**: Domains contain resources
2. **Clear resource boundaries**: Resources represent entities
3. **Action separation**: Actions are distinct operations
4. **Public API contracts**: Don't expose internal implementation
5. **Reducing technical debt**: Organized code is maintainable

### elixir-scribe Specific
- **Explicit folder structure**: Self-documenting via file system
- **Manual enforcement**: Developer discipline vs framework enforcement
- **One action per module**: File-based separation
- **Anti-magic**: Explicit code over DSL generation
- **Self-documenting**: Folder names serve as documentation

### Ash Specific
- **Declarative DSL**: Actions defined in resource
- **Code generation**: Automatic API/migration generation
- **Macros and derivation**: Framework provides boilerplate
- **Resource-centric**: Structure derived from DSL
- **Type safety**: Ash changesets with validation
- **Policies**: Declarative authorization
- **Query DSL**: Natural syntax for filtering

## Decision Matrix

| Criteria | elixir-scribe | Ash Framework |
|-----------|----------------|-----------------|
| **Team size** | Small teams (< 5) who value explicit structure | Any size, especially larger teams |
| **Project type** | Nerves embedded, vanilla Elixir | Phoenix web apps, Ash-based backends |
| **Code philosophy** | Prefer explicit code, avoid magic | Prefer declarative, leverage code gen |
| **Team experience** | Junior teams learning structure | Senior teams wanting productivity |
| **Maintenance preference** | Want manual control | Want automatic features |
| **Scalability needs** | Simple services, embedded systems | Complex domains, APIs |
| **Existing codebase** | Non-Ash Elixir code | Ash-based application |
| **Framework adoption** | Framework-agnostic | Adopting Ash Framework |

**Rule of Thumb**:
- **Use elixir-scribe for**: Nerves projects, embedded systems, simple Elixir services
- **Use Ash for**: Phoenix + Ash apps, complex domains, API-heavy projects
- **Hybrid possible**: Mix both approaches for different domains in same project

## Key References
- Elixir-Scribe GitHub: https://github.com/Elixir-Scribe/elixir-scribe
- Elixir-Scribe Docs: https://hexdocs.pm/elixir_scribe
- Alternative approach: Ash Framework (skills/api-design/SKILL.md)
- Comparison guide: `docs/ash_vs_elixir_scribe.md` (to create)
