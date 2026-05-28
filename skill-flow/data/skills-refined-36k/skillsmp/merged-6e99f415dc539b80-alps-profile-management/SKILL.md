---
name: alps-profile-management
description: Use this skill to create, validate, and improve ALPS profiles for RESTful API design based on natural language descriptions or existing websites.
---

# ALPS Profile Management

Generate, validate, and improve ALPS profiles for RESTful API design.

## Ideal ALPS Profile

**Goal: An ALPS that someone unfamiliar with the app can read and understand.**

### What Makes a Good ALPS

1. **States = What the user sees**
   - Examples: `ProductList`, `ProductDetail`, `Cart`

2. **Transitions = What the user does**
   - Examples: `goProductDetail`, `doAddToCart`

3. **Self-documenting**
   - `title` explains the purpose
   - `doc` describes behavior and side effects

4. **No unreachable states**
   - Every state has an entry point

5. **Necessary and sufficient**
   - Describes semantics, not implementation

### What to Avoid

- Mechanical CRUD listings without meaning
- Implementation details leaking in
- States without transitions
- Excessive documentation nobody reads

## How to Use

This skill responds to natural language requests:

### Generate ALPS from Natural Language
- "Create an ALPS profile for a blog application"
- "Generate ALPS for an e-commerce cart system"
- "Design an ALPS profile for user authentication"

### Generate ALPS from Website (ALPS Surveyor Mode)
- "Crawl <url> and generate ALPS profile"
- "Survey website structure and create ALPS"

**How it works:**
1. **Efficient crawling**: Uses URL pattern classification to avoid redundant analysis.
2. **Token optimization**: Analyzes unique page types only.
3. **AI-powered extraction**: Analyzes DOM structure to infer states, transitions, and semantic fields.
4. **Handover protocol**: Records progress in `handover.json` for continuity across sessions.

### Validate Existing Profile
- "Validate this ALPS profile" (with file path or content)
- "Check my ALPS file for issues"

### Analyze or Improve Existing Profile
- "Analyze this ALPS profile"
- "Improve this ALPS profile"
- "Suggest enhancements for my ALPS"

### Continuous Improvement Loop

When asked to analyze or improve an existing profile:

1. **Read previous AI's insights**.
2. **Read `handover.json` if exists**.
3. **Inherit the context**.
4. **Identify gaps**.
5. **Make improvements**.
6. **MANDATORY: Validate ALPS**.
7. **MANDATORY: Generate HTML**.
8. **Update `handover.json`**.
9. **MANDATORY: Validate `handover.json`**.
10. **Report completion**.

## ALPS Structure Reference

### Three Layers of ALPS

1. **Ontology** - Semantic descriptors (data elements).
2. **Taxonomy** - State descriptors (screens/pages).
3. **Choreography** - Transition descriptors (actions).

### Naming Conventions

| Type | Prefix | Example |
|------|--------|---------|
| Safe transition | `go` | `goToHome` |
| Unsafe transition | `do` | `doCreateUser` |
| Idempotent transition | `do` | `doUpdateUser` |
| State/Page | PascalCase | `HomePage` |
| Semantic field | camelCase | `userId` |

## Generation Guidelines

### Strategy for Large Profiles

1. **Domain Decomposition** - Split into separate ALPS files by functional domain.
2. **Design Each Domain Independently**.
3. **Merge Using `asd merge`**.
4. **Validate After Each Merge**.

### When Creating ALPS from Natural Language

1. **Identify Entities** (Ontology).
2. **Identify States** (Taxonomy).
3. **Identify Transitions** (Choreography).
4. **Add Documentation**.
5. **Add Tags for Organization**.

### Output File Convention

**File name**: Always `alps.json` or `alps.xml`.

**Directory**: Use `alps/` directory if it exists, otherwise create `{app-name}/` directory.

### Validation and Quality Metrics

Use `asd --validate <file>` to validate ALPS profiles and get quality metrics.

## ALPS Surveyor Mode (Website Crawling)

### Overview

Extract ALPS profiles from existing websites by analyzing their structure.

### Efficient Crawling Strategy

1. **URL Pattern Classification**.
2. **DOM Structure Extraction**.
3. **ALPS Generation**.

### Handover Protocol

Use `handover.json` to enable multi-session work.

## References

- [ALPS Specification](http://alps.io/spec/)
- [Schema.org](https://schema.org/)
- [app-state-diagram](https://github.com/alps-asd/app-state-diagram)