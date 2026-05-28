# Templates for Product and Requirements

These templates provide examples for creating human‑readable views from the
database. They are compiled by the scripts in `scripts/` and stored in
`product/views/`.

## Product Card (`PRODUCT.md`)

Include the product’s identity and high‑level information:

```
# {{ product.title }}

**Vision**: {{ product.vision or "TBD" }}

**Updated**: {{ now }}

## Scope

- **In scope**: List the main features or goals here.
- **Out of scope**: List what is explicitly excluded.

## Constraints

- Platform (e.g., web, mobile).
- Compliance (e.g., privacy, accessibility).
- Performance or scalability considerations.

## Terms and Entities

- **ExampleTerm**: Explanation

```

## Backlog (`BACKLOG.md`)

Summarise requirements as a simple list (diff-friendly):

- `R‑001` [PROPOSED, P2] Example Requirement — Short summary.
- `R‑002` [READY, P1] …

Then include a detailed section for each requirement:

```
### R‑001: Example Requirement

**Description**: Full description of the requirement.

**Acceptance Criteria**:

- The fireworks animation appears after clicking the trigger button.
- The density slider adjusts the number of particles from 10–1000.

**Status**: PROPOSED

**Priority**: P2

**Dependencies**: List other requirements here.

**Notes**: Any assumptions or remarks.
```

Repeat for each requirement.

## Open Questions (`OPEN_QUESTIONS.md`)

List unresolved questions that need answers, grouped by scope:

```
### Product-level questions

1. What platforms will this product support (e.g., macOS 13+, Windows)?
2. …

### Requirement R‑001 questions

1. What is the maximum fireworks density the user can set?
2. Should the trigger have a keyboard shortcut?

```