---
name: golang
description: GraphStructManager Go 1.25 + Gremlin guidelines
---

# Overview

You are maintaining GraphStructManager, a type-safe, chainable Gremlin query builder for Go.
Prioritize correctness, predictable API behavior, and clear mapping between Go structs and
Gremlin traversals.

## Inspiration

- The API is inspired by GORM, but adapted for graph databases and Gremlin traversals rather
  than SQL.

## Repository Context

- Go version: 1.25 (module `github.com/jbrusegaard/graph-struct-manager`)
- Gremlin: Apache TinkerPop `gremlin-go` v3.7.4
- Core packages: `gremlin/driver`, `gsmtypes`, `comparator`, `log`
- Public surface: generic query builder (`Query[T gsmtypes.VertexType]`) and helper APIs

## Graph Model Conventions

- Vertex structs must embed `gsmtypes.Vertex` anonymously; `Create`/`Update` validate this.
- Edge structs (when used) embed `gsmtypes.Edge` and implement `gsmtypes.EdgeType`.
- Use `gremlin:"field_name"` tags for properties; `gremlin:"field_name,omitempty"` skips
  zero values and nil pointers during create/update.
- Use `gremlinSubTraversal:"alias"` for subtraversal projections; the alias must match
  `AddSubTraversal` usage.
- Label resolution: `Label() string` wins; empty label defaults to snake_case struct name.

## Query Builder Design

- Keep methods chainable and consistent with existing behavior (mutate query, return `*Query[T]`).
- Use `comparator` constants for predicates; map them to Gremlin `P`/`TextP` consistently.
- Preserve debug string building and `GSM_DEBUG` behavior when adding query steps.
- `Range` is ignored when `Offset` is set; maintain this behavior and warnings.
- `Take()` returns the first result; `ID()` performs fast ID lookup using `HasLabel`.

## Struct Mapping and Tags

- `structToMap` drives create/update; it ignores `gremlinSubTraversal` tags.
- `UnloadGremlinResultIntoStruct` maps Gremlin results to tagged fields, including anonymous
  embedded structs and subtraversal aliases.
- When changing mapping rules, update tests under `gremlin/driver/*_test.go`.

## Logging and Diagnostics

- Logging uses `log.InitializeLogger()` and `GSM_LOG_LEVEL`.
- Query debugging uses `GSM_DEBUG=true` to emit generated traversal strings.

## Error Handling

- Return explicit errors; wrap with context (`fmt.Errorf("context: %w", err)`).
- Avoid panics and hidden behavior changes; align error messages with existing usage.

## Testing and Docs

- Prefer table-driven tests and cover exported behavior.
- If you change public API or query semantics, update `README.md` examples to match.
