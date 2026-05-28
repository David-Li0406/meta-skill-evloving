---
name: create-technical-documentation
description: Use this skill to create focused, specific technical documentation for codebase sections, analyzing code and identifying topics before writing.
---

# Technical Documentation Creation

## Purpose

Create **focused, specific** technical documentation for codebase sections. Unlike general docs (README, CHANGELOG), this skill produces **deep-dive articles** on components, patterns, or subsystems.

## When to Use

- Documenting a complex module or subsystem
- Creating tutorials for internal APIs
- Writing architectural explainers
- Onboarding documentation for new developers
- Self-documenting AgentOps skills and workflows

## Core Workflow

```
Analyze → Discover Topics → Present Options → Write → Review
```

---

## Phase 1: Analysis

### Input Types

| Input | Scope | Use Case |
|-------|-------|----------|
| Entire codebase | Broad discovery | Initial documentation audit |
| Folder/module | Scoped | Document a subsystem |
| Single file | Detailed | Deep dive on one component |
| Code snippet | Targeted | Explain specific pattern |

### Analysis Procedure

1. **Read context map** (`.agent/map.md`) if available
2. **Scan target scope**:
   - Entry points and exports
   - Public API surface
   - Dependencies (imports/requires)
   - Configuration points
3. **Check existing docs**:
   - `.agent/docs/` — agent-generated docs
   - `docs/` — project docs
   - `README.md` — top-level overview
4. **Output**: List of components with documentation potential

---

## Phase 2: Topic Discovery

### Topic Types

| Type | Description | Best For |
|------|-------------|----------|
| **How-To** | Step-by-step task completion | Practical tasks |
| **Explainer** | Concept/design rationale | Understanding "why" |
| **Reference** | API/config/schema details | Quick lookup |
| **Tutorial** | Learning path with examples | Onboarding |
| **Deep Dive** | Internal implementation details | Advanced users |

### Topic Sizing Guidelines

Good topics are:
- **Readable in 5-15 minutes**
- **Self-contained** (minimal external dependencies)
- **Actionable** (reader can do something) or **educational** (reader understands something)

Split large topics into series if needed.

### Discovery Output

Generate topic candidates with:
- Title (action-oriented or descriptive)
- Type (How-To, Explainer, etc.)
- Target audience (beginner, intermediate, advanced)
- Estimated length (short: <500 words, medium: 500-1500, long: >1500)
- Overlap check (similar existing docs)

---

## Phase 3: Interactive Selection

**Use `agent-ops-interview` to present topics before writing.**

### Topic Presentation Format

```markdown
📚 **Documentation Topics for `src/bundle/installer.py`**

I identified 5 potential documentation topics:

1. **[How-To]** Installing bundles with category filtering
   - Audience: End users | Length: Medium
   
2. **[Explainer]** How the conflict resolution algorithm works
   - Audience: Contributors | Length: Long
   
3. **[Reference]** BundleInstaller public API
   - Audience: Developers | Length: Medium
   
4. **[Deep Dive]** Frontmatter parsing and category discovery
   - Audience: Advanced | Length: Long
   
5. **[Tutorial]** Creating a custom bundle category
   - Audience: Beginners | Length: Medium

Which topics should I write? (comma-separated numbers, 'all', or 'suggest')
```

### Selection Options

| Response | Action |
|----------|--------|
| `1,3,5` | Write selected topics |
| `all` | Write all topics |
| `suggest` | Agent recommends based on gaps |
| `none` | Skip documentation |
| `refine 2` | Discuss topic 2 scope before deciding |

---

## Phase 4: Writing

### Code Block Standards

**Always include:**
- File path
- Line numbers (when referencing specific code)
- Syntax highlighting

**Format:**

````markdown
```python title="src/bundle/installer.py" linenums="42"
def load_category_manifest(bundle_path: Path) -> CategoryManifest:
    """Load category definitions and build dynamic mappings."""
    manifest_path = bundle_path / "bundle-categories.yaml"
    if not manifest_path.exists():
        return CategoryManifest(categories={}, presets={})
    # ...
```
````

### Code Extraction Rules

1. **Show relevant context** — not entire files
2. **Highlight key lines** — use comments or annotations
3. **Link to source** — provide file path for full code
4. **Keep snippets runnable** — when possible, show complete examples

