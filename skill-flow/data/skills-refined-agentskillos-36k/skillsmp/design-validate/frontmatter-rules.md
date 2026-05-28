# Design Doc Frontmatter Validation Rules

Complete reference for validating design document frontmatter fields and
values.

## Frontmatter Field Rules

| Field | Type | Required | Validation |
| :---- | :--- | :------- | :--------- |
| status | string | Yes | One of: stub, draft, current, needs-review, archived |
| module | string | Yes | Must exist in config |
| category | string | Yes | Must be in module's categories |
| created | string | Yes | YYYY-MM-DD format |
| updated | string | Yes | YYYY-MM-DD format, >= created |
| last-synced | string | Yes | "never" or YYYY-MM-DD, >= updated |
| completeness | number | Yes | Integer 0-100 |
| related | array | Yes | Array of paths (can be empty) |
| dependencies | array | Yes | Array of paths (can be empty) |

## Status-Completeness Matrix

| Completeness | Expected Status |
| :----------- | :-------------- |
| 0-20 | stub |
| 21-60 | draft |
| 61-90 | current, needs-review |
| 91-100 | current |

## Required Sections

Minimum sections (from config):

- Overview
- Current State
- Rationale
- Related Documentation

Category-specific sections:

- **Architecture**: System Architecture, Data Flow, Integration Points
- **Performance**: Performance Characteristics, Optimization Strategies,
  Benchmarks
- **Observability**: Event System, Logging Strategy, Metrics Collection