### Structure by Type

#### How-To Structure

```markdown
# How to [Action]

## Prerequisites
- Requirement 1
- Requirement 2

## Steps

### 1. [First Step]
[Explanation + code]

### 2. [Second Step]
[Explanation + code]

## Result
[What the user should see/have]

## Troubleshooting
| Problem | Solution |
|---------|----------|
| Error X | Fix Y |
```

#### Explainer Structure

```markdown
# Understanding [Concept]

## What It Is
[One paragraph definition]

## Why It Exists
[Problem it solves, context]

## How It Works
[Detailed explanation with diagrams/code]

### [Subcomponent 1]
[Details]

### [Subcomponent 2]
[Details]

## Trade-offs
| Approach | Pros | Cons |
|----------|------|------|

## Related Concepts
- [Link to related doc 1]
- [Link to related doc 2]
```

#### Reference Structure

```markdown
# [Component] Reference

## Overview
[Brief description]

## API

### `function_name(param1, param2)`

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|

**Returns:** `ReturnType` — Description

**Raises:**
- `ErrorType` — When condition

**Example:**
```language
// Usage example
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|

## See Also
- [Related reference]
```

#### Tutorial Structure

```markdown
# Tutorial: [Learning Goal]

## What You'll Learn
- Skill 1
- Skill 2

## Prerequisites
- Knowledge required
- Tools needed

## Part 1: [Foundation]
[Explanation + hands-on]

## Part 2: [Building]
[Explanation + hands-on]

## Part 3: [Completing]
[Explanation + hands-on]

## Summary
[Recap of skills learned]

## Next Steps
- [Advanced topic link]
- [Related tutorial link]
```

#### Deep Dive Structure

```markdown
# Deep Dive: [Internal Component]

> **Audience**: Contributors and advanced users

## Architecture Overview
[High-level diagram/description]

## Implementation Details

### [Subsystem 1]
[Code walkthrough with annotations]

### [Subsystem 2]
[Code walkthrough with annotations]

## Key Decisions
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|

## Extension Points
[How to customize/extend]

## Known Limitations
- Limitation 1
- Limitation 2

## Future Considerations
- Potential improvement 1
```

---

## Phase 5: Review

### Pre-Publish Checklist

- [ ] **Accuracy**: Code snippets match current source
- [ ] **Completeness**: All sections filled, no TODOs
- [ ] **Links**: No broken internal links
- [ ] **Code validity**: Snippets parse/compile
- [ ] **No secrets**: No API keys, passwords, internal URLs
- [ ] **Audience fit**: Complexity matches stated audience

### Overlap Check

Before finalizing, verify no duplication:
- Search existing docs for similar content
- If overlap found, offer to update existing instead of creating new

---

## Output Locations

| Content Type | Location |
|--------------|----------|
| Agent-generated docs | `.agent/docs/` |
| Project docs | `docs/` |
| MkDocs-ready | `docs/` with frontmatter |

### MkDocs Frontmatter

When outputting to `docs/` for MkDocs:

```yaml
---
title: "Document Title"
description: "Brief description for SEO/preview"
date: 2026-01-21
tags:
  - bundle
  - installation
---
```

---

## Self-Documentation Mode

This skill can document AgentOps itself:

**Suggested topics:**
- Skill system architecture
- Issue management workflow
- Bundle installer mechanics
- State file conventions
- Interview protocol patterns

To self-document:
```
Analyze .github/skills/ and create documentation for the AgentOps skill system
```

---

## Integration Points

| Skill | Integration |
|-------|-------------|
| `agent-ops-context-map` | Use map.md for codebase overview |
| `agent-ops-docs` | Coordinate README/CHANGELOG updates |
| `agent-ops-mkdocs` | Output compatible with MkDocs nav |
| `agent-ops-interview` | Topic selection dialog |

---

## Anti-Patterns

- ❌ Writing before presenting topic options
- ❌ Entire file dumps instead of focused snippets
- ❌ Code without line numbers or file paths
- ❌ Generic content that doesn't reference actual code
- ❌ Creating docs that duplicate existing content
- ❌ Skipping the audience/complexity assessment
- ❌ Outdated code snippets that don't match source